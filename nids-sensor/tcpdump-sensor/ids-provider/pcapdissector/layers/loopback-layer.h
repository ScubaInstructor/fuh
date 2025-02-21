//
// Created by Jochen van Waasen on 23.01.25.
//

#ifndef LOOPBACK_LAYER_H
#define LOOPBACK_LAYER_H

#include <packet.h>
#include <stdint.h>
#include <stddef.h>
#include "ids-provider/pcapdissector/layer.h"

typedef struct loopback_layer {
    uint32_t family; // Address family
} loopback_layer_t;

// Function to dissect Loopback layer
int dissect_loop(layer_t* layer, packet_t* packet, const uint8_t* data, size_t len);

#endif // LOOPBACK_LAYER_H

