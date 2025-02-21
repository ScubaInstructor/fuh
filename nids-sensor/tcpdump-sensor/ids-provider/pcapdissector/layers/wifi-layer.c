//
// Created by Jochen van Waasen on 23.01.25.
//

#include "wifi-layer.h"

#include <stdlib.h>
#include <string.h>
#include <stdio.h>

int dissect_wifi(layer_t* layer, packet_t* packet, const uint8_t* data, size_t len) {
    if (len < 24) { // Minimum size for Wi-Fi header
        fprintf(stderr, "Insufficient data for Wi-Fi dissection\n");
        return 0;
    }

    wifi_header_t* wifi_hdr = (wifi_header_t*)malloc(sizeof(wifi_header_t));
    if (!wifi_hdr) {
        fprintf(stderr, "Failed to allocate memory for Wi-Fi header\n");
        return 0;
    }

    // Parse the fixed Wi-Fi header fields
    wifi_hdr->frame_control = (data[0] << 8) | data[1];
    wifi_hdr->duration_id = (data[2] << 8) | data[3];
    memcpy(wifi_hdr->addr1, &data[4], 6);
    memcpy(wifi_hdr->addr2, &data[10], 6);
    memcpy(wifi_hdr->addr3, &data[16], 6);
    wifi_hdr->seq_ctrl = (data[22] << 8) | data[23];
    wifi_hdr->has_addr4 = 0; // Default: No Address 4

    // Check if Address 4 exists (WDS frames)
    const uint8_t* payload = data + 24;
    size_t payload_len = len - 24;
    if ((wifi_hdr->frame_control & 0x03) == 0x03) { // Check for WDS frame
        if (payload_len < 6) {
            fprintf(stderr, "Insufficient data for WDS Address 4\n");
            free(wifi_hdr);
            return 0;
        }
        memcpy(wifi_hdr->addr4, payload, 6);
        wifi_hdr->has_addr4 = 1; // Indicate that Address 4 is present
        payload += 6;
        payload_len -= 6;
    }

    // Store the parsed Wi-Fi header in the layer
    layer->parsed_data = wifi_hdr;

    return 1; // Dissection successful
}

char* wifi_to_json(layer_t* layer) {
    if (!layer || !layer->parsed_data) return NULL;

    wifi_header_t* wifi_hdr = (wifi_header_t*)layer->parsed_data;

    // Allocate memory for JSON output
    char* json = (char*)malloc(1024);
    if (!json) return NULL;

    // Format the JSON output, including Address 4 only if present
    if (wifi_hdr->has_addr4) {
        snprintf(json, 1024,
                 "\"wifi\": {"
                 "\"wifi.frame_control\": \"0x%04X\","
                 "\"wifi.duration_id\": \"%u\","
                 "\"wifi.addr1\": \"%02X:%02X:%02X:%02X:%02X:%02X\","
                 "\"wifi.addr2\": \"%02X:%02X:%02X:%02X:%02X:%02X\","
                 "\"wifi.addr3\": \"%02X:%02X:%02X:%02X:%02X:%02X\","
                 "\"wifi.addr4\": \"%02X:%02X:%02X:%02X:%02X:%02X\","
                 "\"wifi.seq_ctrl\": \"%u\""
                 "}",
                 wifi_hdr->frame_control,
                 wifi_hdr->duration_id,
                 wifi_hdr->addr1[0], wifi_hdr->addr1[1], wifi_hdr->addr1[2],
                 wifi_hdr->addr1[3], wifi_hdr->addr1[4], wifi_hdr->addr1[5],
                 wifi_hdr->addr2[0], wifi_hdr->addr2[1], wifi_hdr->addr2[2],
                 wifi_hdr->addr2[3], wifi_hdr->addr2[4], wifi_hdr->addr2[5],
                 wifi_hdr->addr3[0], wifi_hdr->addr3[1], wifi_hdr->addr3[2],
                 wifi_hdr->addr3[3], wifi_hdr->addr3[4], wifi_hdr->addr3[5],
                 wifi_hdr->addr4[0], wifi_hdr->addr4[1], wifi_hdr->addr4[2],
                 wifi_hdr->addr4[3], wifi_hdr->addr4[4], wifi_hdr->addr4[5],
                 wifi_hdr->seq_ctrl);
    } else {
        snprintf(json, 1024,
                 "\"wifi\": {"
                 "\"wifi.frame_control\": \"0x%04X\","
                 "\"wifi.duration_id\": \"%u\","
                 "\"wifi.addr1\": \"%02X:%02X:%02X:%02X:%02X:%02X\","
                 "\"wifi.addr2\": \"%02X:%02X:%02X:%02X:%02X:%02X\","
                 "\"wifi.addr3\": \"%02X:%02X:%02X:%02X:%02X:%02X\","
                 "\"wifi.seq_ctrl\": \"%u\""
                 "}",
                 wifi_hdr->frame_control,
                 wifi_hdr->duration_id,
                 wifi_hdr->addr1[0], wifi_hdr->addr1[1], wifi_hdr->addr1[2],
                 wifi_hdr->addr1[3], wifi_hdr->addr1[4], wifi_hdr->addr1[5],
                 wifi_hdr->addr2[0], wifi_hdr->addr2[1], wifi_hdr->addr2[2],
                 wifi_hdr->addr2[3], wifi_hdr->addr2[4], wifi_hdr->addr2[5],
                 wifi_hdr->addr3[0], wifi_hdr->addr3[1], wifi_hdr->addr3[2],
                 wifi_hdr->addr3[3], wifi_hdr->addr3[4], wifi_hdr->addr3[5],
                 wifi_hdr->seq_ctrl);
    }

    return json;
}


void wifi_layer_free(layer_t* layer) {
    if (!layer) return;

    // Free Wi-Fi-specific parsed data
    if (layer->parsed_data) {
        free(layer->parsed_data);
    }

}
