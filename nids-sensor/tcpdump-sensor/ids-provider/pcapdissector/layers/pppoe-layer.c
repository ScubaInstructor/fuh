//
// Created by Jochen van Waasen on 23.01.25.
//
#include "ids-provider/common-util.h"
#include "pppoe-layer.h"
#include <stdlib.h>
#include <string.h>
#include <stdio.h>

#include <netinet/in.h>

#include "ids-provider/pcapdissector/layer.h"

int dissect_pppoe(layer_t* layer, packet_t *packet, const uint8_t* data, size_t len) {
    if (len < PPPOE_HEADER_LEN) {
        fprintf(stderr, "Insufficient data for PPPoE dissection\n");
        return 0;
    }

    pppoe_header_t* pppoe_hdr = (pppoe_header_t*)malloc(sizeof(pppoe_header_t));
    if (!pppoe_hdr) {
        fprintf(stderr, "Failed to allocate memory for PPPoE header\n");
        return 0;
    }

    // Parse the PPPoE header
    pppoe_hdr->version_type = data[0];
    pppoe_hdr->code = data[1];
    pppoe_hdr->session_id = (data[2] << 8) | data[3];
    pppoe_hdr->payload_length = (data[4] << 8) | data[5];

    // Check if the payload length is valid
    if (pppoe_hdr->payload_length > (len - PPPOE_HEADER_LEN)) {
        fprintf(stderr, "Invalid PPPoE payload length\n");
        free(pppoe_hdr);
        return 0;
    }

    // Store parsed header in the layer
    layer->parsed_data = pppoe_hdr;
    layer->to_json = pppoe_to_json;  // Assuming you have a pppoe_to_json function

    // If there's a payload, process the next layer
    if (pppoe_hdr->payload_length > 0) {
        const uint8_t* payload = data + PPPOE_HEADER_LEN;
        size_t payload_len = pppoe_hdr->payload_length;

        // Determine the next protocol ID (PPP protocol field)
        uint16_t next_protocol_id = (payload[0] << 8) | payload[1];
        payload += 2;  // Skip the PPP protocol field
        payload_len -= 2;

        // Use the process_next_layer utility function
        return process_next_layer(packet, next_protocol_id, payload, payload_len, handlers);
    }

    return 1; // Success
}

#define JSON_BUFFER_SIZE 4096
static _Thread_local char json_buffer[JSON_BUFFER_SIZE];

char *pppoe_to_json(layer_t *layer) {
    if (!layer || !layer->parsed_data) return NULL;

    pppoe_header_t *pppoe_hdr = (pppoe_header_t *) layer->parsed_data;

    // Extract version and type from the version_type field
    uint8_t version = (pppoe_hdr->version_type >> 4) & 0x0F;
    uint8_t type = pppoe_hdr->version_type & 0x0F;

    // Construct the JSON structure
    int bytes_written = snprintf(json_buffer, JSON_BUFFER_SIZE,
                                 "\"pppoe\":{"
                                 "\"pppoe.version\":\"%u\","
                                 "\"pppoe.type\":\"%u\","
                                 "\"pppoe.code\":\"%u\","
                                 "\"pppoe.session_id\":\"0x%04X\","
                                 "\"pppoe.payload_length\":\"%u\""
                                 "}",
                                 version,
                                 type,
                                 pppoe_hdr->code,
                                 pppoe_hdr->session_id,
                                 pppoe_hdr->payload_length);

    if (bytes_written < 0 || bytes_written >= JSON_BUFFER_SIZE) {
        fprintf(stderr, "Error: PPPoE JSON truncated or formatting failed\n");
        return NULL;
    }

    return json_buffer;
}

void pppoe_layer_free(layer_t *layer) {
    if (!layer) return;

    // Free only the parsed data if it was dynamically allocated
    if (layer->parsed_data) {
        free(layer->parsed_data);
        layer->parsed_data = NULL;
    }

    // Reset other fields if necessary
    layer->protocol_name = NULL;
    layer->to_json = NULL;
    layer->dissect = NULL;

    // Note: We don't free the layer itself or handle next_layer
}






