//
// Created by Jochen van Waasen on 23.01.25.
//
#include <ids-provider/common-util.h>
#include "ethernet-layer.h"
#include "ids-provider/pcapdissector/layer.h"

#include <packet.h>
#include <stdbool.h>
#include <stdlib.h>
#include <string.h>
#include <stdio.h>
#include <arpa/inet.h>

int dissect_ethernet(layer_t *layer, packet_t *packet, const uint8_t *data, size_t len) {
    if (len < 14) {
        fprintf(stderr, "Insufficient data for Ethernet dissection\n");
        return 0;
    }

    // Allocate memory for Ethernet header
    ethernet_header_t *eth_hdr = (ethernet_header_t *) malloc(sizeof(ethernet_header_t));
    if (!eth_hdr) {
        fprintf(stderr, "Failed to allocate memory for Ethernet header\n");
        return 0;
    }

    // Parse Ethernet header fields
    memcpy(eth_hdr->dest_mac, data, 6);
    memcpy(eth_hdr->src_mac, data + 6, 6);
    eth_hdr->ethertype = ntohs(*(uint16_t *)(data + 12));

    // Ensure Ethernet data is stored
    layer->parsed_data = eth_hdr;
    layer->to_json = ethernet_to_json;

    const uint8_t *payload = data + 14;
    size_t payload_len = len - 14;

    // Handle VLAN tagging (including QinQ)
    while (eth_hdr->ethertype == 0x8100 || eth_hdr->ethertype == 0x88A8) {
        if (payload_len < 4) {
            fprintf(stderr, "Insufficient data for VLAN tag\n");
            free(eth_hdr);
            return 0;
        }

        uint16_t vlan_tci = ntohs(*(uint16_t *)(payload));
        eth_hdr->vlan_id = vlan_tci & 0x0FFF;
        eth_hdr->vlan_priority = (vlan_tci >> 13) & 0x07;
        eth_hdr->ethertype = ntohs(*(uint16_t *)(payload + 2));

        payload += 4;
        payload_len -= 4;
    }

    // Handle LLC (IEEE 802.3)
    if (eth_hdr->ethertype <= 0x05DC) {
        eth_hdr->length = eth_hdr->ethertype; // This is actually the frame length

        // Look up the handler for LLC
        for (int i = 0; handlers[i].protocol_name != NULL; i++) {
            if (handlers[i].id == 0x05DC) {
                layer_t *next_layer = (layer_t *) malloc(sizeof(layer_t));
                if (!next_layer) {
                    fprintf(stderr, "Failed to allocate memory for LLC layer\n");
                    free(eth_hdr);
                    return 0;
                }
                next_layer->protocol_name = handlers[i].protocol_name;
                return handlers[i].dissect(next_layer, packet, payload, payload_len);
            }
        }

        fprintf(stderr, "LLC handler not found\n");
        return 1;
    }

    return process_next_layer(packet, eth_hdr->ethertype, payload, payload_len, handlers);
}

#define JSON_BUFFER_SIZE 4096
static _Thread_local char json_buffer[JSON_BUFFER_SIZE];

char *ethernet_to_json(layer_t *layer) {
    if (!layer || !layer->parsed_data) return NULL;

    ethernet_header_t *eth_hdr = (ethernet_header_t *) layer->parsed_data;

    char src_mac_str[18], dest_mac_str[18];
    mac_to_string(eth_hdr->src_mac, src_mac_str);
    mac_to_string(eth_hdr->dest_mac, dest_mac_str);

    uint32_t src_oui = extract_oui(eth_hdr->src_mac);
    uint32_t dest_oui = extract_oui(eth_hdr->dest_mac);
    const char *src_vendor = lookup_oui_vendor(eth_hdr->src_mac);
    const char *dest_vendor = lookup_oui_vendor(eth_hdr->dest_mac);

    int src_lg = (eth_hdr->src_mac[0] & 0x02) != 0;
    int src_ig = (eth_hdr->src_mac[0] & 0x01) != 0;
    int dest_lg = (eth_hdr->dest_mac[0] & 0x02) != 0;
    int dest_ig = (eth_hdr->dest_mac[0] & 0x01) != 0;

    int bytes_written = snprintf(json_buffer, JSON_BUFFER_SIZE,
                                 "\"eth\":{"
                                 "\"eth_eth_dst\":\"%s\","
                                 "\"eth_eth_dst_resolved\":\"%s\","
                                 "\"eth_eth_dst_oui\":%u,"
                                 "\"eth_eth_dst_oui_resolved\":\"%s\","
                                 "\"eth_eth_dst_lg\":%d,"
                                 "\"eth_eth_dst_ig\":%d,"
                                 "\"eth_eth_src\":\"%s\","
                                 "\"eth_eth_src_resolved\":\"%s\","
                                 "\"eth_eth_src_oui\":%u,"
                                 "\"eth_eth_src_oui_resolved\":\"%s\","
                                 "\"eth_eth_src_lg\":%d,"
                                 "\"eth_eth_src_ig\":%d,"
                                 "\"eth_eth_type\":\"0x%04X\","
                                 "\"eth_eth_len\":%zu,"
                                 "\"eth_eth_stream\":0",
                                 dest_mac_str, dest_vendor, dest_oui, dest_vendor, dest_lg, dest_ig,
                                 src_mac_str, src_vendor, src_oui, src_vendor, src_lg, src_ig,
                                 eth_hdr->ethertype,
                                 sizeof(ethernet_header_t) + (eth_hdr->vlan_id ? 4 : 0));

    if (eth_hdr->vlan_id) {
        bytes_written += snprintf(json_buffer + bytes_written, JSON_BUFFER_SIZE - bytes_written,
                                  ",\"eth_eth_vlan_id\":%u,"
                                  "\"eth_eth_vlan_priority\":%u",
                                  eth_hdr->vlan_id, eth_hdr->vlan_priority);
    }

    strcat(json_buffer, "}");

    return json_buffer;
}


void ethernet_layer_free(layer_t *layer) {
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
}


// Convert a MAC address to a string in the format "xx:xx:xx:xx:xx:xx"
void mac_to_string(const uint8_t mac[6], char out[18]) {
    snprintf(out, 18, "to be implemented");
}

// Extract the OUI (first 3 bytes of the MAC address) as an integer
uint32_t extract_oui(const uint8_t mac[6]) {
    return 0; // Placeholder: Implement actual OUI extraction later
}

// Lookup the vendor name for an OUI (dummy implementation)
const char *lookup_oui_vendor(const uint8_t mac[6]) {
    return "to be implemented";
}
