//
// Created by Jochen van Waasen on 27.01.25.
//

#include "stp-layer.h"

#include <inttypes.h>
#include <stdlib.h>
#include <string.h>
#include <stdio.h>
#include <arpa/inet.h>

int dissect_stp(layer_t* layer, packet_t *packet, const uint8_t* data, size_t len) {
    if (len < 35) { // Minimum STP BPDU length
        fprintf(stderr, "Insufficient data for STP dissection\n");
        return 1;
    }

    stp_header_t* stp_hdr = (stp_header_t*)malloc(sizeof(stp_header_t));
    if (!stp_hdr) {
        fprintf(stderr, "Failed to allocate memory for STP header\n");
        return 1;
    }

    // Parse STP fields
    stp_hdr->protocol_id = (data[0] << 8) | data[1];
    stp_hdr->version = data[2];
    stp_hdr->bpdu_type = data[3];
    stp_hdr->flags = data[4];
    stp_hdr->root_id = ((uint64_t)data[5] << 56) | ((uint64_t)data[6] << 48) |
                       ((uint64_t)data[7] << 40) | ((uint64_t)data[8] << 32) |
                       ((uint64_t)data[9] << 24) | ((uint64_t)data[10] << 16) |
                       ((uint64_t)data[11] << 8) | (uint64_t)data[12];
    stp_hdr->root_path_cost = (data[13] << 24) | (data[14] << 16) | (data[15] << 8) | data[16];
    stp_hdr->bridge_id = ((uint64_t)data[17] << 56) | ((uint64_t)data[18] << 48) |
                         ((uint64_t)data[19] << 40) | ((uint64_t)data[20] << 32) |
                         ((uint64_t)data[21] << 24) | ((uint64_t)data[22] << 16) |
                         ((uint64_t)data[23] << 8) | (uint64_t)data[24];
    stp_hdr->port_id = (data[25] << 8) | data[26];
    stp_hdr->message_age = ntohs(*(uint16_t*)(data + 27));
    stp_hdr->max_age = ntohs(*(uint16_t*)(data + 29));
    stp_hdr->hello_time = ntohs(*(uint16_t*)(data + 31));
    stp_hdr->forward_delay = ntohs(*(uint16_t*)(data + 33));

    // Store the STP header in the layer
    layer->parsed_data = stp_hdr;
    layer->to_json = stp_to_json;

    return 1; // Dissection successful
}

#define JSON_BUFFER_SIZE 4096
static _Thread_local  char json_buffer[JSON_BUFFER_SIZE];
char* stp_to_json(layer_t* layer) {
    if (!layer || !layer->parsed_data) return NULL;

    stp_header_t* stp_hdr = (stp_header_t*)layer->parsed_data;

    int bytes_written = snprintf(json_buffer, JSON_BUFFER_SIZE,
         "\"stp\":{ \"stp.protocol\": \"STP\", "
         "\"stp.protocol_id\": \"0x%04X\", "
         "\"stp.version\": %u, "
         "\"stp.bpdu_type\": %u, "
         "\"stp.flags\": \"0x%02X\", "
         "\"stp.root_id\": \"0x%" PRIx64 "\", "
         "\"stp.root_path_cost\": %u, "
         "\"stp.bridge_id\": \"0x%" PRIx64 "\", "
         "\"stp.port_id\": %u, "
         "\"stp.message_age\": %.2f, "
         "\"stp.max_age\": %.2f, "
         "\"stp.hello_time\": %.2f, "
         "\"stp.forward_delay\": %.2f }",
         stp_hdr->protocol_id,
         stp_hdr->version,
         stp_hdr->bpdu_type,
         stp_hdr->flags,
         stp_hdr->root_id,
         stp_hdr->root_path_cost,
         stp_hdr->bridge_id,
         stp_hdr->port_id,
         stp_hdr->message_age / 256.0,  // Convert to seconds
         stp_hdr->max_age / 256.0,     // Convert to seconds
         stp_hdr->hello_time / 256.0,  // Convert to seconds
         stp_hdr->forward_delay / 256.0); // Convert to seconds

    if (bytes_written < 0 || bytes_written >= JSON_BUFFER_SIZE) {
        // Error or truncation occurred
        fprintf(stderr, "Error: STP JSON truncated or formatting failed\n");
        return NULL;
    }

    return json_buffer;
}

void stp_layer_free(layer_t* layer) {
    if (!layer) return;

    // Free parsed data if allocated
    if (layer->parsed_data) {
        free(layer->parsed_data);
    }
}

