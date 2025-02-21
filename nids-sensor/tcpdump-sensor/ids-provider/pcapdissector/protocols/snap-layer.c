//
// Created by Jochen van Waasen on 27.01.25.
//
#include "ids-provider/common-util.h"
#include "snap-layer.h"
#include <stdlib.h>
#include <string.h>
#include <stdio.h>
#include <arpa/inet.h>


int dissect_snap(layer_t* layer, packet_t *packet, const uint8_t* data, size_t len) {
    if (len < 5) { // Minimum SNAP header length
        fprintf(stderr, "Insufficient data for SNAP dissection\n");
        return 1;
    }

    snap_header_t* snap_hdr = (snap_header_t*)malloc(sizeof(snap_header_t));
    if (!snap_hdr) {
        fprintf(stderr, "Failed to allocate memory for SNAP header\n");
        return 1;
    }

    // Parse SNAP header fields
    memcpy(snap_hdr->oui, data, 3); // OUI
    snap_hdr->ethertype = ntohs(*(uint16_t*)(data + 3)); // Ethertype

    // Store the SNAP header in the layer
    layer->parsed_data = snap_hdr;
    layer->to_json = snap_to_json;

    // Calculate payload offset and length
    const uint8_t* payload = data + 5;  // SNAP header is 5 bytes
    size_t payload_len = len - 5;

    return process_next_layer(packet, snap_hdr->ethertype, payload, payload_len, handlers);
}

#define JSON_BUFFER_SIZE 1024
static _Thread_local  char json_buffer[JSON_BUFFER_SIZE];
char* snap_to_json(layer_t* layer) {
    if (!layer || !layer->parsed_data) {
        return NULL; // Return NULL if the layer or parsed data is missing
    }

    snap_header_t* snap_hdr = (snap_header_t*)layer->parsed_data;

    // Convert SNAP header fields to JSON
    int bytes_written = snprintf(json_buffer, JSON_BUFFER_SIZE,
             "{ \"snap.oui\": \"0x%02X%02X%02X\", "
             "\"snap.ethertype\": \"0x%04X\" }",
             snap_hdr->oui[0], snap_hdr->oui[1], snap_hdr->oui[2],
             snap_hdr->ethertype);

    if (bytes_written < 0 || bytes_written >= JSON_BUFFER_SIZE) {
        // Error or truncation occurred
        fprintf(stderr, "Error: SNAP JSON truncated or formatting failed\n");
        return NULL;
    }

    return json_buffer;
}

void snap_layer_free(layer_t* layer) {
    if (!layer) return;

    // Free parsed data if allocated
    if (layer->parsed_data) {
        free(layer->parsed_data);
    }
}


