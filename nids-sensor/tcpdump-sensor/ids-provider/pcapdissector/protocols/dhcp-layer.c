#include "dhcp-layer.h"
#include <stdio.h>
#include <string.h>

#define JSON_BUFFER_SIZE 4096
static _Thread_local char json_buffer[JSON_BUFFER_SIZE];

dhcp_options_t *parse_dhcp_options(const uint8_t *options, size_t len) {
    dhcp_options_t *dhcp_options = (dhcp_options_t *) malloc(sizeof(dhcp_options_t));
    if (!dhcp_options) {
        fprintf(stderr, "Failed to allocate memory for DHCP options\n");
        return NULL;
    }
    memset(dhcp_options, 0, sizeof(dhcp_options_t));

    size_t offset = 0;
    while (offset < len) {
        uint8_t option_type = options[offset++];
        if (option_type == 255) break; // End option
        if (option_type == 0) continue; // Pad option

        uint8_t option_len = options[offset++];
        if (offset + option_len > len) break; // Malformed option

        switch (option_type) {
            case 1: // Subnet Mask
                memcpy(dhcp_options->subnet_mask, &options[offset], 4);
            break;
            case 3: // Router
                memcpy(dhcp_options->router, &options[offset], 4);
            break;
            case 6: // Domain Name Server
                memcpy(dhcp_options->dns, &options[offset], 4);
            break;
            case 51: // IP Address Lease Time
                dhcp_options->lease_time = ntohl(*(uint32_t *)&options[offset]);
            break;
            case 53: // DHCP Message Type
                dhcp_options->message_type = options[offset];
            break;
            case 54: // Server Identifier
                memcpy(dhcp_options->server_id, &options[offset], 4);
            break;
            // Add more option parsing as needed
        }
        offset += option_len;
    }

    return dhcp_options;
}

int dissect_dhcp(layer_t *layer, packet_t* packet, const uint8_t *data, size_t len) {
    if (!layer || !data || len < sizeof(dhcp_header_t)) {
        fprintf(stderr, "Insufficient data for DHCP dissection\n");
        return 1;
    }

    dhcp_header_t *dhcp_hdr = (dhcp_header_t *) malloc(sizeof(dhcp_header_t));
    if (!dhcp_hdr) {
        fprintf(stderr, "Failed to allocate memory for DHCP header\n");
        return 1;
    }

    memcpy(dhcp_hdr, data, sizeof(dhcp_header_t));

    layer->parsed_data = dhcp_hdr;
    layer->to_json = dhcp_to_json;

    // Parse DHCP options
    const uint8_t *options = data + sizeof(dhcp_header_t);
    size_t options_len = len - sizeof(dhcp_header_t);
    dhcp_hdr->options = parse_dhcp_options(options, options_len);

    return 1;
}

char *dhcp_to_json(layer_t *layer) {
    if (!layer || !layer->parsed_data) return NULL;

    dhcp_header_t *dhcp_hdr = (dhcp_header_t *) layer->parsed_data;
    dhcp_options_t *options = dhcp_hdr->options;

    int bytes_written = snprintf(json_buffer, JSON_BUFFER_SIZE,
        "\"dhcp\": {"
        "\"dhcp.op\": \"%u\","
        "\"dhcp.htype\": \"%u\","
        "\"dhcp.hlen\": \"%u\","
        "\"dhcp.hops\": \"%u\","
        "\"dhcp.xid\": \"0x%08X\","
        "\"dhcp.secs\": \"%u\","
        "\"dhcp.flags\": \"0x%04X\","
        "\"dhcp.ciaddr\": \"%u.%u.%u.%u\","
        "\"dhcp.yiaddr\": \"%u.%u.%u.%u\","
        "\"dhcp.siaddr\": \"%u.%u.%u.%u\","
        "\"dhcp.giaddr\": \"%u.%u.%u.%u\","
        "\"dhcp.options\": {"
        "\"dhcp.option.subnet_mask\": \"%u.%u.%u.%u\","
        "\"dhcp.option.router\": \"%u.%u.%u.%u\","
        "\"dhcp.option.dns\": \"%u.%u.%u.%u\","
        "\"dhcp.option.lease_time\": \"%u\","
        "\"dhcp.option.message_type\": \"%u\","
        "\"dhcp.option.server_id\": \"%u.%u.%u.%u\""
        "}"
        "}",
        dhcp_hdr->op, dhcp_hdr->htype, dhcp_hdr->hlen, dhcp_hdr->hops,
        dhcp_hdr->xid, dhcp_hdr->secs, dhcp_hdr->flags,
        (dhcp_hdr->ciaddr >> 24) & 0xFF, (dhcp_hdr->ciaddr >> 16) & 0xFF,
        (dhcp_hdr->ciaddr >> 8) & 0xFF, dhcp_hdr->ciaddr & 0xFF,
        (dhcp_hdr->yiaddr >> 24) & 0xFF, (dhcp_hdr->yiaddr >> 16) & 0xFF,
        (dhcp_hdr->yiaddr >> 8) & 0xFF, dhcp_hdr->yiaddr & 0xFF,
        (dhcp_hdr->siaddr >> 24) & 0xFF, (dhcp_hdr->siaddr >> 16) & 0xFF,
        (dhcp_hdr->siaddr >> 8) & 0xFF, dhcp_hdr->siaddr & 0xFF,
        (dhcp_hdr->giaddr >> 24) & 0xFF, (dhcp_hdr->giaddr >> 16) & 0xFF,
        (dhcp_hdr->giaddr >> 8) & 0xFF, dhcp_hdr->giaddr & 0xFF,
        options->subnet_mask[0], options->subnet_mask[1], options->subnet_mask[2], options->subnet_mask[3],
        options->router[0], options->router[1], options->router[2], options->router[3],
        options->dns[0], options->dns[1], options->dns[2], options->dns[3],
        options->lease_time,
        options->message_type,
        options->server_id[0], options->server_id[1], options->server_id[2], options->server_id[3]
    );

    if (bytes_written < 0 || bytes_written >= JSON_BUFFER_SIZE) {
        fprintf(stderr, "Error: DHCP JSON truncated or formatting failed\n");
        return NULL;
    }

    return json_buffer;
}


void dhcp_layer_free(layer_t *layer) {
    if (!layer) return;
    if (layer->parsed_data) {
        free(layer->parsed_data);
    }
}
