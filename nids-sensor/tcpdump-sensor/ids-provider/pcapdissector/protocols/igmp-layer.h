//
// Created by Jochen van Waasen on 25.01.25.
//

#ifndef IGMP_LAYER_H
#define IGMP_LAYER_H

#include <packet.h>
#include <stdint.h>
#include <stddef.h>
#include "layer.h"

// IGMP Header structure
typedef struct {
    uint8_t type;                     // IGMP message type (e.g., 0x11 for Query, 0x22 for Report)
    uint8_t max_resp_time;            // Maximum response time in 1/10th of a second
    uint16_t checksum;                // Header checksum
    uint8_t group_address[4];         // Multicast group address
    uint8_t reserved;                 // Reserved field (specific to IGMPv3)
    uint8_t s_flag;                   // Suppress Router-Side Processing (specific to IGMPv3)
    uint8_t qrv;                      // Querier's Robustness Variable (specific to IGMPv3)
    uint8_t qqic;                     // Querier's Query Interval Code (specific to IGMPv3)
    size_t num_source_addresses;      // Number of source addresses in the message
    uint8_t (*source_addresses)[4];   // Pointer to an array of source addresses (each 4 bytes)
} igmp_header_t;

int dissect_igmp(layer_t* layer, packet_t *packet, const uint8_t* data, size_t len);
char* igmp_to_json(layer_t* layer);
void igmp_layer_free(layer_t* layer);

#endif // IGMP_LAYER_H

