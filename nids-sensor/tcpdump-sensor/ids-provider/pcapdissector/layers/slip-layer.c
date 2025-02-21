//
// Created by Jochen van Waasen on 23.01.25.
//

#include "slip-layer.h"
#include <stdlib.h>
#include <stdio.h>
#include <string.h>

int dissect_slip(layer_t* layer, packet_t *packet, const uint8_t* data, size_t len) {
    if (!layer || !data || len == 0) {
        fprintf(stderr, "Invalid input to SLIP dissection\n");
        return 0;
    }

    // SLIP decoding logic placeholder
    layer->parsed_data = malloc(len);
    if (!layer->parsed_data) {
        fprintf(stderr, "Failed to allocate memory for SLIP parsed data\n");
        return 0;
    }

    memcpy(layer->parsed_data, data, len);

    return 1; // Further decoding of encapsulated IP can be added
}

