//
// Created by Jochen van Waasen on 23.01.25.
//

#ifndef PPPOE_LAYER_H
#define PPPOE_LAYER_H

#include <packet.h>
#include <stdint.h>
#include <stddef.h>
#include "layer.h"

#define PPPOE_HEADER_LEN 6 // Minimum PPPoE header length

// PPPoE Header structure
typedef struct pppoe_header {
    uint8_t version_type;     // Version and Type fields combined
    uint8_t code;             // PPPoE code
    uint16_t session_id;      // Session ID
    uint16_t payload_length;  // Length of the payload
    uint8_t* payload;         // Pointer to payload data (if parsed)
} pppoe_header_t;

// Function to dissect PPPoE layer
int dissect_pppoe(layer_t* layer, packet_t *packet, const uint8_t* data, size_t len);
char *pppoe_to_json(layer_t *layer);
void pppoe_layer_free(layer_t *layer);

#endif // PPPOE_LAYER_H


