//
// Created by Jochen van Waasen on 25.01.25.
//

#include "sctp-layer.h"

#include <layer.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <arpa/inet.h>

uint32_t sctp_get_payload_length(sctp_header_t *header) {
    uint32_t total_length = 0;
    for (uint32_t i = 0; i < header->chunk_count; i++) {
        total_length += header->chunks[i]->length - 4; // Subtract chunk header length
    }
    return total_length;
}

uint32_t sctp_get_header_length(sctp_header_t *header) {
    uint32_t total_length = SCTP_COMMON_HEADER_LENGTH;
    for (uint32_t i = 0; i < header->chunk_count; i++) {
        total_length += header->chunks[i]->length;
    }
    return total_length;
}


int dissect_sctp(layer_t *layer, packet_t *packet, const uint8_t *data, size_t len) {
    if (len < 12) {
        fprintf(stderr, "Insufficient data for SCTP dissection\n");
        return 1;
    }

    sctp_header_t *sctp_hdr = (sctp_header_t *) malloc(sizeof(sctp_header_t));
    if (!sctp_hdr) {
        fprintf(stderr, "Failed to allocate memory for SCTP header\n");
        return 1;
    }

    sctp_hdr->src_port = ntohs(*(uint16_t *)data);
    sctp_hdr->dst_port = ntohs(*(uint16_t *)(data + 2));
    sctp_hdr->verification_tag = ntohl(*(uint32_t *)(data + 4));
    sctp_hdr->checksum = ntohl(*(uint32_t *)(data + 8));
    sctp_hdr->chunk_count = 0;
    sctp_hdr->chunks = NULL;

    // Parse SCTP chunks
    size_t offset = 12;
    while (offset < len) {
        if (offset + 4 > len) break; // Not enough data for chunk header

        uint8_t chunk_type = data[offset];
        uint8_t chunk_flags = data[offset + 1];
        uint16_t chunk_length = ntohs(*(uint16_t *)(data + offset + 2));

        if (offset + chunk_length > len) break; // Chunk exceeds packet length

        sctp_chunk_t *chunk = malloc(sizeof(sctp_chunk_t));
        if (!chunk) break;

        chunk->type = chunk_type;
        chunk->flags = chunk_flags;
        chunk->length = chunk_length;
        chunk->data = malloc(chunk_length - 4);
        if (!chunk->data) {
            free(chunk);
            break;
        }
        memcpy(chunk->data, data + offset + 4, chunk_length - 4);

        sctp_hdr->chunk_count++;
        sctp_hdr->chunks = realloc(sctp_hdr->chunks, sctp_hdr->chunk_count * sizeof(sctp_chunk_t *));
        if (!sctp_hdr->chunks) {
            free(chunk->data);
            free(chunk);
            break;
        }
        sctp_hdr->chunks[sctp_hdr->chunk_count - 1] = chunk;

        offset += chunk_length;
    }

    layer->parsed_data = sctp_hdr;
    layer->to_json = sctp_to_json;

    return 1;
}

#define JSON_BUFFER_SIZE 4096
static _Thread_local char json_buffer[JSON_BUFFER_SIZE];

char *sctp_to_json(layer_t *layer) {
    if (!layer || !layer->parsed_data) return NULL;

    sctp_header_t *sctp_hdr = (sctp_header_t *) layer->parsed_data;
    uint32_t payload_length = sctp_get_payload_length(sctp_hdr);
    uint32_t header_length = sctp_get_header_length(sctp_hdr);

    int bytes_written = snprintf(json_buffer, JSON_BUFFER_SIZE,
                                 "\"sctp\": { "
                                 "\"sctp_sctp_srcport\": %u, "
                                 "\"sctp_sctp_dstport\": %u, "
                                 "\"sctp_sctp_port\": [%u, %u], "
                                 "\"sctp_sctp_verification_tag\": \"0x%08x\", "
                                 "\"sctp_sctp_checksum\": \"0x%08x\", "
                                 "\"sctp_sctp_chunk_count\": %u, "
                                 "\"sctp_sctp_payload_length\": %u, "
                                 "\"sctp_sctp_header_length\": %u, "
                                 "\"sctp_sctp_chunks\": [",
                                 sctp_hdr->src_port, sctp_hdr->dst_port,
                                 sctp_hdr->src_port, sctp_hdr->dst_port,
                                 sctp_hdr->verification_tag,
                                 sctp_hdr->checksum,
                                 sctp_hdr->chunk_count,
                                 payload_length,
                                 header_length);

    if (bytes_written < 0 || bytes_written >= JSON_BUFFER_SIZE) return NULL;

    for (int i = 0; i < sctp_hdr->chunk_count; i++) {
        sctp_chunk_t *chunk = sctp_hdr->chunks[i];
        bytes_written += snprintf(json_buffer + bytes_written, JSON_BUFFER_SIZE - bytes_written,
                                  "%s{\"type\": %u, \"flags\": \"0x%02x\", \"length\": %u}",
                                  i > 0 ? ", " : "", chunk->type, chunk->flags, chunk->length);
        if (bytes_written >= JSON_BUFFER_SIZE) return NULL;
    }

    bytes_written += snprintf(json_buffer + bytes_written, JSON_BUFFER_SIZE - bytes_written, "]}");
    if (bytes_written >= JSON_BUFFER_SIZE) return NULL;

    return json_buffer;
}

void sctp_layer_free(layer_t *layer) {
    if (!layer || !layer->parsed_data) return;

    sctp_header_t *sctp_hdr = (sctp_header_t *)layer->parsed_data;
    for (int i = 0; i < sctp_hdr->chunk_count; i++) {
        free(sctp_hdr->chunks[i]->data);
        free(sctp_hdr->chunks[i]);
    }
    free(sctp_hdr->chunks);
    free(sctp_hdr);
    layer->parsed_data = NULL;
}
