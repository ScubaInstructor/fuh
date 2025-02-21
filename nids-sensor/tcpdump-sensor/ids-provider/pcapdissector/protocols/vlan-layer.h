//
// Created by Jochen van Waasen on 23.01.25.
//

#ifndef VLAN_LAYER_H
#define VLAN_LAYER_H

#include <packet.h>

#include "layer.h"
#include <stdint.h>
#include <stddef.h>

typedef struct vlan_header {
    uint16_t tci;       // Tag Control Information (PCP, DEI, VLAN ID)
    uint16_t ethertype; // Encapsulated protocol
    uint8_t pcp;        // Priority Code Point (3 bits)
    uint8_t dei;        // Drop Eligible Indicator (1 bit)
    uint16_t vlan_id;   // VLAN Identifier (12 bits)
} vlan_header_t;

// Function to dissect VLAN layer
int dissect_vlan(layer_t* layer, packet_t *packet, const uint8_t* data, size_t len);
char* vlan_to_json(layer_t* layer);
void vlan_layer_free(layer_t* layer);

#endif // VLAN_LAYER_H

