//
// Created by Jochen van Waasen on 23.01.25.
//

#include "tcp-layer.h"
#include <stdlib.h>
#include <string.h>
#include <stdio.h>
#include <arpa/inet.h>

int dissect_tcp(layer_t* layer, packet_t *packet, const uint8_t* data, size_t len) {
    if (len < 20) { // Minimum TCP header length
        fprintf(stderr, "Insufficient data for TCP dissection\n");
        return 1;
    }

    tcp_header_t* tcp_hdr = (tcp_header_t*)malloc(sizeof(tcp_header_t));
    if (!tcp_hdr) {
        fprintf(stderr, "Failed to allocate memory for TCP header\n");
        return 1;
    }

    // Parse the TCP header
    tcp_hdr->src_port = (data[0] << 8) | data[1];
    tcp_hdr->dst_port = (data[2] << 8) | data[3];
    tcp_hdr->seq_num = (data[4] << 24) | (data[5] << 16) | (data[6] << 8) | data[7];
    tcp_hdr->ack_num = (data[8] << 24) | (data[9] << 16) | (data[10] << 8) | data[11];
    tcp_hdr->data_offset = (data[12] >> 4) * 4; // Header length in bytes
    tcp_hdr->flags = data[13];
    tcp_hdr->window_size = (data[14] << 8) | data[15];
    tcp_hdr->checksum = (data[16] << 8) | data[17];
    tcp_hdr->urgent_pointer = (data[18] << 8) | data[19];

    // Check if there are TCP options
    size_t header_length = tcp_hdr->data_offset;
    if (header_length > 20 && header_length <= len) {
        size_t options_len = header_length - 20;
        tcp_hdr->options = (uint8_t*)malloc(options_len);
        if (!tcp_hdr->options) {
            fprintf(stderr, "Failed to allocate memory for TCP options\n");
            free(tcp_hdr);
            return 1;
        }
        memcpy(tcp_hdr->options, data + 20, options_len);
        tcp_hdr->options_len = options_len;
    } else {
        tcp_hdr->options = NULL;
        tcp_hdr->options_len = 0;
    }

    tcp_hdr->header_length = tcp_hdr->data_offset;
    tcp_hdr->payload_length = len - tcp_hdr->header_length;
    tcp_hdr->tcp_stream = 0; // To be implemented
    tcp_hdr->tcp_len = len;
    tcp_hdr->nxtseq = tcp_hdr->seq_num + tcp_hdr->payload_length;
    tcp_hdr->tcp_analysis = "to be implemented";
    tcp_hdr->time_relative = 0.0; // To be implemented
    tcp_hdr->time_delta = 0.0; // To be implemented

    layer->parsed_data = tcp_hdr;
    layer->to_json = tcp_to_json;

    // TCP doesn't typically have a next layer to dissect
    return 1; // Dissection successful
}

