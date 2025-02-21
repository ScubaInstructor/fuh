//
// Created by Jochen van Waasen on 23.01.25.
//

#ifndef ICMP_LAYER_H
#define ICMP_LAYER_H

#include <ids-provider/pcapdissector/layer.h>
#include <packet.h>
#include <stdint.h>
#include <stddef.h>

// ICMP header structure
typedef struct {
    uint8_t type;              // Type of the ICMP message
    uint8_t code;              // Code for the ICMP message
    uint16_t checksum;         // Checksum of the ICMP message
    uint16_t identifier;       // Identifier (e.g., for Echo Request/Reply)
    uint16_t sequence_number;  // Sequence number (e.g., for Echo Request/Reply)
    uint32_t gateway_address;  // Gateway address (used in Redirect messages)
    uint32_t unused;           // Unused field for some message types
    uint32_t original_data[4]; // Part of the original IP header (e.g., for Time Exceeded)
} icmp_header_t;


// Function to dissect ICMP layer
int dissect_icmp(layer_t* layer, packet_t *packet, const uint8_t* data, size_t len);
char* icmp_to_json(layer_t* layer);
void icmp_layer_free(layer_t* layer);

#endif // ICMP_LAYER_H

