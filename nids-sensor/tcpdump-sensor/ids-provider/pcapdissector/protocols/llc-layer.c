//
// Created by Jochen van Waasen on 26.01.25.
//
#include <ids-provider/common-util.h>
#include "llc-layer.h"
#include <stdlib.h>
#include <string.h>
#include <stdio.h>


int dissect_llc(layer_t* layer, packet_t *packet, const uint8_t* data, size_t len) {
    if (!layer || !packet || !data || len < 3) {
        fprintf(stderr, "Insufficient data for LLC dissection\n");
        return 1;
    }

    llc_header_t* llc_hdr = (llc_header_t*)malloc(sizeof(llc_header_t));
    if (!llc_hdr) {
        fprintf(stderr, "Failed to allocate memory for LLC header\n");
        return 1;
    }

    llc_hdr->dsap = data[0];
    llc_hdr->ssap = data[1];
    llc_hdr->control = data[2];

    size_t header_length = 3;
    layer->parsed_data = llc_hdr;
    layer->to_json = llc_to_json;

    const uint8_t* payload = data + header_length;
    size_t payload_len = len - header_length;

    // Handle next layer
    if (payload_len > 0) {
        uint16_t protocol_id;

        // Check for SNAP
        if (llc_hdr->dsap == 0xAA && llc_hdr->ssap == 0xAA && llc_hdr->control == 0x03) {
            protocol_id = 0xAAAA; // SNAP identifier
        } else {
            // For non-SNAP, use both DSAP and SSAP as the protocol identifier
            protocol_id = (llc_hdr->dsap << 8) | llc_hdr->ssap;
        }

        return process_next_layer(packet, protocol_id, payload, payload_len, handlers);
    }

    return 1; // Success, but no further layers to process
}


#define JSON_BUFFER_SIZE 1024
static _Thread_local char json_buffer[JSON_BUFFER_SIZE];

char* llc_to_json(layer_t* layer) {
    if (!layer || !layer->parsed_data) return NULL;

    llc_header_t* llc_hdr = (llc_header_t*)layer->parsed_data;

    int bytes_written = snprintf(json_buffer, JSON_BUFFER_SIZE,
             "\"llc\": {"
             "\"llc.dsap\": \"0x%02X\","
             "\"llc.ssap\": \"0x%02X\","
             "\"llc.control\": \"0x%02X\","
             "\"llc.type\": \"%s\"",
             llc_hdr->dsap,
             llc_hdr->ssap,
             llc_hdr->control,
             (llc_hdr->dsap == 0xAA && llc_hdr->ssap == 0xAA && llc_hdr->control == 0x03) ? "SNAP" : "I");

    if (bytes_written < 0 || bytes_written >= JSON_BUFFER_SIZE) {
        return NULL; // Error or buffer overflow
    }

    if (llc_hdr->dsap == 0xAA && llc_hdr->ssap == 0xAA && llc_hdr->control == 0x03) {
        int remaining_space = JSON_BUFFER_SIZE - bytes_written;
        int snap_bytes = snprintf(json_buffer + bytes_written, remaining_space,
                 ",\"llc.oui\": \"0x%06X\","
                 "\"llc.pid\": \"0x%04X\"",
                 llc_hdr->oui,
                 llc_hdr->pid);

        if (snap_bytes < 0 || snap_bytes >= remaining_space) {
            return NULL; // Error or buffer overflow
        }

        bytes_written += snap_bytes;
    }

    if (JSON_BUFFER_SIZE - bytes_written > 1) {
        json_buffer[bytes_written] = '}';
        json_buffer[bytes_written + 1] = '\0';
    } else {
        return NULL; // Not enough space to close the JSON object
    }

    return json_buffer;
}


void llc_layer_free(layer_t* layer) {
    if (!layer) return;

    if (layer->parsed_data) {
        free(layer->parsed_data);
    }
}

