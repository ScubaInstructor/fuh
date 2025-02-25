//
// Created by Jochen van Waasen on 26.01.25.
//

#ifndef LLC_LAYER_H
#define LLC_LAYER_H

#include "layer.h"

typedef struct {
    uint8_t dsap;
    uint8_t ssap;
    uint8_t control;
    uint16_t oui;
    uint16_t pid;
    uint8_t protocol;
} llc_header_t;

int dissect_llc(layer_t* layer, packet_t *packet, const uint8_t* data, size_t len);
char* llc_to_json(layer_t* layer);
void llc_layer_free(layer_t* layer);

#endif // LLC_LAYER_H

