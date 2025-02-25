//
// Created by Jochen van Waasen on 28.01.25.
//

#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <arpa/inet.h>
#include "icmpv6-layer.h"

int dissect_icmpv6(layer_t* layer, packet_t* packet, const uint8_t* data, size_t len) {
    if (len < sizeof(icmpv6_header_t)) {
        fprintf(stderr, "Insufficient data for ICMPv6 dissection\n");
        return 1;
    }

    // Allocate memory for the ICMPv6 header
    icmpv6_header_t* icmp_hdr = (icmpv6_header_t*)malloc(sizeof(icmpv6_header_t));
    if (!icmp_hdr) {
        fprintf(stderr, "Failed to allocate memory for ICMPv6 header\n");
        return 1;
    }

    // Parse ICMPv6 header fields
    icmp_hdr->type = data[0];
    icmp_hdr->code = data[1];
    icmp_hdr->checksum = ntohs(*(uint16_t*)(data + 2));
    icmp_hdr->reserved = len >= 8 ? ntohl(*(uint32_t*)(data + 4)) : 0;

    // Store the ICMPv6 header in the layer
    layer->parsed_data = icmp_hdr;
    layer->to_json = icmpv6_to_json;

    // Check ICMPv6 type to decide further dissection
    switch (icmp_hdr->type) {
        case 128: // Echo Request
        case 129: // Echo Reply
            fprintf(stderr, "ICMPv6 Echo Request/Reply detected\n");
            break;
        case 133: // Router Solicitation
        case 134: // Router Advertisement
        case 135: // Neighbor Solicitation
        case 136: // Neighbor Advertisement
            fprintf(stderr, "ICMPv6 Neighbor Discovery message detected\n");
            break;
        default:
            fprintf(stderr, "Unknown ICMPv6 type: %u\n", icmp_hdr->type);
            break;
    }

    return 1; // Successful dissection
}

#define JSON_BUFFER_SIZE 1024
static _Thread_local  char json_buffer[JSON_BUFFER_SIZE];
char* icmpv6_to_json(layer_t* layer) {
    if (!layer || !layer->parsed_data) {
        return NULL; // Return NULL if the layer or parsed data is missing
    }

    icmpv6_header_t* icmp_hdr = (icmpv6_header_t*)layer->parsed_data;

    // Convert ICMPv6 header fields to JSON
    int bytes_written = snprintf(json_buffer, JSON_BUFFER_SIZE,
             "\"icmpv6\":{  \"icmpv6.type\": %u, "
             "\"icmpv6.code\": %u, "
             "\"icmpv6.checksum\": \"0x%04X\", "
             "\"icmpv6.reserved\": \"0x%08X\" }",
             icmp_hdr->type,
             icmp_hdr->code,
             icmp_hdr->checksum,
             icmp_hdr->reserved);

    if (bytes_written < 0 || bytes_written >= JSON_BUFFER_SIZE) {
        // Error or truncation occurred
        fprintf(stderr, "Error: ICMPv6 JSON truncated or formatting failed\n");
        return NULL;
    }

    return json_buffer;
}


void icmpv6_layer_free(layer_t* layer) {
    if (!layer) return;

    // Free the parsed data (ARP header)
    if (layer->parsed_data) {
        free(layer->parsed_data);
    }
}

