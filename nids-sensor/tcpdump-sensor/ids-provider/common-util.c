#include "common-util.h"
#include "yaml-processor.h"

#include <string.h>
#include <stdlib.h>
#include <netdissect-alloc.h>

int write_unsupported_pcap = 0;

const char* get_option_value(struct kv_pair* pairs, size_t pairs_count, const char* search_key) {
    for (size_t i = 0; i < pairs_count; i++) {
        if (strcmp(pairs[i].key, search_key) == 0) {
            return pairs[i].value;
        }
    }
    return NULL; // Not found
}

struct kv_pair* load_yaml_config(netdissect_options *ndo, const char* config_file, size_t* count) {
    if (!config_file) {
        fprintf(stderr, "No config file specified.\n");
        *count = 0;
        return NULL;
    }

    // Load and parse YAML file using the bridge function
    int lineCount;
    char** yamlLines = loadYamlFile(config_file, &lineCount);
    if (!yamlLines) {
        fprintf(stderr, "Failed to load YAML file: %s\n", config_file);
        *count = 0;
        return NULL;
    }

    // Flatten the YAML structure into key-value pairs
    int pairCount = 0;
    struct kv_pair* pairs = flattenYamlNode(yamlLines, lineCount, &pairCount);
    if (!pairs) {
        fprintf(stderr, "Failed to flatten YAML structure.\n");
        *count = 0;
        free(yamlLines);
        return NULL;
    }

    // Allocate memory for the kv_pair array using nd_malloc
    struct kv_pair* arr = (struct kv_pair*)nd_malloc(ndo, sizeof(struct kv_pair) * pairCount);
    if (!arr) {
        fprintf(stderr, "Memory allocation failed using nd_malloc.\n");
        freeKvPairs(pairs, pairCount);
        free(yamlLines);
        *count = 0;
        return NULL;
    }

    // Copy the pairs into the new array
    for (int i = 0; i < pairCount; i++) {
        arr[i].key = pairs[i].key;     // Reuse pointers for strings
        arr[i].value = pairs[i].value; // Reuse pointers for strings
    }

    // Clean up the original pairs array and YAML node
    free(pairs);
    free(yamlLines);

    // Set the output count and return the allocated array
    *count = pairCount;

    // we need that parameter here
    // loadyaml has to be executed, so we can rely on that
    const char* write_unsupported_pcap_str = get_option_value(arr, *count, "dissect.write_unsupported_pcap");
    write_unsupported_pcap = (write_unsupported_pcap_str != NULL &&
                           (strcmp(write_unsupported_pcap_str, "true") == 0 ||
                            strcmp(write_unsupported_pcap_str, "1") == 0)) ? 1 : 0;

    return arr;
}

void write_packet_to_pcap(const char* filename, const struct pcap_pkthdr* pkt_hdr, const uint8_t* pkt_data) {
    if (!filename || !pkt_hdr || !pkt_data) {
        fprintf(stderr, "Invalid arguments to write_packet_to_pcap\n");
        return;
    }

    // Open the file for writing
    FILE* pcap_file = fopen(filename, "ab"); // Open in append mode to preserve existing packets
    if (!pcap_file) {
        fprintf(stderr, "Failed to open pcap file for writing: %s\n", filename);
        return;
    }

    // Create a pcap handle using pcap_open_dead
    char errbuf[PCAP_ERRBUF_SIZE];
    pcap_t* pcap_handle = pcap_open_dead(DLT_EN10MB, 65535); // Ethernet link layer
    if (!pcap_handle) {
        fprintf(stderr, "Failed to create pcap handle\n");
        fclose(pcap_file);
        return;
    }

    // Create a pcap dumper to write to the file
    pcap_dumper_t* pcap_dumper = pcap_dump_fopen(pcap_handle, pcap_file);
    if (!pcap_dumper) {
        fprintf(stderr, "Failed to create pcap dumper\n");
        fclose(pcap_file);
        pcap_close(pcap_handle);
        return;
    }

    // Write the packet to the file
    pcap_dump((u_char*)pcap_dumper, pkt_hdr, pkt_data);

    // Clean up
    pcap_dump_close(pcap_dumper);
    pcap_close(pcap_handle);
    fclose(pcap_file);
}

