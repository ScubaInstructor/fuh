//
// Created by Jochen van Waasen on 23.01.25.
//
#include "ids-provider/common-util.h"
#include "udp-layer.h"
#include <stdlib.h>
#include <string.h>
#include <stdio.h>
#include <arpa/inet.h>


int dissect_udp(layer_t *layer, packet_t *packet, const uint8_t *data, size_t len) {
    if (len < 8) {
        fprintf(stderr, "Insufficient data for UDP dissection\n");
        return 1;
    }

    udp_header_t *udp_hdr = (udp_header_t *) malloc(sizeof(udp_header_t));
    if (!udp_hdr) {
        fprintf(stderr, "Failed to allocate memory for UDP header\n");
        return 1;
    }

    // Extract fields with proper endianness conversion
    udp_hdr->src_port = ntohs(*(uint16_t *)(data));
    udp_hdr->dst_port = ntohs(*(uint16_t *)(data + 2));
    udp_hdr->length = ntohs(*(uint16_t *)(data + 4));
    udp_hdr->checksum = ntohs(*(uint16_t *)(data + 6));
    udp_hdr->checksum_status = 2; // Assuming checksum is valid
    udp_hdr->stream = 0; // Initialize stream number
    udp_hdr->stream_pnum = 1; // Initialize packet number within stream
    udp_hdr->time_relative = 0.0; // Initialize relative time
    udp_hdr->time_delta = 0.0; // Initialize time delta
    udp_hdr->warning = NULL;

    // Calculate payload length and set payload pointer
    udp_hdr->payload_len = udp_hdr->length >= 8 ? udp_hdr->length - 8 : 0;
    udp_hdr->payload = udp_hdr->payload
                           ? hex_encode(udp_hdr->payload, udp_hdr->payload_len)
                           : (const unsigned char *) "";

    // Attach parsed data and JSON conversion function
    layer->parsed_data = udp_hdr;
    layer->to_json = udp_to_json;

    if (udp_hdr->length < 8) {
        fprintf(stderr, "Invalid UDP length: %u (must be at least 8 bytes)\n", udp_hdr->length);
        udp_hdr->warning = "Invalid length (too small)";
        return 1;
    }

    if (udp_hdr->length > len) {
        fprintf(stderr, "Invalid UDP length: %u (exceeds available data: %zu bytes)\n", udp_hdr->length, len);
        udp_hdr->warning = "Fragmented or truncated UDP packet";
        return 1;
    }

    if (udp_hdr->payload_len == 0) {
        return 1;
    }

    return 1;
    //return process_next_layer(packet, udp_hdr->dst_port, udp_hdr->payload, udp_hdr->payload_len, udp_port_handlers);
}


#define JSON_BUFFER_SIZE 8192
static _Thread_local char json_buffer[JSON_BUFFER_SIZE];

char *udp_to_json(layer_t *layer) {
    if (!layer || !layer->parsed_data) return NULL;
    udp_header_t *udp_hdr = (udp_header_t *) layer->parsed_data;

    char warning_buffer[JSON_BUFFER_SIZE] = "";
    if (udp_hdr->warning) {
        snprintf(warning_buffer, JSON_BUFFER_SIZE, ", \"udp.warning\": \"%s\"", udp_hdr->warning);
    }

    int bytes_written = snprintf(json_buffer, JSON_BUFFER_SIZE,
                                 "\"udp\":{"
                                 "\"udp_udp_srcport\":%u,"
                                 "\"udp_udp_dstport\":%u,"
                                 "\"udp_udp_port\":[%u,%u],"
                                 "\"udp_udp_length\":%u,"
                                 "\"udp_udp_checksum\":\"0x%04X\","
                                 "\"udp_udp_checksum_status\":%u,"
                                 "\"udp_udp_stream\":%u,"
                                 "\"udp_udp_stream_pnum\":%u,"
                                 "\"udp_udp_time_relative\":%.9f,"
                                 "\"udp_udp_time_delta\":%.9f,"
                                 "\"udp_udp_payload\":\"%s\"%s"
                                 "}",
                                 udp_hdr->src_port,
                                 udp_hdr->dst_port,
                                 udp_hdr->src_port, udp_hdr->dst_port,
                                 udp_hdr->length,
                                 udp_hdr->checksum,
                                 udp_hdr->checksum_status,
                                 udp_hdr->stream,
                                 udp_hdr->stream_pnum,
                                 udp_hdr->time_relative,
                                 udp_hdr->time_delta,
                                 udp_hdr->payload ? hex_encode(udp_hdr->payload, udp_hdr->payload_len) : (const unsigned char*)"",
                                 udp_hdr->warning ? warning_buffer : "");

    if (bytes_written < 0 || bytes_written >= JSON_BUFFER_SIZE) {
        return NULL; // Buffer too small or error occurred
    }

    return json_buffer;
}


void udp_layer_free(layer_t *layer) {
    if (!layer) return;

    // Free parsed data if allocated
    if (layer->parsed_data) {
        free(layer->parsed_data);
    }
}
