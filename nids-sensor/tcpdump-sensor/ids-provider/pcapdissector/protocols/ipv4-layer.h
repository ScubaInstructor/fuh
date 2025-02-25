//
// Created by Jochen van Waasen on 23.01.25.
//
#ifndef IPV4_LAYER_H
#define IPV4_LAYER_H

#include <packet.h>
#include <stdint.h>
#include <stddef.h>
#include <ids-provider/pcapdissector/layer.h>


// IPv4 header structure
typedef struct ipv4_header {
    uint8_t version;           // IP version
    uint8_t ihl;               // Internet Header Length
    uint8_t dscp;              // Differentiated Services Code Point
    uint8_t ecn;               // Explicit Congestion Notification
    uint16_t total_length;     // Total length of the packet
    uint16_t identification;   // Identification
    uint8_t flags;             // Flags (3 bits)
    uint16_t fragment_offset;  // Fragment offset (13 bits)
    uint8_t ttl;               // Time to live
    uint8_t protocol;          // Protocol (e.g., TCP=6, UDP=17, ICMP=1)
    uint16_t header_checksum;  // Header checksum
    uint8_t src_addr[4];       // Source IP address
    uint8_t dst_addr[4];       // Destination IP address
} ipv4_header_t;

// Function to dissect IPv4 layer
int dissect_ipv4(layer_t* layer, packet_t *packet, const uint8_t* data, size_t len);
char* ipv4_to_json(layer_t* layer);
void ipv4_layer_free(layer_t* layer);

#endif // IPV4_LAYER_H