void generate_timestamped_filename(const char* base_filename, char* buffer, size_t buffer_size) {
    if (!base_filename || strlen(base_filename) == 0) {
        snprintf(buffer, buffer_size, "default-%ld", time(NULL)); // Fallback to default name
        return;
    }

    time_t now = time(NULL);
    struct tm* t = localtime(&now);

    // Extract base name and extension
    const char* dot = strrchr(base_filename, '.'); // Find last dot
    size_t base_length = dot ? (dot - base_filename) : strlen(base_filename);
    const char* extension = dot ? dot : "";

    // Format timestamped filename
    snprintf(buffer, buffer_size, "%.*s-%04d%02d%02d-%02d%02d%02d%s",
             (int)base_length, base_filename, // Base name
             t->tm_year + 1900, t->tm_mon + 1, t->tm_mday, // Date
             t->tm_hour, t->tm_min, t->tm_sec, // Time
             extension); // File extension
}

#include <stdint.h>
#include <stdlib.h>
#include <string.h>
#include <stdio.h>

// Function to encode data in Base64
char* base64_encode(const unsigned char* data, size_t input_length) {
    static const char encoding_table[] = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789+/";
    size_t output_length = 4 * ((input_length + 2) / 3);
    char* encoded_data = malloc(output_length + 1); // +1 for null terminator
    if (!encoded_data) return NULL;

    for (size_t i = 0, j = 0; i < input_length;) {
        uint32_t octet_a = i < input_length ? data[i++] : 0;
        uint32_t octet_b = i < input_length ? data[i++] : 0;
        uint32_t octet_c = i < input_length ? data[i++] : 0;

        uint32_t triple = (octet_a << 16) | (octet_b << 8) | octet_c;

        encoded_data[j++] = encoding_table[(triple >> 18) & 0x3F];
        encoded_data[j++] = encoding_table[(triple >> 12) & 0x3F];
        encoded_data[j++] = (i > input_length + 1) ? '=' : encoding_table[(triple >> 6) & 0x3F];
        encoded_data[j++] = (i > input_length) ? '=' : encoding_table[triple & 0x3F];
    }

    encoded_data[output_length] = '\0'; // Null-terminate the string
    return encoded_data;
}

char* encode_packet_to_base64(const struct pcap_pkthdr* pkt_hdr, const uint8_t* pkt_data) {
    if (!pkt_hdr || !pkt_data) {
        return NULL;
    }

    size_t output_size;
    uint8_t* pcap_binary = create_pcap_binary(pkt_hdr, pkt_data, &output_size);
    if (!pcap_binary) {
        return NULL;
    }

    FILE* file = fopen("output.pcap", "wb"); if (file) { fwrite(pcap_binary, 1, output_size, file); fclose(file); }

    // Encode the PCAP binary to Base64
    char* base64_result = base64_encode(pcap_binary, output_size);

    // Free the PCAP binary buffer
    free(pcap_binary);

    return base64_result; // Return Base64 encoded string
}

// Define PCAP Global Header
static const struct pcap_global_header PCAP_GLOBAL_HEADER = {
    .magic_number = 0xa1b2c3d4,  // Standard magic number (little-endian)
    .version_major = 2,          // PCAP version 2.4
    .version_minor = 4,
    .thiszone = 0,               // GMT time zone offset
    .sigfigs = 0,                // No timestamp accuracy
    .snaplen = 65535,            // Max packet size
    .network = 1                 // Ethernet (DLT_EN10MB)
};

