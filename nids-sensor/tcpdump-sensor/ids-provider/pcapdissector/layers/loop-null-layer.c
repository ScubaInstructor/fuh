//
// Created by Jochen van Waasen on 23.01.25.
//
#include "ids-provider/common-util.h"
#include "loop-null-layer.h"
#include <stdlib.h>
#include <string.h>
#include <stdio.h>

int dissect_loop_null(layer_t* layer, packet_t *packet, const uint8_t* data, size_t len) {
    if (!layer || !data || len < 4) {
        fprintf(stderr, "Insufficient data for Loop/Null dissection\n");
        return 0;
    }

    loop_null_header_t* header = (loop_null_header_t*)malloc(sizeof(loop_null_header_t));
    if (!header) {
        fprintf(stderr, "Failed to allocate memory for Loop/Null header\n");
        return 0;
    }

    // Parse the family field (first 4 bytes)
    header->family = ntohl(*(uint32_t*)data);
    layer->parsed_data = header;

    const uint8_t* payload = data + 4;
    size_t payload_len = len - 4;


    // Use the process_next_layer utility function
    return process_next_layer(packet, header->family, payload, payload_len, handlers);
}


