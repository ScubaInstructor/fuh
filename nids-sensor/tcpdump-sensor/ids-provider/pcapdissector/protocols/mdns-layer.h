#ifndef MDNS_LAYER_H
#define MDNS_LAYER_H

#include "layer.h"
#include "packet.h"

#define MDNS_HEADER_LEN 12

typedef struct {
    uint16_t transaction_id;
    uint16_t flags;
    uint16_t questions;
    uint16_t answer_rrs;
    uint16_t authority_rrs;
    uint16_t additional_rrs;
    // Additional fields for parsed records could be added here
} mdns_header_t;

int dissect_mdns(layer_t *layer, packet_t *packet, const uint8_t *data, size_t len);
char *mdns_to_json(layer_t *layer);
void mdns_layer_free(layer_t *layer);

#endif // MDNS_LAYER_H
