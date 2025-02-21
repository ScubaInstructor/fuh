//
// Created by Jochen van Waasen on 23.01.25.
//

#ifndef LINUX_COOKED_LAYER_H
#define LINUX_COOKED_LAYER_H

#include <packet.h>
#include <stdint.h>
#include <stddef.h>
#include <ids-provider/pcapdissector/layer.h>

typedef struct linux_cooked_layer {
    uint16_t packet_type;  // Packet type (e.g., Unicast, Broadcast)
    uint16_t protocol;     // Protocol type (e.g., IPv4, ARP)
    uint8_t* data;         // Pointer to the encapsulated data
    size_t len;            // Length of the encapsulated data
} linux_cooked_layer_t;

// Function to dissect Linux Cooked layer
int dissect_linux_cooked(layer_t* layer, packet_t* packet, const uint8_t* data, size_t len);

#endif // LINUX_COOKED_LAYER_H

