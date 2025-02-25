//
// Created by Jochen van Waasen on 28.01.25.
//

#ifndef SNA_PATH_CONTROL_LAYER_H
#define SNA_PATH_CONTROL_LAYER_H

#include <packet.h>
#include <stdint.h>
#include "layer.h"

// SNA Path Control header structure
typedef struct sna_path_control_header {
    uint8_t command;       // Command byte
    uint16_t routing_info; // Routing information (2 bytes)
    uint8_t payload[];     // Optional payload
} sna_path_control_header_t;


int dissect_sna_path_control(layer_t* layer, packet_t *packet, const uint8_t* data, size_t len);
char* sna_path_control_to_json(layer_t* layer);
void sna_path_control_layer_free(layer_t* layer);

#endif // SNA_PATH_CONTROL_LAYER_H

