//
// Created by Jochen van Waasen on 23.01.25.
//

#include "raw-ip-layer.h"
#include <stdlib.h>
#include <string.h>
#include <stdio.h>

int dissect_raw_ip(layer_t* layer, packet_t* packet, const uint8_t* data, size_t len) {
    if (!layer || !data || len == 0) {
        fprintf(stderr, "Invalid arguments to dissect_raw_ip\n");
        return 0;
    }

    raw_ip_layer_t* raw_ip = (raw_ip_layer_t*)malloc(sizeof(raw_ip_layer_t));
    if (!raw_ip) {
        fprintf(stderr, "Failed to allocate memory for Raw IP layer\n");
        return 0;
    }

    raw_ip->data = (uint8_t*)malloc(len);
    if (!raw_ip->data) {
        free(raw_ip);
        fprintf(stderr, "Failed to allocate memory for Raw IP data\n");
        return 0;
    }

    memcpy(raw_ip->data, data, len);
    raw_ip->len = len;

    layer->parsed_data = raw_ip;

    return 1;
}

