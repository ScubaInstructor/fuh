//
// Created by Jochen van Waasen on 29.01.25.
//

#include "snmp-layer.h"

#include <stdio.h>
#include <stdlib.h>
#include <string.h>

int dissect_snmp(layer_t* layer, packet_t* packet, const uint8_t* data, size_t len) {
    if (len < 2) { // At minimum, SNMP contains version and community string
        fprintf(stderr, "Insufficient data for SNMP dissection\n");
        return 1;
    }

    snmp_header_t* snmp_hdr = (snmp_header_t*)malloc(sizeof(snmp_header_t));
    if (!snmp_hdr) {
        fprintf(stderr, "Failed to allocate memory for SNMP header\n");
        return 1;
    }

    // Extract SNMP version
    snmp_hdr->version = data[0];

    // Extract Community String (assume it's a null-terminated string)
    size_t comm_len = (len > 64) ? 64 : len - 2;
    memcpy(snmp_hdr->community, data + 1, comm_len);
    snmp_hdr->community[comm_len] = '\0'; // Ensure null termination

    // Extract PDU Type
    snmp_hdr->pdu_type = data[1 + comm_len];

    layer->parsed_data = snmp_hdr;
    layer->to_json = snmp_to_json;

    return 1; // Successful dissection
}

#define JSON_BUFFER_SIZE 1024
static _Thread_local  char json_buffer[JSON_BUFFER_SIZE];
char* snmp_to_json(layer_t* layer) {
    if (!layer || !layer->parsed_data) return NULL;

    snmp_header_t* snmp_hdr = (snmp_header_t*)layer->parsed_data;

    int bytes_written = snprintf(json_buffer, JSON_BUFFER_SIZE,
             "\"snmp\": {"
             "\"version\": \"%u\","
             "\"community\": \"%s\","
             "\"pdu_type\": \"0x%02X\""
             "}",
             snmp_hdr->version,
             snmp_hdr->community,
             snmp_hdr->pdu_type);

    if (bytes_written < 0 || bytes_written >= JSON_BUFFER_SIZE) {
        // Error or truncation occurred
        fprintf(stderr, "Error: SNMP JSON truncated or formatting failed\n");
        return NULL;
    }

    return json_buffer;
}

void snmp_layer_free(layer_t* layer) {
    if (!layer) return;
    if (layer->parsed_data) {
        free(layer->parsed_data);
    }
}
