//
// Created by Jochen van Waasen on 23.01.25.
//
#include "ids-provider/common-util.h"
#include "ipv4-layer.h"

#include <icmp-layer.h>
#include <stdlib.h>
#include <string.h>
#include <stdio.h>

int dissect_ipv4(layer_t *layer, packet_t *packet, const uint8_t *data, size_t len) {
    if (!layer || !data || len < 20) {
        // Minimum IPv4 header length
        fprintf(stderr, "Insufficient data for IPv4 dissection\n");
        return 1;
    }

    // Allocate memory for the IPv4 header structure
    ipv4_header_t *ip_hdr = (ipv4_header_t *) malloc(sizeof(ipv4_header_t));
    if (!ip_hdr) {
        fprintf(stderr, "Failed to allocate memory for IPv4 header\n");
        return 1;
    }

    // Parse the IPv4 header fields
    ip_hdr->version = (data[0] >> 4) & 0xF; // Extract version (4 bits)
    ip_hdr->ihl = data[0] & 0xF; // Extract header length (4 bits)
    ip_hdr->dscp = (data[1] >> 2) & 0x3F; // DSCP (6 bits)
    ip_hdr->ecn = data[1] & 0x3; // ECN (2 bits)
    ip_hdr->total_length = (data[2] << 8) | data[3]; // Total length
    ip_hdr->identification = (data[4] << 8) | data[5]; // Identification
    ip_hdr->flags = (data[6] >> 5) & 0x7; // Flags (3 bits)
    ip_hdr->fragment_offset = ((data[6] & 0x1F) << 8) | data[7]; // Fragment offset
    ip_hdr->ttl = data[8]; // Time to live
    ip_hdr->protocol = data[9]; // Protocol
    ip_hdr->header_checksum = (data[10] << 8) | data[11]; // Header checksum
    memcpy(ip_hdr->src_addr, &data[12], 4); // Source address
    memcpy(ip_hdr->dst_addr, &data[16], 4); // Destination address

    // Store the parsed header in the layer
    layer->parsed_data = ip_hdr;
    layer->to_json = ipv4_to_json;

    // Calculate the payload offset
    size_t header_length = ip_hdr->ihl * 4; // IHL is in 4-byte units
    if (len < header_length) {
        fprintf(stderr, "Invalid IPv4 header length\n");
        free(ip_hdr);
        return 1;
    }

    const uint8_t *payload = data + header_length;
    size_t payload_len = len - header_length;

    return process_next_layer(packet, ip_hdr->protocol, payload, payload_len, handlers);
}

#define JSON_BUFFER_SIZE 4096
static _Thread_local char json_buffer[JSON_BUFFER_SIZE];

char *ipv4_to_json(layer_t *layer) {
    if (!layer || !layer->parsed_data) return NULL;

    ipv4_header_t *ip_hdr = (ipv4_header_t *) layer->parsed_data;

    int bytes_written = snprintf(json_buffer, JSON_BUFFER_SIZE,
                                 "\"ip\": {"
                                 "\"ip_ip_addr\": [\"%u.%u.%u.%u\", \"%u.%u.%u.%u\"],"
                                 "\"ip_ip_checksum\": \"0x%04X\","
                                 "\"ip_ip_checksum_status\": \"2\","
                                 "\"ip_ip_dsfield\": \"0x%02X\","
                                 "\"ip_ip_dsfield_dscp\": \"%u\","
                                 "\"ip_ip_dsfield_ecn\": \"%u\","
                                 "\"ip_ip_dst\": \"%u.%u.%u.%u\","
                                 "\"ip_ip_dst_host\": \"%u.%u.%u.%u\","
                                 "\"ip_ip_flags\": \"0x%02X\","
                                 "\"ip_ip_flags_df\": %s,"
                                 "\"ip_ip_flags_mf\": %s,"
                                 "\"ip_ip_flags_rb\": %s,"
                                 "\"ip_ip_frag_offset\": \"%u\","
                                 "\"ip_ip_hdr_len\": \"%u\","
                                 "\"ip_ip_host\": [\"%u.%u.%u.%u\", \"%u.%u.%u.%u\"],"
                                 "\"ip_ip_id\": \"0x%04X\","
                                 "\"ip_ip_len\": \"%u\","
                                 "\"ip_ip_proto\": \"%u\","
                                 "\"ip_ip_src\": \"%u.%u.%u.%u\","
                                 "\"ip_ip_src_host\": \"%u.%u.%u.%u\","
                                 "\"ip_ip_stream\": \"0\","
                                 "\"ip_ip_ttl\": \"%u\","
                                 "\"ip_ip_version\": \"%u\""
                                 "}",
                                 ip_hdr->src_addr[0], ip_hdr->src_addr[1], ip_hdr->src_addr[2], ip_hdr->src_addr[3],
                                 ip_hdr->dst_addr[0], ip_hdr->dst_addr[1], ip_hdr->dst_addr[2], ip_hdr->dst_addr[3],
                                 ip_hdr->header_checksum,
                                 (ip_hdr->dscp << 2) | ip_hdr->ecn,
                                 ip_hdr->dscp,
                                 ip_hdr->ecn,
                                 ip_hdr->dst_addr[0], ip_hdr->dst_addr[1], ip_hdr->dst_addr[2], ip_hdr->dst_addr[3],
                                 ip_hdr->dst_addr[0], ip_hdr->dst_addr[1], ip_hdr->dst_addr[2], ip_hdr->dst_addr[3],
                                 ip_hdr->flags,
                                 (ip_hdr->flags & 0x40) ? "true" : "false",
                                 (ip_hdr->flags & 0x20) ? "true" : "false",
                                 (ip_hdr->flags & 0x80) ? "true" : "false",
                                 ip_hdr->fragment_offset,
                                 ip_hdr->ihl * 4,
                                 ip_hdr->src_addr[0], ip_hdr->src_addr[1], ip_hdr->src_addr[2], ip_hdr->src_addr[3],
                                 ip_hdr->dst_addr[0], ip_hdr->dst_addr[1], ip_hdr->dst_addr[2], ip_hdr->dst_addr[3],
                                 ip_hdr->identification,
                                 ip_hdr->total_length,
                                 ip_hdr->protocol,
                                 ip_hdr->src_addr[0], ip_hdr->src_addr[1], ip_hdr->src_addr[2], ip_hdr->src_addr[3],
                                 ip_hdr->src_addr[0], ip_hdr->src_addr[1], ip_hdr->src_addr[2], ip_hdr->src_addr[3],
                                 ip_hdr->ttl,
                                 ip_hdr->version);

    if (bytes_written < 0 || bytes_written >= JSON_BUFFER_SIZE) {
        fprintf(stderr, "Error: IPv4 JSON truncated or formatting failed\n");
        return NULL;
    }

    return json_buffer;
}


void ipv4_layer_free(layer_t *layer) {
    if (!layer) return;

    // Free only the parsed data if it was dynamically allocated
    if (layer->parsed_data) {
        free(layer->parsed_data);
        layer->parsed_data = NULL;
    }

    // Reset other fields if necessary
    layer->protocol_name = NULL;
    layer->to_json = NULL;
    layer->dissect = NULL;

    // Note: We don't free the layer itself or handle next_layer
}


