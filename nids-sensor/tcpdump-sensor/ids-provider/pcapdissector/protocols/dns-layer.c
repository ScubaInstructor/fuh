//
// Created by Jochen van Waasen on 29.01.25.
//

#include "dns-layer.h"

#include <layer.h>
#include <stdio.h>
#include <stdlib.h>

int dissect_dns(layer_t* layer, packet_t* packet, const uint8_t* data, size_t len) {
    if (len < 12) {  // DNS header is 12 bytes
        fprintf(stderr, "Insufficient data for DNS dissection\n");
        return 1;
    }

    dns_header_t* dns_hdr = (dns_header_t*)malloc(sizeof(dns_header_t));
    if (!dns_hdr) {
        fprintf(stderr, "Failed to allocate memory for DNS header\n");
        return 1;
    }

    // Parse the DNS header
    dns_hdr->transaction_id = (data[0] << 8) | data[1];
    dns_hdr->flags = (data[2] << 8) | data[3];
    dns_hdr->qd_count = (data[4] << 8) | data[5];
    dns_hdr->an_count = (data[6] << 8) | data[7];
    dns_hdr->ns_count = (data[8] << 8) | data[9];
    dns_hdr->ar_count = (data[10] << 8) | data[11];

    layer->parsed_data = dns_hdr;
    layer->to_json = dns_to_json;

    return 1; // Successful dissection
}

#define JSON_BUFFER_SIZE 1024
static _Thread_local  char json_buffer[JSON_BUFFER_SIZE];
char* dns_to_json(layer_t* layer) {
    if (!layer || !layer->parsed_data) return NULL;

    dns_header_t* dns_hdr = (dns_header_t*)layer->parsed_data;

    int bytes_written = snprintf(json_buffer, JSON_BUFFER_SIZE,
             "\"dns\": {"
             "\"transaction_id\": \"0x%04X\","
             "\"flags\": \"0x%04X\","
             "\"qd_count\": \"%u\","
             "\"an_count\": \"%u\","
             "\"ns_count\": \"%u\","
             "\"ar_count\": \"%u\""
             "}",
             dns_hdr->transaction_id,
             dns_hdr->flags,
             dns_hdr->qd_count,
             dns_hdr->an_count,
             dns_hdr->ns_count,
             dns_hdr->ar_count);

    if (bytes_written < 0 || bytes_written >= JSON_BUFFER_SIZE) {
        // Error or truncation occurred
        fprintf(stderr, "Error: DNS JSON truncated or formatting failed\n");
        return NULL;
    }

    return json_buffer;
}

void dns_layer_free(layer_t* layer) {
    if (!layer) return;
    if (layer->parsed_data) {
        free(layer->parsed_data);
    }
}
