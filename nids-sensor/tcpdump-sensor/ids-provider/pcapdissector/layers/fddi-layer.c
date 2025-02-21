//
// Created by Jochen van Waasen on 23.01.25.
//

#include "fddi-layer.h"
#include <stdlib.h>
#include <string.h>
#include <stdio.h>

int dissect_fddi(layer_t* layer, packet_t* packet, const uint8_t* data, size_t len) {
    if (len < 13) { // FDDI header is 13 bytes
        fprintf(stderr, "Insufficient data for FDDI dissection\n");
        return 0;
    }

    fddi_header_t* header = (fddi_header_t*)malloc(sizeof(fddi_header_t));
    if (!header) {
        fprintf(stderr, "Failed to allocate memory for FDDI header\n");
        return 0;
    }

    header->frame_control = data[0];
    memcpy(header->dest_mac, data + 1, 6);
    memcpy(header->src_mac, data + 7, 6);

    layer->parsed_data = header;

    return 1; // Further dissection of payload can be added
}

