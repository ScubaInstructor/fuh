//
// Created by Jochen van Waasen on 23.01.25.
//

#ifndef ARP_LAYER_H
#define ARP_LAYER_H

#include <packet.h>
#include "layer.h"

#include <stdint.h>
#include <stddef.h>

// ARP header structure
typedef struct arp_header {
    uint16_t hardware_type;      // Hardware type (e.g., Ethernet)
    uint16_t protocol_type;      // Protocol type (e.g., IPv4)
    uint8_t hardware_size;       // Hardware address size (e.g., 6 for MAC)
    uint8_t protocol_size;       // Protocol address size (e.g., 4 for IPv4)
    uint16_t opcode;             // ARP opcode (1: request, 2: reply, etc.)
    uint8_t sender_mac[6];       // Sender MAC address
    uint8_t sender_ip[4];        // Sender IP address
    uint8_t target_mac[6];       // Target MAC address
    uint8_t target_ip[4];        // Target IP address
} arp_header_t;

// Function to dissect ARP layer
int dissect_arp(layer_t* layer, packet_t *packet, const uint8_t* data, size_t len);
char* arp_to_json(layer_t* layer);
void arp_layer_free(layer_t* layer);

#endif // ARP_LAYER_H
