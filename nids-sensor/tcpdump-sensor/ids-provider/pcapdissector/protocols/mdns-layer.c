#include "mdns-layer.h"
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <arpa/inet.h>

int dissect_mdns(layer_t *layer, packet_t *packet, const uint8_t *data, size_t len) {
    if (len < MDNS_HEADER_LEN) {
        fprintf(stderr, "Insufficient data for mDNS dissection\n");
        return 1;
    }

    mdns_header_t *mdns_hdr = (mdns_header_t *)malloc(sizeof(mdns_header_t));
    if (!mdns_hdr) {
        fprintf(stderr, "Failed to allocate memory for mDNS header\n");
        return 1;
    }

    mdns_hdr->transaction_id = ntohs(*(uint16_t *)data);
    mdns_hdr->flags = ntohs(*(uint16_t *)(data + 2));
    mdns_hdr->questions = ntohs(*(uint16_t *)(data + 4));
    mdns_hdr->answer_rrs = ntohs(*(uint16_t *)(data + 6));
    mdns_hdr->authority_rrs = ntohs(*(uint16_t *)(data + 8));
    mdns_hdr->additional_rrs = ntohs(*(uint16_t *)(data + 10));

    layer->parsed_data = mdns_hdr;
    layer->to_json = mdns_to_json;

    // Further parsing of questions, answers, etc. could be added here

    return 1; // Success
}

#define JSON_BUFFER_SIZE 4096
static _Thread_local char json_buffer[JSON_BUFFER_SIZE];

char *mdns_to_json(layer_t *layer) {
    if (!layer || !layer->parsed_data) return NULL;

    mdns_header_t *mdns_hdr = (mdns_header_t *)layer->parsed_data;

    int bytes_written = snprintf(json_buffer, JSON_BUFFER_SIZE,
        "\"mdns\": {"
        "\"transaction_id\": %u,"
        "\"flags\": \"0x%04X\","
        "\"questions\": %u,"
        "\"answer_rrs\": %u,"
        "\"authority_rrs\": %u,"
        "\"additional_rrs\": %u"
        "}",
        mdns_hdr->transaction_id,
        mdns_hdr->flags,
        mdns_hdr->questions,
        mdns_hdr->answer_rrs,
        mdns_hdr->authority_rrs,
        mdns_hdr->additional_rrs
    );

    if (bytes_written < 0 || bytes_written >= JSON_BUFFER_SIZE) {
        fprintf(stderr, "Error: mDNS JSON truncated or formatting failed\n");
        return NULL;
    }

    return json_buffer;
}

void mdns_layer_free(layer_t *layer) {
    if (!layer) return;
    if (layer->parsed_data) {
        free(layer->parsed_data);
        layer->parsed_data = NULL;
    }
    layer->protocol_name = NULL;
    layer->to_json = NULL;
    layer->dissect = NULL;
}
