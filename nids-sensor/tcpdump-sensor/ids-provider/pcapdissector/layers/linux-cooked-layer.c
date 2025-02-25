//
// Created by Jochen van Waasen on 23.01.25.
//
#include "linux-cooked-layer.h"
#include <stdlib.h>
#include <string.h>
#include <stdio.h>

int dissect_linux_cooked(layer_t* layer, packet_t* packet, const uint8_t* data, size_t len) {
    if (len < 16) { // Linux Cooked header is 16 bytes
        fprintf(stderr, "Insufficient data for Linux Cooked dissection\n");
        return 0;
    }

    linux_cooked_layer_t* cooked = (linux_cooked_layer_t*)malloc(sizeof(linux_cooked_layer_t));
    if (!cooked) {
        fprintf(stderr, "Failed to allocate memory for Linux Cooked layer\n");
        return 0;
    }

    cooked->packet_type = (data[0] << 8) | data[1];
    cooked->protocol = (data[2] << 8) | data[3];
    cooked->len = len - 16;
    cooked->data = (uint8_t*)malloc(cooked->len);
    if (!cooked->data) {
        free(cooked);
        fprintf(stderr, "Failed to allocate memory for Linux Cooked payload\n");
        return 0;
    }

    memcpy(cooked->data, data + 16, cooked->len);
    layer->parsed_data = cooked;

    return 1;
}
