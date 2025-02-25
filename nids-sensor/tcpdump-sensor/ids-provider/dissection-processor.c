#include "dissection-processor.h"
#include "ring-buffer.h"
#include "common-util.h"
#include <stdlib.h>

#include <sys/socket.h>
#include <netinet/in.h>
#include <arpa/inet.h>
#include <sys/types.h>

#include <sys/ioctl.h>
#include <net/if.h>
#include <unistd.h>

#include <lz4.h>
#include <pthread.h>
#include <string.h>
#include <pcap/pcap.h>  // For pcap_t, DLT values, pcap macros

#include "pcapdissector/packet.h"


#define MAX_JSON_SIZE 65536
#define MAX_PACKET_JSON_SIZE (65536 + 65536)

dissection_processor *dissection_processor_create(netdissect_options *ndo, char *device) {
    dissection_processor *dp = nd_malloc(ndo, sizeof(dissection_processor));
    if (dp) {
        struct kv_pair *pairs = ndo->ids_pairs;
        const size_t count = ndo->ids_pairs_count;

        dp->ndo = ndo;
        dp->running = 1;
        dp->device = device;
        dp->drop_ipv4_packets = false;
        dp->drop_ipv6_packets = false;
        dp->drop_no_ip_packets = false;
        dp->non_ip_packets_dropped = 0;

        dp->dlt = ndo->ids_dlt;
        dp->dlt_name = ndo->ids_dlt_name;

        int fd;
        struct ifreq ifr;

        fd = socket(AF_INET, SOCK_DGRAM, 0);

        ifr.ifr_addr.sa_family = AF_INET;
        strncpy(ifr.ifr_name, device, IFNAMSIZ - 1);

        ioctl(fd, SIOCGIFADDR, &ifr);
        close(fd);

        strncpy(dp->ip_address, inet_ntoa(((struct sockaddr_in *)&ifr.ifr_addr)->sin_addr), INET_ADDRSTRLEN);
        dp->ip_address[INET_ADDRSTRLEN - 1] = '\0';
        ndo->ip_address[INET_ADDRSTRLEN - 1] = '\0';
        printf("%s IP Address: %s\n", device, dp->ip_address);

        dp->drop_ipv4_packets = strcasecmp(get_option_value(pairs, count, "dissect.drop_ipv4_packets"), "TRUE") == 0;
        dp->drop_ipv6_packets = strcasecmp(get_option_value(pairs, count, "dissect.drop_ipv6_packets"), "TRUE") == 0;
        dp->drop_no_ip_packets = strcasecmp(get_option_value(pairs, count, "dissect.drop_no_ip_packets"), "TRUE") == 0;

        dp->attach_pcap_file = strcasecmp(get_option_value(pairs, count, "dissect.json.attach_pcap_file"), "TRUE") == 0;
        dp->packet_compression = strcasecmp(get_option_value(pairs, count, "dissect.json.compression"), "TRUE") == 0;
        dp->drop_no_cicfm_packets = strcasecmp(get_option_value(pairs, count, "dissect.drop_no_cicfm_packets"), "TRUE") == 0;
        return dp;
    }
    return NULL;
}

void dissection_processor_destroy(dissection_processor *dp) {
    if (dp) {
    }
}

