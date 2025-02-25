//
// Created by Jochen van Waasen on 27.01.25.
//

#ifndef STP_LAYER_H
#define STP_LAYER_H

#include <packet.h>
#include <stdint.h>
#include <stddef.h>
#include <ids-provider/pcapdissector/layer.h>

// STP header structure
typedef struct {
    uint16_t protocol_id;   // Protocol ID (should be 0x0000 for STP)
    uint8_t version;        // Version of the protocol
    uint8_t bpdu_type;      // BPDU Type
    uint8_t flags;          // Flags
    uint64_t root_id;       // Root Bridge Identifier
    uint32_t root_path_cost; // Root Path Cost
    uint64_t bridge_id;     // Bridge Identifier
    uint16_t port_id;       // Port Identifier
    uint16_t message_age;   // Message Age (in 1/256 seconds)
    uint16_t max_age;       // Maximum Age (in 1/256 seconds)
    uint16_t hello_time;    // Hello Time (in 1/256 seconds)
    uint16_t forward_delay; // Forward Delay (in 1/256 seconds)
} stp_header_t;

// Function to dissect STP layer
int dissect_stp(layer_t* layer, packet_t *packet, const uint8_t* data, size_t len);
char* stp_to_json(layer_t* layer);
void stp_layer_free(layer_t* layer);

#endif // STP_LAYER_H

