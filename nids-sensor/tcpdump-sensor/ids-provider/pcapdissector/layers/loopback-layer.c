//
// Created by Jochen van Waasen on 23.01.25.
//

#include "loopback-layer.h"
#include <stdlib.h>
#include <string.h>
#include <stdio.h>

int dissect_loop(layer_t* layer, packet_t* packet, const uint8_t* data, size_t len) {
    if (len < 4) { // Loopback header is 4 bytes
        fprintf(stderr, "Insufficient data for Loopback dissection\n");
        return 0;
    }

    loopback_layer_t* loop = (loopback_layer_t*)malloc(sizeof(loopback_layer_t));
    if (!loop) {
        fprintf(stderr, "Failed to allocate memory for Loopback layer\n");
        return 0;
    }

    loop->family = (data[0] << 24) | (data[1] << 16) | (data[2] << 8) | data[3];
    layer->parsed_data = loop;

    return 1;
}

