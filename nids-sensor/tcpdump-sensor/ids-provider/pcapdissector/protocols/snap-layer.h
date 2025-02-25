//
// Created by Jochen van Waasen on 27.01.25.
//

#ifndef SNAP_LAYER_H
#define SNAP_LAYER_H

#include <packet.h>
#include <stdint.h>
#include <stddef.h>
#include <ids-provider/pcapdissector/layer.h>

// SNAP header structure
typedef struct {
    uint8_t oui[3];       // Organizationally Unique Identifier
    uint16_t ethertype;   // Ethertype
} snap_header_t;

// Function to dissect SNAP layer
int dissect_snap(layer_t* layer, packet_t *packet, const uint8_t* data, size_t len);
char* snap_to_json(layer_t* layer);
void snap_layer_free(layer_t* layer);

#endif // SNAP_LAYER_H

