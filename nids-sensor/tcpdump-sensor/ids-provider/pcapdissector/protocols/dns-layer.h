//
// Created by Jochen van Waasen on 29.01.25.
//

#ifndef DNS_LAYER_H
#define DNS_LAYER_H
#include <layer.h>
#include <packet.h>
#include <stdint.h>

typedef struct dns_header {
    uint16_t transaction_id;
    uint16_t flags;
    uint16_t qd_count;
    uint16_t an_count;
    uint16_t ns_count;
    uint16_t ar_count;
} dns_header_t;

int dissect_dns(layer_t* layer, packet_t* packet, const uint8_t* data, size_t len);
char* dns_to_json(layer_t* layer);
void dns_layer_free(layer_t* layer);


#endif //DNS_LAYER_H
