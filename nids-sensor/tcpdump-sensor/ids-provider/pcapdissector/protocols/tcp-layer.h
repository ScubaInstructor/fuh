//
// Created by Jochen van Waasen on 23.01.25.
//

#ifndef TCP_LAYER_H
#define TCP_LAYER_H

#include <packet.h>
#include <stdint.h>
#include <stddef.h>
#include <ids-provider/pcapdissector/layer.h>

// TCP header structure
typedef struct {
    uint16_t src_port;
    uint16_t dst_port;
    uint32_t seq_num;
    uint32_t ack_num;
    uint8_t data_offset;
    uint8_t flags;
    uint16_t window_size;
    uint16_t checksum;
    uint16_t urgent_pointer;
    uint8_t* options;
    size_t options_len;
    // New fields
    uint32_t payload_length;
    uint32_t header_length;
    uint32_t tcp_stream;
    uint32_t tcp_len;
    uint32_t nxtseq;
    char* tcp_analysis;
    double time_relative;
    double time_delta;
} tcp_header_t;


// Function to dissect TCP layer
int dissect_tcp(layer_t* layer, packet_t *packet, const uint8_t* data, size_t len);
char* tcp_to_json(layer_t* layer);
void tcp_layer_free(layer_t* layer);

#endif // TCP_LAYER_H
