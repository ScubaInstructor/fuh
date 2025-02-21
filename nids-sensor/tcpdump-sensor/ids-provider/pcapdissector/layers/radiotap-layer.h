//
// Created by Jochen van Waasen on 23.01.25.
//

#ifndef RADIOTAP_LAYER_H
#define RADIOTAP_LAYER_H

#include <packet.h>
#include <stdint.h>
#include <stddef.h>
#include "ids-provider/pcapdissector/layer.h"

// Structure for parsed Radiotap header
typedef struct {
    uint8_t version;
    uint8_t pad;
    uint16_t length;
    uint32_t present_flags;
} radiotap_header_t;

// Function to dissect Radiotap layer
int dissect_radiotap(layer_t* layer, packet_t* packet, const uint8_t* data, size_t len);

#endif // RADIOTAP_LAYER_H

