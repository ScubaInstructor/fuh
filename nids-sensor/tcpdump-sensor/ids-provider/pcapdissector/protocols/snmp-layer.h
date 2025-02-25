//
// Created by Jochen van Waasen on 29.01.25.
//

#ifndef SNMP_LAYER_H
#define SNMP_LAYER_H
#include <layer.h>
#include <packet.h>
#include <stdint.h>

typedef struct snmp_header {
    uint8_t version;
    char community[64]; // Assume max length of 64
    uint8_t pdu_type;
} snmp_header_t;

int dissect_snmp(layer_t* layer, packet_t* packet, const uint8_t* data, size_t len);
char* snmp_to_json(layer_t* layer);
void snmp_layer_free(layer_t* layer);


#endif //SNMP_LAYER_H
