#include "ssdp-layer.h"
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

int dissect_ssdp(layer_t *layer, packet_t *packet, const uint8_t *data, size_t len) {
    if (len < 16) {
        fprintf(stderr, "Insufficient data for SSDP dissection\n");
        return 0;
    }

    ssdp_header_t *ssdp_hdr = (ssdp_header_t *)calloc(1, sizeof(ssdp_header_t));
    if (!ssdp_hdr) {
        fprintf(stderr, "Failed to allocate memory for SSDP header\n");
        return 0;
    }

    // Adjusted header termination search
    const uint8_t* end_of_headers = memmem(data, len, "\r\n\r\n", 4);
    if (!end_of_headers) {
        end_of_headers = memmem(data, len, "\n\n", 2); // Handle SSDP request
    }

    if (!end_of_headers) {
        fprintf(stderr, "Invalid SSDP message: no valid header termination found\n");
        free(ssdp_hdr);
        return 0;
    }

    size_t headers_len = end_of_headers - data + 2; // Now using \n\n detection
    char *headers = malloc(headers_len + 1);
    if (!headers) {
        fprintf(stderr, "Failed to allocate memory for SSDP headers\n");
        free(ssdp_hdr);
        return 0;
    }

    memcpy(headers, data, headers_len);
    headers[headers_len] = '\0';

    char *saveptr;
    char *line = strtok_r(headers, "\r\n", &saveptr);
    if (!line) {
        fprintf(stderr, "Failed to parse SSDP first line\n");
        free(headers);
        free(ssdp_hdr);
        return 0;
    }

    if (strncmp(line, "HTTP/1.1 ", 9) == 0) {
        ssdp_hdr->is_request = 0;
        sscanf(line, "HTTP/1.1 %d", &ssdp_hdr->status_code);
    } else {
        ssdp_hdr->is_request = 1;
        char *method = strtok_r(line, " ", &saveptr);
        char *uri = strtok_r(NULL, " ", &saveptr);
        char *http_version = strtok_r(NULL, " ", &saveptr);

        if (method && uri && http_version) {
            snprintf(ssdp_hdr->method, sizeof(ssdp_hdr->method), "%s", method);
            snprintf(ssdp_hdr->uri, sizeof(ssdp_hdr->uri), "%s", uri);
        } else {
            fprintf(stderr, "Malformed SSDP request\n");
            free(headers);
            free(ssdp_hdr);
            return 0;
        }
    }

    while ((line = strtok_r(NULL, "\r\n", &saveptr)) != NULL) {
        if (strncasecmp(line, "HOST:", 5) == 0)
            snprintf(ssdp_hdr->host, sizeof(ssdp_hdr->host), "%s", line + 6);
        else if (strncasecmp(line, "NT:", 3) == 0)
            snprintf(ssdp_hdr->nt, sizeof(ssdp_hdr->nt), "%s", line + 4);
        else if (strncasecmp(line, "NTS:", 4) == 0)
            snprintf(ssdp_hdr->nts, sizeof(ssdp_hdr->nts), "%s", line + 5);
        else if (strncasecmp(line, "USN:", 4) == 0)
            snprintf(ssdp_hdr->usn, sizeof(ssdp_hdr->usn), "%s", line + 5);
        else if (strncasecmp(line, "LOCATION:", 9) == 0)
            snprintf(ssdp_hdr->location, sizeof(ssdp_hdr->location), "%s", line + 10);
        else if (strncasecmp(line, "CACHE-CONTROL:", 14) == 0)
            sscanf(line + 15, "max-age=%d", &ssdp_hdr->max_age);
        else if (strncasecmp(line, "ST:", 3) == 0)
            snprintf(ssdp_hdr->st, sizeof(ssdp_hdr->st), "%s", line + 4);
        else if (strncasecmp(line, "EXT:", 4) == 0)
            snprintf(ssdp_hdr->ext, sizeof(ssdp_hdr->ext), "%s", line + 5);
        else if (strncasecmp(line, "SERVER:", 7) == 0)
            snprintf(ssdp_hdr->server, sizeof(ssdp_hdr->server), "%s", line + 8);
    }

    free(headers);
    layer->parsed_data = ssdp_hdr;
    layer->to_json = ssdp_to_json;

    return 1;
}



#define JSON_BUFFER_SIZE 4096
static _Thread_local char json_buffer[JSON_BUFFER_SIZE];

char *ssdp_to_json(layer_t *layer) {
    if (!layer || !layer->parsed_data) return NULL;

    ssdp_header_t *ssdp_hdr = (ssdp_header_t *)layer->parsed_data;

    int bytes_written = snprintf(json_buffer, JSON_BUFFER_SIZE,
        "\"ssdp\": {"
        "\"ssdp.type\": \"%s\","
        "\"ssdp.method\": \"%s\","
        "\"ssdp.uri\": \"%s\","
        "\"ssdp.host\": \"%s\","
        "\"ssdp.nt\": \"%s\","
        "\"ssdp.nts\": \"%s\","
        "\"ssdp.usn\": \"%s\","
        "\"ssdp.location\": \"%s\","
        "\"ssdp.cache_control\": \"max-age=%d\","
        "\"ssdp.status_code\": \"%d\""
        "}",
        ssdp_hdr->is_request ? "Request" : "Response",
        ssdp_hdr->method,
        ssdp_hdr->uri,
        ssdp_hdr->host,
        ssdp_hdr->nt,
        ssdp_hdr->nts,
        ssdp_hdr->usn,
        ssdp_hdr->location,
        ssdp_hdr->max_age,
        ssdp_hdr->status_code
    );

    if (bytes_written < 0 || bytes_written >= JSON_BUFFER_SIZE) {
        fprintf(stderr, "Error: SSDP JSON truncated or formatting failed\n");
        return NULL;
    }

    return json_buffer;
}


void ssdp_layer_free(layer_t *layer) {
    if (!layer) return;
    if (layer->parsed_data) {
        free(layer->parsed_data);
        layer->parsed_data = NULL;
    }
    layer->protocol_name = NULL;
    layer->to_json = NULL;
    layer->dissect = NULL;
}
