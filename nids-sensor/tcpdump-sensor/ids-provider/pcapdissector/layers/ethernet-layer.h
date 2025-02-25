//
// Created by Jochen van Waasen on 23.01.25.
//

#ifndef ETHERNET_LAYER_H
#define ETHERNET_LAYER_H

#include <packet.h>
#include <stdint.h>
#include <stddef.h>
#include "ids-provider/pcapdissector/layer.h"

// Ethernet header structure
typedef struct {
    uint8_t dest_mac[6];
    uint8_t src_mac[6];
    uint16_t ethertype;
    uint16_t length;
    uint16_t vlan_id;
    uint8_t vlan_priority;
    uint16_t qinq_id;
    uint8_t qinq_priority;
} ethernet_header_t;


// Function to dissect Ethernet layer
int dissect_ethernet(layer_t *layer, packet_t *packet, const uint8_t *data, size_t len);
char* ethernet_to_json(layer_t* layer);
void ethernet_layer_free(layer_t* layer);
void mac_to_string(const uint8_t mac[6], char out[18]);
uint32_t extract_oui(const uint8_t mac[6]);
const char* lookup_oui_vendor(const uint8_t mac[6]);

#endif // ETHERNET_LAYER_H

