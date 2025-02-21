//
// Created by Jochen van Waasen on 23.01.25.
//

#ifndef IPV6_LAYER_H
#define IPV6_LAYER_H

#include <packet.h>

#include "layer.h"
#include <stdint.h>
#include <stddef.h>

// IPv6 header structure
typedef struct ipv6_header {
    uint32_t version_traffic_class_flow_label; // Version (4 bits), Traffic Class (8 bits), Flow Label (20 bits)
    uint16_t payload_length;  // Length of payload, including extension headers
    uint8_t next_header;      // Next header type (TCP=6, UDP=17, ICMPv6=58, etc.)
    uint8_t hop_limit;        // Similar to TTL in IPv4
    uint8_t src[16];          // IPv6 source address (128-bit)
    uint8_t dst[16];          // IPv6 destination address (128-bit)
} ipv6_header_t;

// Function to dissect IPv6 layer
int dissect_ipv6(layer_t* layer, packet_t *packet, const uint8_t* data, size_t len);
char* ipv6_to_json(layer_t* layer);
void ipv6_layer_free(layer_t* layer);

#endif // IPV6_LAYER_H

