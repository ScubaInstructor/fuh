#ifndef NTP_LAYER_H
#define NTP_LAYER_H

#include <packet.h>
#include <stdint.h>
#include <stdlib.h>
#include "../layer.h"

typedef struct ntp_header {
    uint8_t li_vn_mode;
    uint8_t stratum;
    uint8_t poll;
    uint8_t precision;
    uint32_t root_delay;
    uint32_t root_dispersion;
    uint32_t reference_id;
    uint64_t reference_timestamp;
    uint64_t origin_timestamp;
    uint64_t receive_timestamp;
    uint64_t transmit_timestamp;
} ntp_header_t;

int dissect_ntp(layer_t* layer, packet_t* packet, const uint8_t* data, size_t len);
char* ntp_to_json(layer_t* layer);
void ntp_layer_free(layer_t* layer);

#endif // NTP_LAYER_H