uint8_t* create_pcap_binary(const struct pcap_pkthdr* pkt_hdr, const uint8_t* pkt_data, size_t* output_size) {
    if (!pkt_hdr || !pkt_data || output_size == NULL) {
        return NULL;
    }

    // Sizes
    size_t global_header_size = sizeof(PCAP_GLOBAL_HEADER);
    size_t packet_header_size = sizeof(struct pcap_packet_header);
    size_t packet_data_size = pkt_hdr->caplen;

    *output_size = global_header_size + packet_header_size + packet_data_size;

    // Allocate memory for the PCAP binary
    uint8_t* pcap_binary = malloc(*output_size);
    if (!pcap_binary) {
        return NULL;
    }

    size_t offset = 0;

    // Write the global header (ONLY if this is a standalone PCAP file)
    memcpy(pcap_binary + offset, &PCAP_GLOBAL_HEADER, global_header_size);
    offset += global_header_size;

    // Convert libpcap's pcap_pkthdr to PCAP Packet Header format
    struct pcap_packet_header pkt_header = {
        .ts_sec = pkt_hdr->ts.tv_sec,
        .ts_usec = pkt_hdr->ts.tv_usec,
        .incl_len = pkt_hdr->caplen,
        .orig_len = pkt_hdr->len
    };

    // Write the packet header
    memcpy(pcap_binary + offset, &pkt_header, packet_header_size);
    offset += packet_header_size;

    // Write the packet data
    memcpy(pcap_binary + offset, pkt_data, packet_data_size);

    return pcap_binary; // Return the PCAP binary
}

int process_next_layer(packet_t* packet, uint16_t protocol_id, const uint8_t* payload, size_t payload_len, const handler_t* handlers) {
    for (int i = 0; handlers[i].protocol_name != NULL; i++) {
        if (handlers[i].id == protocol_id) {
            if (packet->num_layers >= MAX_LAYERS - 1) {
                fprintf(stderr, "Maximum number of layers reached\n");
                return 1;
            }
            layer_t *next_layer = &packet->layers[packet->num_layers++];
            next_layer->protocol_name = handlers[i].protocol_name;
            return handlers[i].dissect(next_layer, packet, payload, payload_len);
        }
    }
    fprintf(stderr, "Unsupported protocol ID: 0x%04X\n", protocol_id);
    if (write_unsupported_pcap) {
        size_t output_size;
        uint8_t* pcap_binary = create_pcap_binary(&packet->pkthdr, packet->raw_data, &output_size);

        // Get current timestamp
        time_t now = time(NULL);
        struct tm *t = localtime(&now);
        char timestamp[20];
        strftime(timestamp, sizeof(timestamp), "%Y%m%d_%H%M%S", t);

        // Create filename with timestamp
        char filename[100];
        snprintf(filename, sizeof(filename), "unknown-protocol-0x%04X-%s.pcap", protocol_id, timestamp);

        // Open file for writing
        FILE *file = fopen(filename, "wb");
        if (file == NULL) {
            fprintf(stderr, "Error opening file for writing\n");
            free(pcap_binary);
            return 1;
        }

        // Write pcap binary to file
        size_t written = fwrite(pcap_binary, 1, output_size, file);
        if (written != output_size) {
            fprintf(stderr, "Error writing to file\n");
        }

        // Close file and free memory
        fclose(file);
        free(pcap_binary);

        fprintf(stderr, "Packet written to file: %s\n", filename);
    }
    return 1;
}

const unsigned char* hex_encode(const uint8_t* data, size_t len) {
    if (!data || len == 0) return NULL;

    char* hex_string = (char*)malloc(len * 3); // Each byte becomes two hex chars plus a colon
    if (!hex_string) return NULL;

    char* ptr = hex_string;
    for (size_t i = 0; i < len; i++) {
        ptr += sprintf(ptr, "%02x", data[i]);
        if (i < len - 1) {
            *ptr++ = ':';
        }
    }
    *ptr = '\0'; // Null-terminate the string
    return (const unsigned char*)hex_string;
}

#include <ctype.h>
#include <string.h>

void trimWhitespace(char* str) {
    if (str == NULL || *str == '\0') {
        return;
    }

    // Trim leading whitespace
    char* start = str;
    while (isspace((unsigned char)*start)) {
        start++;
    }

    // Trim trailing whitespace
    char* end = start + strlen(start) - 1;
    while (end > start && isspace((unsigned char)*end)) {
        *end = '\0';
        end--;
    }

    // Shift the trimmed string to the original buffer if needed
    if (start != str) {
        memmove(str, start, strlen(start) + 1);
    }
}