void dissection_processor_run(const dissection_processor *dp, char *device) {
    netdissect_options *ndo = dp->ndo;
    struct ring_buffer *rb_in = ndo->ids_rb;
    struct ring_buffer *rb_out = ndo->ids_rb_json;

    if (rb_in == NULL) {
        fprintf(stderr, "Error: Input ring buffer (packet-buffer) is not initialized. Exiting dissection thread.\n");
        return;
    }

    if (rb_out == NULL) {
        fprintf(stderr, "Error: Output ring buffer (json-buffer) is not initialized. Exiting dissection thread.\n");
        return;
    }

    // Calculate maximum compressed size once
    int max_compressed_size = LZ4_compressBound(MAX_JSON_SIZE);
    if (max_compressed_size <= 0) {
        fprintf(stderr, "Failed to calculate max compressed size\n");
        return;
    }
    char *compressed_buffer = (char *) malloc(max_compressed_size);
    char *json_result = (char *) malloc(MAX_JSON_SIZE);
    if (!compressed_buffer || !json_result) {
        fprintf(stderr, "Failed to allocate memory for buffers\n");
        free(compressed_buffer);
        free(json_result);
        return;
    }

    time_t now = time(NULL);

    static size_t frameCounter = 1;

    static char packet_json_buffer[MAX_PACKET_JSON_SIZE];
    static char pcap_binary_field[MAX_JSON_SIZE] = {0};
    if (dp->attach_pcap_file) {
        memset(pcap_binary_field, 0, sizeof(pcap_binary_field));
    }

    while (dp->running) {
        size_t packet_len;
        struct timeval ts;

        now = time(NULL);

        const uint8_t *packet_data = ring_buffer_dequeue(rb_in, &packet_len, &ts);

        if (packet_data == NULL) {
            usleep(500);
            continue;
        }

        if (packet_len < sizeof(struct pcap_pkthdr)) {
            fprintf(stderr, "Error: Dequeued data smaller than pcap header\n");
            continue;
        }

        const struct pcap_pkthdr *pkt_hdr = (const struct pcap_pkthdr *) packet_data;
        const u_char *pkt_data = packet_data + sizeof(struct pcap_pkthdr);

        frameCounter++;
        packet_t *pkt = packet_create(pkt_data, pkt_hdr, dp->dlt);
        char *chain = build_protocol_chain(pkt, dp->dlt);
        //fprintf(stderr, "Protocol chain: %s\n", chain);

        if (dp->drop_no_cicfm_packets) {
            // Ensure the protocol chain STARTS with "eth:ip" (IPv4)
            if (strncmp(chain, "eth:ip:tcp", 10) == 0 ||
                strncmp(chain, "eth:ip:udp", 10) == 0 ||
                strncmp(chain, "eth:ip:icmp", 11) == 0 ||
                strncmp(chain, "eth:ip:sctp", 11) == 0) {
                //Regular IPv4-based transport layer (TCP/UDP/ICMP/SCTP)
                }
            else if (strncmp(chain, "eth:gre:ip", 10) == 0 ||
                     strncmp(chain, "eth:l2tp:ip", 11) == 0 ||
                     strncmp(chain, "eth:pppoe:ip", 12) == 0) {
                //Tunneling (GRE, L2TP, PPPoE) carrying IPv4 traffic
                     }
            else {
                packet_destroy(pkt);
                continue;
            }
        }

        char *packet_json = pkt ? packet_to_json(pkt) : NULL;

        char timestampEpoch[32];
        char timestampStringUtc[64];
        char timestampStringLocal[64];

        snprintf(timestampEpoch, sizeof(timestampEpoch),
                 "%ld.%06d",
                 (long)pkt_hdr->ts.tv_sec,
                 (int)pkt_hdr->ts.tv_usec);

        // 2) UTC string
        strftime(timestampStringUtc, sizeof(timestampStringUtc),
                 "%b %e, %Y %H:%M:%S", gmtime(&pkt_hdr->ts.tv_sec));
        snprintf(timestampStringUtc + strlen(timestampStringUtc),
                 sizeof(timestampStringUtc) - strlen(timestampStringUtc),
                 ".%06d UTC",
                 pkt_hdr->ts.tv_usec);

        struct tm *lt = localtime(&pkt_hdr->ts.tv_sec);
        if (lt) {
            strftime(timestampStringLocal, sizeof(timestampStringLocal),
                     "%b %e, %Y %H:%M:%S", lt);
            snprintf(timestampStringLocal + strlen(timestampStringLocal),
                     sizeof(timestampStringLocal) - strlen(timestampStringLocal),
                     ".%06d CET",
                     pkt_hdr->ts.tv_usec);
            // Example output: "Jan 26, 2025 13:27:13.938636 CET"
        } else {
            // Fallback if localtime() fails
            snprintf(timestampStringLocal, sizeof(timestampStringLocal), "unknown");
        }

        char dateString[32]; // Ensure enough space for "packets-YYYY-MM-DD"
        struct tm *captureDate = gmtime(&pkt_hdr->ts.tv_sec);
        if (captureDate) {
            // Format as "packets-YYYY-MM-DD"
            strftime(dateString, sizeof(dateString), "packets-%Y-%m-%d", captureDate);
            // Example output: "packets-2025-01-26"
        } else {
            snprintf(dateString, sizeof(dateString), "packets-unknown");
        }

        const char *protocol_chain = build_protocol_chain(pkt, dp->dlt);

        if (strcmp(protocol_chain, "") == 0) {
            fprintf(stderr, "ERROR: Failed to determine protocol chain\n");
        }
        if (dp->attach_pcap_file) {
            char *pcap_base64 = encode_packet_to_base64(pkt_hdr, pkt_data);
            if (pcap_base64) {
                snprintf(pcap_binary_field, sizeof(pcap_binary_field),
                         ", \"pcap_binary\":\"%s\"", pcap_base64); // Create the pcap_binary field
                free(pcap_base64);
            }
        }

        snprintf(packet_json_buffer, MAX_JSON_SIZE,
                 "{"
                 "\"_index\":\"%s\","
                 "\"_type\":\"doc\","
                 "\"_score\":null,"
                 "\"_source\":{"
                 "\"capture_host\":\"%s\","
                 "\"capture_interface_name\":\"%s\","
                 "\"layers\":{"
                 "\"frame\":{"
                 "\"frame_frame_encap_type\":%d,"
                 "\"frame_frame_time\":\"%s\","
                 "\"frame_frame_time_utc\":\"%s\","
                 "\"frame_frame_time_epoch\":%s," // No quotes around epoch
                 "\"frame_frame_offset_shift\":0.000000000," // Already a number
                 "\"frame_frame_time_delta\":0.000000000,"
                 "\"frame_frame_time_delta_displayed\":0.000000000,"
                 "\"frame_frame_time_relative\":0.000000000,"
                 "\"frame_frame_number\":%zu," // No quotes around frame number
                 "\"frame_frame_len\":%u," // No quotes around frame length
                 "\"frame_frame_cap_len\":%u," // No quotes around captured length
                 "\"frame_frame_marked\":0,"
                 "\"frame_frame_ignored\":0,"
                 "\"frame_frame_protocols\":\"%s\""
                 "},%s"
                 "}%s"
                 "}"
                 "}",
                 dateString,
                 dp->ip_address,
                 device,
                 dp->dlt, // No quotes, it's an integer
                 timestampStringLocal,
                 timestampStringUtc,
                 timestampEpoch, // No quotes, it's a number
                 frameCounter, // No quotes, it's a number
                 pkt_hdr->len, // No quotes, it's a number
                 pkt_hdr->caplen, // No quotes, it's a number
                 (pkt ? protocol_chain : "unknown"),
                 packet_json ? packet_json : "{}",
                 pcap_binary_field
        );


        size_t json_length = strlen(packet_json_buffer);
        packet_destroy(pkt);

        if (json_length == 0) {
            if (dp->drop_no_ip_packets) {
                continue;
            } else {
                fprintf(stderr, "Failed to dissect packet or buffer too small\n");
                continue;
            }
        }

        if (dp->packet_compression) {
            int compressed_size = LZ4_compress_default(packet_json_buffer, compressed_buffer, json_length,
                                                       max_compressed_size);

            if (compressed_size <= 0) {
                fprintf(stderr, "LZ4 compression failed\n");
                continue;
            }

            //size_t available_space = ring_buffer_available_space(rb_out);
            //fprintf(stderr, "JSON ring buffer available space: %zu packets\n", available_space);

            if (ring_buffer_push(ndo, rb_out, compressed_buffer, compressed_size, &ts)) {
                //fprintf(stderr, "JSON data pushed into json-buffer. Length: %d bytes\n", compressed_size);
            } else {
                fprintf(stderr, "json-buffer full. Dropping compressed JSON data.\n");
            }
        } else {
            if (ring_buffer_push(ndo, rb_out, packet_json_buffer, json_length, &ts)) {
                //fprintf(stderr, "JSON data pushed into json-buffer. Length: %d bytes\n", compressed_size);
            } else {
                fprintf(stderr, "json-buffer full. Dropping uncompressed JSON data.\n");
            }
        }

        usleep(10);

        //size_t a_available_space = ring_buffer_available_space(rb_out);
        //fprintf(stderr, "JSON ring buffer available space: %zu packets\n", a_available_space);
    }

    free(json_result);
}

void dissection_processor_stop(dissection_processor *dp) {
    dp->running = 0;
}
