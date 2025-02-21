//
// Created by Jochen van Waasen on 23.01.25.
//

#include "ppp-layer.h"
#include <stdlib.h>
#include <string.h>
#include <stdio.h>

int dissect_ppp(layer_t* layer, packet_t* packet, const uint8_t* data, size_t len) {
    if (len < 2) { // PPP header is at least 2 bytes
        fprintf(stderr, "Insufficient data for PPP dissection\n");
        return 0;
    }

    ppp_layer_t* ppp = (ppp_layer_t*)malloc(sizeof(ppp_layer_t));
    if (!ppp) {
        fprintf(stderr, "Failed to allocate memory for PPP layer\n");
        return 0;
    }

    ppp->protocol = (data[0] << 8) | data[1];
    ppp->len = len - 2;
    ppp->data = (uint8_t*)malloc(ppp->len);
    if (!ppp->data) {
        free(ppp);
        fprintf(stderr, "Failed to allocate memory for PPP payload\n");
        return 0;
    }

    memcpy(ppp->data, data + 2, ppp->len);
    layer->parsed_data = ppp;

    return 1;
}

