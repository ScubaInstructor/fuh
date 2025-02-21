//
// Created by Jochen van Waasen on 23.01.25.
//
#ifndef UDP_LAYER_H
#define UDP_LAYER_H

#include <ids-provider/pcapdissector/layer.h>
#include <packet.h>
#include <stdint.h>
#include <stddef.h>


// UDP header structure
typedef struct {
    uint16_t src_port;
    uint16_t dst_port;
    uint16_t length;
    uint16_t checksum;
    const char* warning;
    uint32_t stream;
    uint32_t stream_pnum;
    double time_relative;
    double time_delta;
    uint8_t checksum_status;
    const uint8_t* payload;
    size_t payload_len;
    uint32_t src_ip;
    uint32_t dst_ip;
} udp_header_t;

// Function to dissect UDP layer
int dissect_udp(layer_t* layer, packet_t *packet, const uint8_t* data, size_t len);
char* udp_to_json(layer_t* layer);
void udp_layer_free(layer_t* layer);
#endif // UDP_LAYER_H

