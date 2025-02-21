//
// Created by Jochen van Waasen on 23.01.25.
//

#ifndef FDDI_LAYER_H
#define FDDI_LAYER_H

#include <packet.h>
#include <stdint.h>
#include <stddef.h>
#include "ids-provider/pcapdissector/layer.h"

// Structure for parsed FDDI header
typedef struct {
    uint8_t frame_control;
    uint8_t dest_mac[6];
    uint8_t src_mac[6];
} fddi_header_t;

// Function to dissect FDDI layer
int dissect_fddi(layer_t* layer, packet_t* packet, const uint8_t* data, size_t len);

#endif // FDDI_LAYER_H

