#include "ntp-layer.h"
#include <stdio.h>
#include <string.h>

#define JSON_BUFFER_SIZE 4096
static _Thread_local char json_buffer[JSON_BUFFER_SIZE];

int dissect_ntp(layer_t *layer, packet_t* packet, const uint8_t *data, size_t len) {
    if (!layer || !data || len < sizeof(ntp_header_t)) {
        fprintf(stderr, "Insufficient data for NTP dissection\n");
        return 1;
    }

    ntp_header_t *ntp_hdr = (ntp_header_t *) malloc(sizeof(ntp_header_t));
    if (!ntp_hdr) {
        fprintf(stderr, "Failed to allocate memory for NTP header\n");
        return 1;
    }

    memcpy(ntp_hdr, data, sizeof(ntp_header_t));

    layer->parsed_data = ntp_hdr;
    layer->to_json = ntp_to_json;

    return 1;
}

uint64_t custom_be64toh(uint64_t big_endian_64bits) {
    uint64_t result = 0;
    for (int i = 0; i < 8; ++i) {
        result = (result << 8) | ((big_endian_64bits >> (i * 8)) & 0xFF);
    }
    return result;
}

char *ntp_to_json(layer_t *layer) {
    if (!layer || !layer->parsed_data) return NULL;

    ntp_header_t *ntp_hdr = (ntp_header_t *) layer->parsed_data;

    int bytes_written = snprintf(json_buffer, JSON_BUFFER_SIZE,
        "\"ntp\": {"
        "\"ntp.flags\": \"0x%02X\","
        "\"ntp.stratum\": \"%u\","
        "\"ntp.poll\": \"%d\","
        "\"ntp.precision\": \"%d\","
        "\"ntp.root_delay\": \"%u\","
        "\"ntp.root_dispersion\": \"%u\","
        "\"ntp.ref_id\": \"0x%08X\","
        "\"ntp.ref_timestamp\": \"%llu\","
        "\"ntp.orig_timestamp\": \"%llu\","
        "\"ntp.recv_timestamp\": \"%llu\","
        "\"ntp.tx_timestamp\": \"%llu\""
        "}",
        ntp_hdr->li_vn_mode,
        ntp_hdr->stratum,
        ntp_hdr->poll,
        ntp_hdr->precision,
        ntohl(ntp_hdr->root_delay),
        ntohl(ntp_hdr->root_dispersion),
        ntohl(ntp_hdr->reference_id),
        (unsigned long long)custom_be64toh(ntp_hdr->reference_timestamp),
        (unsigned long long)custom_be64toh(ntp_hdr->origin_timestamp),
        (unsigned long long)custom_be64toh(ntp_hdr->receive_timestamp),
        (unsigned long long)custom_be64toh(ntp_hdr->transmit_timestamp)
    );

    if (bytes_written < 0 || bytes_written >= JSON_BUFFER_SIZE) {
        fprintf(stderr, "Error: NTP JSON truncated or formatting failed\n");
        return NULL;
    }

    return json_buffer;
}

void ntp_layer_free(layer_t *layer) {
    if (!layer) return;
    if (layer->parsed_data) {
        free(layer->parsed_data);
    }
}
