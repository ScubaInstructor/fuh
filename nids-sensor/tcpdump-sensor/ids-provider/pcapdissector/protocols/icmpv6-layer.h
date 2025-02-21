//
// Created by Jochen van Waasen on 28.01.25.
//

#ifndef ICMPV6_LAYER_H
#define ICMPV6_LAYER_H

#include <packet.h>
#include <stdint.h>
#include "layer.h"

// ICMPv6 header structure
typedef struct icmpv6_header {
    uint8_t type;         // ICMPv6 message type
    uint8_t code;         // ICMPv6 message code
    uint16_t checksum;    // Checksum
    uint32_t reserved;    // Reserved (used in some messages, optional)
} icmpv6_header_t;

int dissect_icmpv6(layer_t* layer, packet_t* packet, const uint8_t* data, size_t len);
char* icmpv6_to_json(layer_t* layer);
void icmpv6_layer_free(layer_t* layer);

#endif // ICMPV6_LAYER_H

