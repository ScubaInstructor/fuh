//
// Created by Jochen van Waasen on 23.01.25.
//

#include "icmp-layer.h"
#include <stdlib.h>
#include <string.h>
#include <stdio.h>

int dissect_icmp(layer_t* layer, packet_t *packet, const uint8_t* data, size_t len) {
    if (len < 8) { // Minimum ICMP header length
        fprintf(stderr, "Insufficient data for ICMP dissection\n");
        return 1;
    }

    icmp_header_t* icmp_hdr = (icmp_header_t*)malloc(sizeof(icmp_header_t));
    if (!icmp_hdr) {
        fprintf(stderr, "Failed to allocate memory for ICMP header\n");
        return 1;
    }

    // Parse the common ICMP header fields
    icmp_hdr->type = data[0];
    icmp_hdr->code = data[1];
    icmp_hdr->checksum = (data[2] << 8) | data[3];
    icmp_hdr->identifier = (data[4] << 8) | data[5];
    icmp_hdr->sequence_number = (data[6] << 8) | data[7];

    // Parse additional fields based on type and code
    switch (icmp_hdr->type) {
        case 3: // Destination Unreachable
        case 11: // Time Exceeded
        case 12: // Parameter Problem
            if (len >= 12) {
                memcpy(icmp_hdr->original_data, data + 8, 8); // Copy part of the original IP header
            }
        break;

        case 5: // Redirect
            if (len >= 12) {
                icmp_hdr->gateway_address = (data[8] << 24) | (data[9] << 16) | (data[10] << 8) | data[11];
                memcpy(icmp_hdr->original_data, data + 12, 8); // Copy part of the original IP header
            }
        break;

        default:
            icmp_hdr->unused = 0; // Default unused field for unsupported types
        break;
    }

    // Store parsed ICMP data in the layer structure
    layer->parsed_data = icmp_hdr;

    // Set the to_json function pointer
    layer->to_json = icmp_to_json;

    // No next layer for ICMP
    return 1; // Dissection successful
}

#define JSON_BUFFER_SIZE 4096
static _Thread_local char json_buffer[JSON_BUFFER_SIZE];

char* icmp_to_json(layer_t* layer) {
    if (!layer || !layer->parsed_data) return NULL;

    icmp_header_t* icmp_hdr = (icmp_header_t*)layer->parsed_data;

    int bytes_written = snprintf(json_buffer, JSON_BUFFER_SIZE,
             "\"icmp\":{ \"icmp.protocol\": \"ICMP\", "
             "\"icmp_icmp_type\": %u, "
             "\"icmp_icmp_code\": %u, "
             "\"icmp_icmp_checksum\": \"0x%04X\", "
             "\"icmp_icmp_identifier\": %u, "
             "\"icmp_icmp_sequence_number\": %u",
             icmp_hdr->type,
             icmp_hdr->code,
             icmp_hdr->checksum,
             icmp_hdr->identifier,
             icmp_hdr->sequence_number);

    if (bytes_written < 0 || bytes_written >= JSON_BUFFER_SIZE) {
        return NULL; // Error or buffer overflow
    }

    int remaining_space = JSON_BUFFER_SIZE - bytes_written;
    int additional_bytes = 0;

    switch (icmp_hdr->type) {
        case 3: // Destination Unreachable
        case 11: // Time Exceeded
        case 12: // Parameter Problem
            additional_bytes = snprintf(json_buffer + bytes_written, remaining_space,
                     ", \"icmp.original_data\": \"0x%08X 0x%08X\" }",
                     icmp_hdr->original_data[0], icmp_hdr->original_data[1]);
            break;

        case 5: // Redirect
            additional_bytes = snprintf(json_buffer + bytes_written, remaining_space,
                     ", \"icmp.gateway_address\": \"%u.%u.%u.%u\", "
                     "\"icmp.original_data\": \"0x%08X 0x%08X\" }",
                     (icmp_hdr->gateway_address >> 24) & 0xFF,
                     (icmp_hdr->gateway_address >> 16) & 0xFF,
                     (icmp_hdr->gateway_address >> 8) & 0xFF,
                     icmp_hdr->gateway_address & 0xFF,
                     icmp_hdr->original_data[0], icmp_hdr->original_data[1]);
            break;

        default:
            additional_bytes = snprintf(json_buffer + bytes_written, remaining_space, " }");
            break;
    }

    if (additional_bytes < 0 || additional_bytes >= remaining_space) {
        return NULL; // Error or buffer overflow
    }

    return json_buffer;
}


void icmp_layer_free(layer_t* layer) {
    if (!layer) return;

    // Free the parsed data (ARP header)
    if (layer->parsed_data) {
        free(layer->parsed_data);
    }
}



