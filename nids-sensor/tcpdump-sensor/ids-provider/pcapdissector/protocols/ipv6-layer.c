//
// Created by Jochen van Waasen on 23.01.25.
//
#include "ids-provider/common-util.h"
#include "ipv6-layer.h"
#include <stdlib.h>
#include <string.h>
#include <stdio.h>
#include <tcp-layer.h>
#include <udp-layer.h>


#include "icmpv6-layer.h"

int dissect_ipv6(layer_t* layer, packet_t *packet, const uint8_t* data, size_t len) {
    if (len < 40) { // Minimum IPv6 header size
        fprintf(stderr, "Insufficient data for IPv6 dissection\n");
        return 1;
    }

    ipv6_header_t* ip_hdr = (ipv6_header_t*)malloc(sizeof(ipv6_header_t));
    if (!ip_hdr) {
        fprintf(stderr, "Failed to allocate memory for IPv6 header\n");
        return 1;
    }

    // Parse the IPv6 header
    memcpy(ip_hdr, data, 40);

    // Store parsed data
    layer->parsed_data = ip_hdr;

    // Determine the next protocol
    uint8_t next_header = ip_hdr->next_header;
    const uint8_t* payload = data + 40;
    size_t payload_len = len - 40;

    // Handle IPv6 Extension Headers
    while (next_header == 0 || next_header == 43 || next_header == 60) { // Hop-by-Hop, Routing, Destination Options
        fprintf(stderr, "IPv6 Extension Header detected (Next Header: %d). Skipping...\n", next_header);
        if (payload_len < 8) {
            fprintf(stderr, "Insufficient data for IPv6 extension header\n");
            free(ip_hdr);
            return 1;
        }
        next_header = payload[0]; // Get next header from extension header
        size_t ext_header_len = (payload[1] + 1) * 8;
        payload += ext_header_len;
        payload_len -= ext_header_len;
    }

    // Use the process_next_layer utility function
    return process_next_layer(packet, next_header, payload, payload_len, handlers);
}

void ipv6_layer_free(layer_t *layer) {
    if (layer && layer->parsed_data) {
        free(layer->parsed_data);
        layer->parsed_data = NULL;
    }
}