#define JSON_BUFFER_SIZE 4096
static _Thread_local  char json_buffer[JSON_BUFFER_SIZE];
char* tcp_to_json(layer_t* layer) {
    if (!layer || !layer->parsed_data) return NULL;

    tcp_header_t* tcp_hdr = (tcp_header_t*)layer->parsed_data;

    // Format the JSON
    int bytes_written = snprintf(json_buffer, JSON_BUFFER_SIZE,
        "\"tcp\":{ "
        "\"tcp_tcp_src_port\": %u, "
        "\"tcp_tcp_dst_port\": %u, "
        "\"tcp_tcp_seq_num\": %u, "
        "\"tcp_tcp_ack_num\": %u, "
        "\"tcp_tcp_data_offset\": %u, "
        "\"tcp_tcp_flags\": \"%02x\", "
        "\"tcp_tcp_flag_ns\": %d, "
        "\"tcp_tcp_flag_cwr\": %d, "
        "\"tcp_tcp_flag_ece\": %d, "
        "\"tcp_tcp_flag_urg\": %d, "
        "\"tcp_tcp_flag_ack\": %d, "
        "\"tcp_tcp_flag_psh\": %d, "
        "\"tcp_tcp_flag_rst\": %d, "
        "\"tcp_tcp_flag_syn\": %d, "
        "\"tcp_tcp_flag_fin\": %d, "
        "\"tcp_tcp_window_size\": %u, "
        "\"tcp_tcp_checksum\": \"0x%04x\", "
        "\"tcp_tcp_urgent_pointer\": %u, "
        "\"tcp_tcp_payload_length\": %u, "
        "\"tcp_tcp_header_length\": %u, "
        "\"tcp_tcp_stream\": %u, "
        "\"tcp_tcp_len\": %u, "
        "\"tcp_tcp_nxtseq\": %u, "
        "\"tcp_tcp_analysis\": \"%s\", "
        "\"tcp_tcp_time_relative\": %.6f, "
        "\"tcp_tcp_time_delta\": %.6f",
        tcp_hdr->src_port,
        tcp_hdr->dst_port,
        tcp_hdr->seq_num,
        tcp_hdr->ack_num,
        tcp_hdr->data_offset,
        tcp_hdr->flags,
        (tcp_hdr->flags & 0x100) >> 8, // NS
        (tcp_hdr->flags & 0x80) >> 7,  // CWR
        (tcp_hdr->flags & 0x40) >> 6,  // ECE
        (tcp_hdr->flags & 0x20) >> 5,  // URG
        (tcp_hdr->flags & 0x10) >> 4,  // ACK
        (tcp_hdr->flags & 0x08) >> 3,  // PSH
        (tcp_hdr->flags & 0x04) >> 2,  // RST
        (tcp_hdr->flags & 0x02) >> 1,  // SYN
        (tcp_hdr->flags & 0x01),       // FIN
        tcp_hdr->window_size,
        tcp_hdr->checksum,
        tcp_hdr->urgent_pointer,
        tcp_hdr->payload_length,
        tcp_hdr->header_length,
        tcp_hdr->tcp_stream,
        tcp_hdr->tcp_len,
        tcp_hdr->nxtseq,
        tcp_hdr->tcp_analysis,
        tcp_hdr->time_relative,
        tcp_hdr->time_delta);

    if (bytes_written < 0 || bytes_written >= JSON_BUFFER_SIZE) {
        return NULL; // Error or buffer overflow
    }

    int remaining_space = JSON_BUFFER_SIZE - bytes_written;

    // Add TCP options if present
    if (tcp_hdr->options && tcp_hdr->options_len > 0) {
        int options_bytes = snprintf(json_buffer + bytes_written, remaining_space,
                                     ", \"tcp_tcp_options\": \"");

        if (options_bytes < 0 || options_bytes >= remaining_space) {
            return NULL; // Error or buffer overflow
        }

        bytes_written += options_bytes;
        remaining_space -= options_bytes;

        // Convert options to a hex string
        for (size_t i = 0; i < tcp_hdr->options_len && remaining_space > 2; i++) {
            options_bytes = snprintf(json_buffer + bytes_written, remaining_space,
                                     "%02x", tcp_hdr->options[i]);

            if (options_bytes < 0 || options_bytes >= remaining_space) {
                return NULL; // Error or buffer overflow
            }

            bytes_written += options_bytes;
            remaining_space -= options_bytes;
        }

        // Close the options string
        if (remaining_space > 2) {
            strcat(json_buffer + bytes_written, "\"");
            bytes_written += 1;
            remaining_space -= 1;
        } else {
            return NULL; // Not enough space to close the string
        }
    }

    // Close JSON object
    if (remaining_space > 2) {
        strcat(json_buffer + bytes_written, " }");
    } else {
        return NULL; // Not enough space to close the object
    }
    return json_buffer;
}

void tcp_layer_free(layer_t* layer) {
    if (!layer) return;

    // Free parsed data if allocated
    if (layer->parsed_data) {
        free(layer->parsed_data);
    }
}



