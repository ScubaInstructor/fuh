#ifndef UDP_PORT_CUSTOM_H
#define UDP_PORT_CUSTOM_H

#include "layer.h"
#include <packet.h>

typedef struct {
    uint16_t src_port;
    uint16_t dst_port;
    uint16_t length;
    uint16_t checksum;
    size_t payload_length;
} udp_port_custom_header_t;

int dissect_udp_port_custom(layer_t *layer, packet_t *packet, const uint8_t *data, size_t len);
char *udp_port_custom_to_json(layer_t *layer);
void udp_port_custom_layer_free(layer_t *layer);

#endif // UDP_PORT_CUSTOM_H
