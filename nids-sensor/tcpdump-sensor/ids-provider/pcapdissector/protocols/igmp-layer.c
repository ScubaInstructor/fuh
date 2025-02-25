//
// Created by Jochen van Waasen on 25.01.25.
//

#include "igmp-layer.h"

#include <layer.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

int dissect_igmp(layer_t* layer, packet_t *packet, const uint8_t* data, size_t len) {
    if (!layer || !data || len < 8) { // Minimum IGMP header length
        fprintf(stderr, "Insufficient data for IGMP dissection\n");
        return 1;
    }

    // Allocate memory for the IGMP header structure
    igmp_header_t* igmp_hdr = (igmp_header_t*)malloc(sizeof(igmp_header_t));
    if (!igmp_hdr) {
        fprintf(stderr, "Failed to allocate memory for IGMP header\n");
        return 1;
    }

    // Parse IGMP fields
    igmp_hdr->type = data[0];                               // Message Type
    igmp_hdr->max_resp_time = data[1];                      // Max Response Time
    igmp_hdr->checksum = (data[2] << 8) | data[3];          // Checksum
    memcpy(igmp_hdr->group_address, &data[4], 4);           // Group Address

    // Calculate the number of source addresses
    igmp_hdr->num_source_addresses = (len > 12) ? (len - 12) / 4 : 0;

    // Parse source addresses if present
    if (igmp_hdr->num_source_addresses > 0) {
        igmp_hdr->source_addresses = (uint8_t(*)[4])malloc(igmp_hdr->num_source_addresses * 4);
        if (!igmp_hdr->source_addresses) {
            fprintf(stderr, "Failed to allocate memory for source addresses\n");
            free(igmp_hdr);
            return 1;
        }
        memcpy(igmp_hdr->source_addresses, data + 12, igmp_hdr->num_source_addresses * 4);
    } else {
        igmp_hdr->source_addresses = NULL;
    }

    // Attach parsed header to the layer
    layer->parsed_data = igmp_hdr;
    layer->to_json = igmp_to_json;

    return 1; // Successful dissection
}


#define JSON_BUFFER_SIZE 4096
static _Thread_local char json_buffer[JSON_BUFFER_SIZE];

char* igmp_to_json(layer_t* layer) {
    if (!layer || !layer->parsed_data) return NULL;

    igmp_header_t* igmp_hdr = (igmp_header_t*)layer->parsed_data;

    int bytes_written = snprintf(json_buffer, JSON_BUFFER_SIZE,
             "\"igmp\":{ \"igmp.type\": \"%u\", "
             "\"igmp.max_resp_time\": \"%u\", "
             "\"igmp.checksum\": \"0x%04X\", "
             "\"igmp.group_address\": \"%u.%u.%u.%u\", "
             "\"igmp.reserved\": \"%u\", "
             "\"igmp.s_flag\": \"%u\", "
             "\"igmp.qrv\": \"%u\", "
             "\"igmp.qqic\": \"%u\", "
             "\"igmp.source_addresses\": [",
             igmp_hdr->type,
             igmp_hdr->max_resp_time,
             igmp_hdr->checksum,
             igmp_hdr->group_address[0], igmp_hdr->group_address[1],
             igmp_hdr->group_address[2], igmp_hdr->group_address[3],
             igmp_hdr->reserved,
             igmp_hdr->s_flag,
             igmp_hdr->qrv,
             igmp_hdr->qqic);

    if (bytes_written < 0 || bytes_written >= JSON_BUFFER_SIZE) {
        return NULL; // Error or buffer overflow
    }

    int remaining_space = JSON_BUFFER_SIZE - bytes_written;

    // Append source addresses
    for (size_t i = 0; i < igmp_hdr->num_source_addresses && remaining_space > 0; i++) {
        int addr_bytes = snprintf(json_buffer + bytes_written, remaining_space,
                                  "%s\"%u.%u.%u.%u\"",
                                  i > 0 ? ", " : "",
                                  igmp_hdr->source_addresses[i][0],
                                  igmp_hdr->source_addresses[i][1],
                                  igmp_hdr->source_addresses[i][2],
                                  igmp_hdr->source_addresses[i][3]);

        if (addr_bytes < 0 || addr_bytes >= remaining_space) {
            return NULL; // Error or buffer overflow
        }

        bytes_written += addr_bytes;
        remaining_space -= addr_bytes;
    }

    // Close the JSON array and object
    if (remaining_space > 2) {
        strcat(json_buffer + bytes_written, "] }");
    } else {
        return NULL; // Not enough space to close the JSON
    }

    return json_buffer;
}


void igmp_layer_free(layer_t* layer) {
    if (!layer) return;

    // Free the parsed data (ARP header)
    if (layer->parsed_data) {
        free(layer->parsed_data);
    }
}


