#ifndef COMMON_UTIL_H
#define COMMON_UTIL_H

#include "ids-provider/pcapdissector/packet.h"
#include <netdissect.h>

// Define PCAP Global Header
struct pcap_global_header {
    uint32_t magic_number;   // Magic number: 0xa1b2c3d4 (standard) or 0xd4c3b2a1 (byte-swapped)
    uint16_t version_major;  // Major version (usually 2)
    uint16_t version_minor;  // Minor version (usually 4)
    int32_t  thiszone;       // GMT to local correction (0 for GMT)
    uint32_t sigfigs;        // Timestamp accuracy (usually 0)
    uint32_t snaplen;        // Snapshot length (max bytes per packet, e.g., 65535)
    uint32_t network;        // Link-layer type (e.g., Ethernet = 1)
};

// Define PCAP Packet Header (not pcap_pkthdr from libpcap)
struct pcap_packet_header {
    uint32_t ts_sec;   // Timestamp seconds
    uint32_t ts_usec;  // Timestamp microseconds
    uint32_t incl_len; // Captured length (caplen)
    uint32_t orig_len; // Original length (len)
};

extern struct kv_pair *load_yaml_config(
    netdissect_options *ndo,
    const char *config_file,
    size_t *count);

const char *get_option_value(
    struct kv_pair *pairs,
    size_t pairs_count,
    const char *search_key);

void write_packet_to_pcap(
    const char *filename,
    const struct pcap_pkthdr *pkt_hdr,
    const uint8_t *pkt_data);

void generate_timestamped_filename(
    const char* base_filename,
    char* buffer,
    size_t buffer_size);

char* base64_encode(
    const unsigned char* data,
    size_t input_length);

char* encode_packet_to_base64(const struct pcap_pkthdr* pkt_hdr, const uint8_t* pkt_data);

uint8_t* create_pcap_binary(
    const struct pcap_pkthdr* pkt_hdr,
    const uint8_t* pkt_data,
    size_t* output_size);

#define INET_ADDRSTRLEN 16 // Ensure space for IPv4 string

int get_current_ip_address(const char* device, char* ip_buffer, size_t buffer_len);

int process_next_layer(
    packet_t* packet,
    uint16_t protocol_id,
    const uint8_t* payload,
    size_t payload_len,
    const handler_t* handlers);

const unsigned char* hex_encode(
    const uint8_t* data,
    size_t len);

void trimWhitespace(char* str);

#endif
