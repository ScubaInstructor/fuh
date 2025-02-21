#ifndef WIFI_LAYER_H
#define WIFI_LAYER_H

#include <packet.h>
#include <stdint.h>
#include "layer.h"

// Wi-Fi Header Structure
typedef struct wifi_header {
    uint16_t frame_control; // Frame Control Field
    uint16_t duration_id;   // Duration/ID
    uint8_t addr1[6];       // Receiver MAC Address
    uint8_t addr2[6];       // Transmitter MAC Address
    uint8_t addr3[6];       // Destination MAC Address
    uint16_t seq_ctrl;      // Sequence Control
    uint8_t addr4[6];       // Fourth MAC Address (optional, for WDS)
    uint8_t has_addr4;      // Flag: 1 if addr4 is present, 0 otherwise
} wifi_header_t;

// Function to dissect Wi-Fi frames
int dissect_wifi(layer_t* layer, packet_t* packet, const uint8_t* data, size_t len);
char* wifi_to_json(layer_t* layer);
void wifi_layer_free(layer_t* layer);

#endif // WIFI_LAYER_H
