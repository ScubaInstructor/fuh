//
// Created by Jochen van Waasen on 23.01.25.
//

#ifndef LOOP_NULL_LAYER_H
#define LOOP_NULL_LAYER_H

#include "ids-provider/pcapdissector/layer.h"
#include <packet.h>
#include <stdint.h>
#include <stddef.h>


// Structure for parsed Loop/Null Layer
typedef struct {
    uint32_t family; // Address family (e.g., AF_INET, AF_INET6)
} loop_null_header_t;

// Function to dissect Loop/Null layer
int dissect_loop_null(layer_t* layer, packet_t *packet, const uint8_t* data, size_t len);

#endif // LOOP_NULL_LAYER_H

