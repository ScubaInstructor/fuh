//
// Created by Jochen van Waasen on 23.01.25.
//

#include "arp-layer.h"
#include <stdlib.h>
#include <string.h>
#include <stdio.h>

int dissect_arp(layer_t* layer, packet_t *packet, const uint8_t* data, size_t len) {
    // Minimum ARP header length is 28 bytes
    if (len < 28) {
        fprintf(stderr, "Insufficient data for ARP dissection (length: %zu bytes)\n", len);
        return 1;
    }

    // Allocate memory for ARP header
    arp_header_t* arp_hdr = (arp_header_t*)malloc(sizeof(arp_header_t));
    if (!arp_hdr) {
        fprintf(stderr, "Failed to allocate memory for ARP header\n");
        return 1;
    }

    // Parse ARP header fields
    arp_hdr->hardware_type = (data[0] << 8) | data[1];
    arp_hdr->protocol_type = (data[2] << 8) | data[3];
    arp_hdr->hardware_size = data[4];
    arp_hdr->protocol_size = data[5];
    arp_hdr->opcode = (data[6] << 8) | data[7];

    memcpy(arp_hdr->sender_mac, data + 8, 6);    // Sender MAC
    memcpy(arp_hdr->sender_ip, data + 14, 4);   // Sender IP
    memcpy(arp_hdr->target_mac, data + 18, 6);  // Target MAC
    memcpy(arp_hdr->target_ip, data + 24, 4);   // Target IP

    // Log parsed ARP fields
    /*fprintf(stderr, "ARP Dissected: Opcode=%u, Sender MAC=%02X:%02X:%02X:%02X:%02X:%02X, "
                    "Sender IP=%u.%u.%u.%u, Target MAC=%02X:%02X:%02X:%02X:%02X:%02X, "
                    "Target IP=%u.%u.%u.%u\n",
            arp_hdr->opcode,
            arp_hdr->sender_mac[0], arp_hdr->sender_mac[1], arp_hdr->sender_mac[2],
            arp_hdr->sender_mac[3], arp_hdr->sender_mac[4], arp_hdr->sender_mac[5],
            arp_hdr->sender_ip[0], arp_hdr->sender_ip[1], arp_hdr->sender_ip[2], arp_hdr->sender_ip[3],
            arp_hdr->target_mac[0], arp_hdr->target_mac[1], arp_hdr->target_mac[2],
            arp_hdr->target_mac[3], arp_hdr->target_mac[4], arp_hdr->target_mac[5],
            arp_hdr->target_ip[0], arp_hdr->target_ip[1], arp_hdr->target_ip[2], arp_hdr->target_ip[3]);
            */

    // Store the parsed ARP header in the layer
    layer->parsed_data = arp_hdr;
    layer->to_json = arp_to_json;

    // Check for additional payload
    const uint8_t* payload = data + 28;
    size_t payload_len = len - 28;

    if (payload_len > 0) {
        // Check if this is padding (all zeros)
        int is_padding = 1;
        for (size_t i = 0; i < payload_len; i++) {
            if (payload[i] != 0) {
                is_padding = 0;
                break;
            }
        }

        if (is_padding) {
            //fprintf(stderr, "ARP Dissection: Detected Ethernet padding (%zu bytes). Ignoring.\n", payload_len);
        } else {
            fprintf(stderr, "Unknown ARP payload detected (%zu bytes). No further dissection available.\n", payload_len);
        }
    }

    return 1;
}

#define JSON_BUFFER_SIZE 4096
static _Thread_local  char json_buffer[JSON_BUFFER_SIZE];
char* arp_to_json(layer_t* layer) {
    if (!layer || !layer->parsed_data) return NULL;

    arp_header_t* arp_hdr = (arp_header_t*)layer->parsed_data;

    // Format the ARP header fields into a JSON object
    int bytes_written = snprintf(json_buffer, JSON_BUFFER_SIZE,
             "\"arp\": {"
             "\"arp.hardware_type\": \"0x%04X\","
             "\"arp.protocol_type\": \"0x%04X\","
             "\"arp.hardware_size\": \"%u\","
             "\"arp.protocol_size\": \"%u\","
             "\"arp.opcode\": \"%u\","
             "\"arp.sender_mac\": \"%02X:%02X:%02X:%02X:%02X:%02X\","
             "\"arp.sender_ip\": \"%u.%u.%u.%u\","
             "\"arp.target_mac\": \"%02X:%02X:%02X:%02X:%02X:%02X\","
             "\"arp.target_ip\": \"%u.%u.%u.%u\""
             "}",
             arp_hdr->hardware_type,
             arp_hdr->protocol_type,
             arp_hdr->hardware_size,
             arp_hdr->protocol_size,
             arp_hdr->opcode,
             arp_hdr->sender_mac[0], arp_hdr->sender_mac[1], arp_hdr->sender_mac[2],
             arp_hdr->sender_mac[3], arp_hdr->sender_mac[4], arp_hdr->sender_mac[5],
             arp_hdr->sender_ip[0], arp_hdr->sender_ip[1], arp_hdr->sender_ip[2], arp_hdr->sender_ip[3],
             arp_hdr->target_mac[0], arp_hdr->target_mac[1], arp_hdr->target_mac[2],
             arp_hdr->target_mac[3], arp_hdr->target_mac[4], arp_hdr->target_mac[5],
             arp_hdr->target_ip[0], arp_hdr->target_ip[1], arp_hdr->target_ip[2], arp_hdr->target_ip[3]);

    if (bytes_written < 0 || bytes_written >= JSON_BUFFER_SIZE) {
        // Error or truncation occurred
        fprintf(stderr, "Error: ARP JSON truncated or formatting failed\n");
        return NULL;
    }

    return json_buffer;
}

void arp_layer_free(layer_t* layer) {
    if (!layer) return;

    // Free the parsed data (ARP header)
    if (layer->parsed_data) {
        free(layer->parsed_data);
    }
}



