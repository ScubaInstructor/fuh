//
// Created by Jochen van Waasen on 28.01.25.
//

#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <arpa/inet.h>
#include "sna-path-control-layer.h"

int dissect_sna_path_control(layer_t* layer, packet_t *packet, const uint8_t* data, size_t len) {
    if (len < 3) { // Minimum size for SNA Path Control: Command (1 byte) + Routing Info (2 bytes)
        fprintf(stderr, "Insufficient data for SNA Path Control dissection\n");
        return 1;
    }

    // Allocate memory for the SNA Path Control header
    sna_path_control_header_t* sna_hdr = (sna_path_control_header_t*)malloc(sizeof(sna_path_control_header_t) + len - 3);
    if (!sna_hdr) {
        fprintf(stderr, "Failed to allocate memory for SNA Path Control header\n");
        return 1;
    }

    // Parse SNA Path Control fields
    sna_hdr->command = data[0];
    sna_hdr->routing_info = (data[1] << 8) | data[2];

    // Copy the payload, if any
    size_t payload_len = len - 3; // Remaining data after the header
    if (payload_len > 0) {
        memcpy(sna_hdr->payload, data + 3, payload_len);
    }

    // Store the parsed header in the layer
    layer->parsed_data = sna_hdr;
    layer->to_json = sna_path_control_to_json;

    // Log dissection details
    fprintf(stderr, "SNA Path Control: Command=0x%02X, Routing Info=0x%04X, Payload Length=%zu\n",
            sna_hdr->command, sna_hdr->routing_info, payload_len);

    return 1; // Successful dissection
}

#define JSON_BUFFER_SIZE 512
static _Thread_local  char json_buffer[JSON_BUFFER_SIZE];
char* sna_path_control_to_json(layer_t* layer) {
    if (!layer || !layer->parsed_data) {
        return NULL; // Return NULL if the layer or parsed data is missing
    }

    sna_path_control_header_t* sna_hdr = (sna_path_control_header_t*)layer->parsed_data;

    // Convert SNA Path Control fields to JSON
    int bytes_written = snprintf(json_buffer, JSON_BUFFER_SIZE,
             "\"sna\":{"
             "\"sna_sna_command\":\"0x%02X\", "
             "\"sna_sna_routing_info\":\"0x%04X\", "
             "\"sna_sna_payload_length\":%zu}",
             sna_hdr->command,
             sna_hdr->routing_info,
             strlen((char*)sna_hdr->payload));

    if (bytes_written < 0 || bytes_written >= JSON_BUFFER_SIZE) {
        // Error or truncation occurred
        fprintf(stderr, "Error: SNA_PATH_CONTROL JSON truncated or formatting failed\n");
        return NULL;
    }

    return json_buffer;
}

void sna_path_control_layer_free(layer_t* layer) {
    if (!layer) return;

    // Free parsed data if allocated
    if (layer->parsed_data) {
        free(layer->parsed_data);
    }
}

