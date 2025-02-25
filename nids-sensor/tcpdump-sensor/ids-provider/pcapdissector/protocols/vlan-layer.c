//
// Created by Jochen van Waasen on 23.01.25.
//
#include <ids-provider/common-util.h>
#include "vlan-layer.h"
#include <stdlib.h>
#include <string.h>
#include <stdio.h>


int dissect_vlan(layer_t* layer, packet_t *packet, const uint8_t* data, size_t len) {
    if (len < 4) {
        fprintf(stderr, "Insufficient data for VLAN dissection\n");
        return 1;
    }

    vlan_header_t* vlan_hdr = (vlan_header_t*)malloc(sizeof(vlan_header_t));
    if (!vlan_hdr) {
        fprintf(stderr, "Failed to allocate memory for VLAN header\n");
        return 1;
    }

    vlan_hdr->tci = (data[0] << 8) | data[1];
    vlan_hdr->ethertype = (data[2] << 8) | data[3];

    layer->parsed_data = vlan_hdr;

    const uint8_t* payload = data + 4;
    size_t payload_len = len - 4;

    return process_next_layer(packet, vlan_hdr->ethertype, payload, payload_len, handlers);
}

#define JSON_BUFFER_SIZE 4096
static _Thread_local  char json_buffer[JSON_BUFFER_SIZE];
char* vlan_to_json(layer_t* layer) {
    if (!layer || !layer->parsed_data) return NULL;

    vlan_header_t* vlan_hdr = (vlan_header_t*)layer->parsed_data;

    int bytes_written = snprintf(json_buffer, JSON_BUFFER_SIZE,
             "\"vlan\": {"
             "\"vlan.pcp\": \"%u\","
             "\"vlan.dei\": \"%u\","
             "\"vlan.id\": \"%u\","
             "\"vlan.ethertype\": \"0x%04X\""
             "}",
             vlan_hdr->pcp,
             vlan_hdr->dei,
             vlan_hdr->vlan_id,
             vlan_hdr->ethertype);

    return json_buffer;
}

void vlan_layer_free(layer_t *layer) {
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

