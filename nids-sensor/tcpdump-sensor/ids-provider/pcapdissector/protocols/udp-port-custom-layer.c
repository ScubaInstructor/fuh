#include "udp-port-custom-layer.h"

#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <arpa/inet.h>

int dissect_udp_port_custom(layer_t *layer, packet_t *packet, const uint8_t *data, size_t len) {
    if (len < 8) {
        fprintf(stderr, "Insufficient data for UDP dissection\n");
        return 1;
    }

    udp_port_custom_header_t *udp_hdr = (udp_port_custom_header_t *)malloc(sizeof(udp_port_custom_header_t));
    if (!udp_hdr) {
        fprintf(stderr, "Failed to allocate memory for UDP header\n");
        return 1;
    }

    udp_hdr->src_port = ntohs(*(uint16_t *)data);
    udp_hdr->dst_port = ntohs(*(uint16_t *)(data + 2));
    udp_hdr->length = ntohs(*(uint16_t *)(data + 4));
    udp_hdr->checksum = ntohs(*(uint16_t *)(data + 6));

    layer->parsed_data = udp_hdr;
    layer->to_json = udp_port_custom_to_json;

    if (udp_hdr->length < 8 || udp_hdr->length > len) {
        fprintf(stderr, "Invalid UDP length: %u (expected between 8 and %zu)\n", udp_hdr->length, len);
        return 1;
    }

    udp_hdr->payload_length = udp_hdr->length - 8;

    // Set the protocol name to "UDP-<dst_port>"
    char protocol_name[20];
    snprintf(protocol_name, sizeof(protocol_name), "UDP-%u", udp_hdr->dst_port);
    layer->protocol_name = strdup(protocol_name);

    return 1; // Success
}

#define JSON_BUFFER_SIZE 4096
static _Thread_local char json_buffer[JSON_BUFFER_SIZE];

char *udp_port_custom_to_json(layer_t *layer) {
    if (!layer || !layer->parsed_data) return NULL;

    udp_port_custom_header_t *udp_hdr = (udp_port_custom_header_t *)layer->parsed_data;

    int bytes_written = snprintf(json_buffer, JSON_BUFFER_SIZE,
        "\"udp\": {"
        "\"udp.srcport\": \"%u\","
        "\"udp.dstport\": \"%u\","
        "\"udp.length\": \"%u\","
        "\"udp.checksum\": \"0x%04X\","
        "\"payload_length\": \"%zu\""
        "}",
        udp_hdr->src_port,
        udp_hdr->dst_port,
        udp_hdr->length,
        udp_hdr->checksum,
        udp_hdr->payload_length
    );

    if (bytes_written < 0 || bytes_written >= JSON_BUFFER_SIZE) {
        fprintf(stderr, "Error: UDP JSON truncated or formatting failed\n");
        return NULL;
    }

    return json_buffer;
}

void udp_port_custom_layer_free(layer_t *layer) {
    if (!layer) return;
    if (layer->parsed_data) {
        free(layer->parsed_data);
        layer->parsed_data = NULL;
    }
    if (layer->protocol_name) {
        free((char *)layer->protocol_name);
        layer->protocol_name = NULL;
    }
    layer->to_json = NULL;
    layer->dissect = NULL;
}
