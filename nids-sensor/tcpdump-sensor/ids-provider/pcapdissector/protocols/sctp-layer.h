//
// Created by Jochen van Waasen on 25.01.25.
//

#ifndef SCTP_LAYER_H
#define SCTP_LAYER_H

#include <packet.h>
#include <stdint.h>
#include <stddef.h>
#include "layer.h"

#define SCTP_COMMON_HEADER_LENGTH 12

typedef struct {
    uint8_t type;
    uint8_t flags;
    uint16_t length;
    uint8_t *data;
} sctp_chunk_t;

typedef struct {
    uint16_t src_port;
    uint16_t dst_port;
    uint32_t verification_tag;
    uint32_t checksum;
    uint32_t chunk_count;
    sctp_chunk_t **chunks;
} sctp_header_t;

int dissect_sctp(layer_t* layer,  packet_t *packet, const uint8_t* data, size_t len);
char* sctp_to_json(layer_t* layer);
void sctp_layer_free(layer_t* layer);

#endif // SCTP_LAYER_H

