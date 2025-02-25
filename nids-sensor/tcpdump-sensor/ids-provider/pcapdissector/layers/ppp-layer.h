//
// Created by Jochen van Waasen on 23.01.25.
//

#ifndef PPP_LAYER_H
#define PPP_LAYER_H

#include <packet.h>
#include <stdint.h>
#include <stddef.h>
#include "ids-provider/pcapdissector/layer.h"

typedef struct ppp_layer {
    uint16_t protocol; // PPP protocol type
    uint8_t* data;     // Encapsulated payload
    size_t len;        // Length of encapsulated payload
} ppp_layer_t;

// Function to dissect PPP layer
int dissect_ppp(layer_t* layer, packet_t* packet, const uint8_t* data, size_t len);

#endif // PPP_LAYER_H

