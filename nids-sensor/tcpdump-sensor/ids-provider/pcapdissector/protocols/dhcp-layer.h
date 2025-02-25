#ifndef DHCP_LAYER_H
#define DHCP_LAYER_H

#include <packet.h>
#include <stdint.h>
#include <stdlib.h>
#include "layer.h"

typedef struct dhcp_options {
    uint8_t subnet_mask[4];
    uint8_t router[4];
    uint8_t dns[4];
    uint32_t lease_time;
    uint8_t message_type;
    uint8_t server_id[4];
    // Add more fields as needed for other DHCP options
} dhcp_options_t;

typedef struct dhcp_header {
    uint8_t op;
    uint8_t htype;
    uint8_t hlen;
    uint8_t hops;
    uint32_t xid;
    uint16_t secs;
    uint16_t flags;
    uint32_t ciaddr;
    uint32_t yiaddr;
    uint32_t siaddr;
    uint32_t giaddr;
    uint8_t chaddr[16];
    char sname[64];
    char file[128];
    dhcp_options_t* options;
} dhcp_header_t;

int dissect_dhcp(layer_t* layer, packet_t* packet, const uint8_t* data, size_t len);
char* dhcp_to_json(layer_t* layer);
void dhcp_layer_free(layer_t* layer);

#endif // DHCP_LAYER_H
