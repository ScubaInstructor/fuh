//
// Created by Jochen van Waasen on 23.01.25.
//

#include "radiotap-layer.h"
#include <stdlib.h>
#include <string.h>
#include <stdio.h>
#include <netinet/in.h> // For htons/ntohs

int dissect_radiotap(layer_t* layer, packet_t* packet, const uint8_t* data, size_t len) {
    if (len < 8) { // Radiotap header is at least 8 bytes
        fprintf(stderr, "Insufficient data for Radiotap dissection\n");
        return 0;
    }

    radiotap_header_t* header = (radiotap_header_t*)malloc(sizeof(radiotap_header_t));
    if (!header) {
        fprintf(stderr, "Failed to allocate memory for Radiotap header\n");
        return 0;
    }

    header->version = data[0];
    header->pad = data[1];
    header->length = ntohs(*(uint16_t*)(data + 2));
    header->present_flags = ntohl(*(uint32_t*)(data + 4));

    layer->parsed_data = header;
    layer->protocol_name = "Wi-Fi Radiotap";

    return 1; // Additional processing of fields can be added
}

