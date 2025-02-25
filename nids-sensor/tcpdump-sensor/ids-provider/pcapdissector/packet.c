#include "ids-provider/common-util.h"
#include "packet.h"
#include "layer.h"
#include <ethernet-layer.h>

#include <stdlib.h>
#include <stdio.h>
#include <string.h>


#define PACKET_POOL_SIZE 100
static packet_t packet_pool[PACKET_POOL_SIZE];
static int available_packets[PACKET_POOL_SIZE] = {0};

packet_t* get_packet_from_pool() {
    for (int i = 0; i < PACKET_POOL_SIZE; i++) {
        if (available_packets[i] == 0) {
            available_packets[i] = 1;
            return &packet_pool[i];
        }
    }
    return NULL; // Pool exhausted
}

/* Create a new packet structure */
packet_t* packet_create(const uint8_t* data, const struct pcap_pkthdr *pkt_hdr, int linktype) {
    packet_t* pkt = get_packet_from_pool();
    if (!pkt) {
        return NULL;
    }
    memcpy(&pkt->pkthdr, pkt_hdr, sizeof(struct pcap_pkthdr));
    memcpy(pkt->raw_data, data, pkt_hdr->caplen);
    pkt->len = pkt_hdr->caplen;
    pkt->num_layers = 0;

    if (!determine_first_layer(linktype, pkt, data, pkt_hdr->caplen)) {
        return NULL;
    }

    return pkt;
}

/* Free the packet structure */
void packet_destroy(packet_t* pkt) {
    if (!pkt) return;

    // Free each layer
    for (int i = 0; i < pkt->num_layers; i++) {
        layer_free(&pkt->layers[i]);
    }

    // Reset the packet for reuse
    pkt->len = 0;
    pkt->num_layers = 0;
    memset(&pkt->pkthdr, 0, sizeof(struct pcap_pkthdr));

    // Return the packet to the pool
    const ptrdiff_t index = pkt - packet_pool;
    if (index >= 0 && index < PACKET_POOL_SIZE) {
        available_packets[index] = 0;
    }
}


int determine_first_layer(int linktype, packet_t* pkt, const uint8_t* data, size_t len) {
    if (!pkt || !data || len == 0) {
        fprintf(stderr, "Invalid parameters to determine_first_layer\n");
        return 0;
    }

    /* Initialize the first layer by matching the linktype with a handler in the unified handlers array */
    for (int i = 0; handlers[i].protocol_name != NULL; i++) {
        if (handlers[i].id == linktype) { // Match DLT and ensure it's a DLT handler
            pkt->num_layers = 1;
            layer_t* first_layer = &pkt->layers[0];
            first_layer->protocol_name = handlers[i].protocol_name;
            first_layer->dissect = handlers[i].dissect;

            /* Call the layer-specific dissection function */
            int result = first_layer->dissect(first_layer, pkt, data, len);

            if (result == 0 && pkt->num_layers == 1) {
                // If no additional layers were added, the dissection failed entirely
                fprintf(stderr, "Failed to dissect the first layer: %s\n", handlers[i].protocol_name);
                pkt->num_layers = 0;
                return 0;
            }

            return 1; /* Success */
        }
    }

    /* No matching handler found for the given linktype */
    fprintf(stderr, "Unsupported linktype: %d\n", linktype);
    return 0;
}

#define JSON_BUFFER_SIZE 131072  // 65536 + 65536
static _Thread_local char json_buffer[JSON_BUFFER_SIZE];

char* packet_to_json(packet_t* packet) {
    if (!packet || packet->num_layers == 0) return NULL;

    json_buffer[0] = '\0';  // Start with an empty string
    size_t remaining_space = JSON_BUFFER_SIZE - 1;  // Leave space for null terminator
    int first_layer = 1;  // Used to track the first valid JSON layer

    for (int i = 0; i < packet->num_layers && remaining_space > 0; i++) {
        layer_t* current_layer = &packet->layers[i];
        char* layer_json = current_layer->to_json ? current_layer->to_json(current_layer) : NULL;

        if (layer_json) {
            size_t layer_json_len = strlen(layer_json);
            if (layer_json_len <= 0) {
                fprintf(stderr, "JSON of layer %s is empty\n", current_layer->protocol_name);
                continue;
            }

            // If not the first valid layer, append a comma before adding this JSON
            if (!first_layer && remaining_space > 2) {
                strncat(json_buffer, ",", remaining_space);
                remaining_space -= 1;
            }

            // Append the JSON, ensuring it fits
            if (layer_json_len < remaining_space) {
                strncat(json_buffer, layer_json, remaining_space);
                remaining_space -= layer_json_len;
            } else {
                strncat(json_buffer, layer_json, remaining_space - 5);
                strcat(json_buffer, "\"...\"");
                remaining_space = 0;
            }

            first_layer = 0; // The first valid JSON has been added
        } else {
            fprintf(stderr, "JSON of layer %s is empty\n", current_layer->protocol_name);
        }
    }

    return json_buffer;
}


#define MAX_PROTOCOL_CHAIN_LENGTH 256
char* build_protocol_chain(packet_t* pkt, int dlt) {
    static _Thread_local char protocol_chain[MAX_PROTOCOL_CHAIN_LENGTH];

    if (!pkt || pkt->num_layers == 0) {
        return ""; // Return an empty string if no valid packet
    }

    protocol_chain[0] = '\0'; // Start with an empty string
    size_t remaining_space = MAX_PROTOCOL_CHAIN_LENGTH - 1; // -1 for null terminator

    for (int i = 0; i < pkt->num_layers && remaining_space > 0; i++) {
        layer_t* current_layer = &pkt->layers[i];

        if (!current_layer->protocol_name) {
            current_layer->protocol_name = "Unknown";
        }

        size_t name_length = strlen(current_layer->protocol_name);
        if (name_length + 1 > remaining_space) { // +1 for ':' or null terminator
            // Not enough space for this protocol name, truncate
            strncat(protocol_chain, current_layer->protocol_name, remaining_space - 1);
            protocol_chain[MAX_PROTOCOL_CHAIN_LENGTH - 1] = '\0';
            break;
        }

        // Append the protocol name
        strcat(protocol_chain, current_layer->protocol_name);
        remaining_space -= name_length;

        if (i < pkt->num_layers - 1 && remaining_space > 1) {
            strcat(protocol_chain, ":");
            remaining_space--;
        }
    }

    return protocol_chain;
}