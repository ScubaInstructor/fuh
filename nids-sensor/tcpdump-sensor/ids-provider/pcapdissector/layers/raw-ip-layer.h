//
// Created by Jochen van Waasen on 23.01.25.
//

#ifndef RAW_IP_LAYER_H
#define RAW_IP_LAYER_H

#include <ids-provider/pcapdissector/layer.h>
#include <packet.h>
#include <stdint.h>
#include <stddef.h>

typedef struct raw_ip_layer {
    uint8_t* data;   // Pointer to the raw IP data
    size_t len;      // Length of the raw IP data
} raw_ip_layer_t;

// Function to dissect Raw IP layer
int dissect_raw_ip(layer_t* layer, packet_t* packet, const uint8_t* data, size_t len);

#endif // RAW_IP_LAYER_H

