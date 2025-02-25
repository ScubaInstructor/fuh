
#include "ring-buffer.h"
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <stdatomic.h>
#include "common-util.h"
#include <netdissect-alloc.h>

struct ring_buffer *ring_buffer_init(netdissect_options *ndo, size_t count, size_t snaplen, const char *buffer_id) {
    struct ring_buffer *rb = nd_malloc(ndo, sizeof(*rb));
    if (!rb) return NULL;

    rb->count = count;
    rb->snaplen = snaplen;
    rb->head = 0;
    rb->tail = 0;

    rb->buffer = nd_malloc(ndo, count * snaplen);
    if (!rb->buffer) {
        free(rb);
        return NULL;
    }

    rb->meta = nd_malloc(ndo, count * sizeof(struct packet_entry));
    if (!rb->meta) {
        free(rb->buffer);
        free(rb);
        return NULL;
    }

    rb->buffer_id = buffer_id;

    // Zero-initialize buffer and metadata
    memset(rb->buffer, 0, count * snaplen);
    memset(rb->meta, 0, count * sizeof(struct packet_entry));

    return rb;
}

void ring_buffer_free(struct ring_buffer *rb) {
    if (!rb) return;
    free(rb->buffer);
    free(rb->meta);
    free(rb);
}

int ring_buffer_enqueue(struct ring_buffer *rb, const uint8_t *sp, size_t length, const struct timeval *ts) {
    size_t head = atomic_load(&rb->head);
    size_t tail = atomic_load(&rb->tail);

    size_t next_head = (head + 1) % rb->count;
    if (next_head == tail) {
        // Buffer is full
        return -1;
    }

    if (length > rb->snaplen) {
        // Truncated packet
        length = rb->snaplen;
    }

    uint8_t *slot_ptr = rb->buffer + (head * rb->snaplen);
    memcpy(slot_ptr, sp, length);

    rb->meta[head].length = length;
    rb->meta[head].ts = *ts;

    atomic_store(&rb->head, next_head); // Advance head atomically
    return 0;
}

const uint8_t *ring_buffer_dequeue(struct ring_buffer *rb, size_t *out_length, struct timeval *out_ts) {
    size_t tail = atomic_load(&rb->tail);
    size_t head = atomic_load(&rb->head);

    if (tail == head) {
        // Buffer is empty
        return NULL;
    }

    const uint8_t *data = rb->buffer + (tail * rb->snaplen);
    *out_length = rb->meta[tail].length;
    *out_ts = rb->meta[tail].ts;

    atomic_store(&rb->tail, (tail + 1) % rb->count); // Advance tail atomically
    return data;
}

int ring_buffer_push(netdissect_options *ndo, struct ring_buffer *rb, const void *data, size_t length, const struct timeval *ts) {
    size_t head = atomic_load(&rb->head);
    size_t tail = atomic_load(&rb->tail);
    size_t next_head = (head + 1) % rb->count;

    // Check if the buffer is full
    if (next_head == tail) {
        fprintf(stderr, "Push failed: Buffer is full. head=%zu, tail=%zu\n", head, tail);
        return 0; // Buffer is full
    }

    // Validate data length
    if (length > rb->snaplen) {
        fprintf(stderr, "Warning: Data length (%zu) exceeds slot size (%zu). Truncating.\n", length, rb->snaplen);
        length = rb->snaplen; // Truncate to slot size
    }

    uint8_t *slot_ptr = rb->buffer + (head * rb->snaplen);
    memcpy(slot_ptr, data, length); // Copy data into buffer

    // Set metadata
    rb->meta[head].length = length;
    rb->meta[head].ts = *ts;

    // Advance the head pointer atomically
    atomic_store(&rb->head, next_head);

    // Debug logging
    //fprintf(stderr, "Push successful: head=%zu -> %zu, tail=%zu, length=%zu\n", head, next_head, tail, length);

    return 1; // Successfully pushed
}

size_t ring_buffer_available_space(struct ring_buffer *rb) {
    size_t head = atomic_load(&rb->head);
    size_t tail = atomic_load(&rb->tail);

    if (head >= tail) {
        return rb->count - (head - tail) - 1;
    } else {
        return tail - head - 1;
    }
}

void initialize_ring_buffer_after_open(netdissect_options *ndo) {
    struct kv_pair *pairs = ndo->ids_pairs;
    const size_t count = ndo->ids_pairs_count;

    const char *yaml_buffer_count = get_option_value(pairs, count, "capture.tcpdump.buffer_count");

    int buffer_count = 0;
    size_t snaplen = ndo->ndo_snaplen;

    if (yaml_buffer_count != NULL) {
        buffer_count = atoi(yaml_buffer_count);
    }

    if (buffer_count > 0) {
        struct ring_buffer *rb = ring_buffer_init(ndo, buffer_count, snaplen, "packet-buffer");

        if (!rb) {
            fprintf(stderr, "Failed to initialize ring buffer\n");
            exit(EXIT_FAILURE);
        } else {
            ndo->ids_rb = rb;

            size_t total_buffer_size = (size_t) buffer_count * snaplen;
            double total_buffer_size_mb = (double) total_buffer_size / (1024.0 * 1024.0);

            fprintf(stderr, "%s initialized with %d buffers, each %zu bytes. Total size: %.2f MB\n",
                    rb->buffer_id, buffer_count, snaplen, total_buffer_size_mb);
        }

        const char *compression = get_option_value(pairs, count, "dissect.json.compression");
        const char *uncompressed_ratio = get_option_value(pairs, count, "dissect.json.buffer_uncompressed_ratio");
        const char *compressed_ratio = get_option_value(pairs, count, "dissect.json.buffer_compressed_ratio");
        const char *json_buffer_count = get_option_value(pairs, count, "dissect.json.buffer_count");

        int use_compression = 0;
        double use_uncompressed_ratio = 4;
        double use_compressed_ratio = 2;
        int use_json_buffer_count = 0;
        double compression_ratio = 1;

        if (compression != NULL) {
            if (strcasecmp(compression, "true") == 0) {
                use_compression = 1;
            }
        }

        if (json_buffer_count != NULL) {
            use_json_buffer_count = atoi(json_buffer_count);
        }

        if (uncompressed_ratio != NULL) {
            use_uncompressed_ratio = atof(uncompressed_ratio);
        }

        if (compressed_ratio != NULL) {
            use_compressed_ratio = atof(compressed_ratio);
        }

        compression_ratio = use_compression ? use_compressed_ratio : use_uncompressed_ratio;

        int snaplen_json = (int) (snaplen * compression_ratio + 0.5);

        struct ring_buffer *rb_json = NULL;
        if (use_json_buffer_count > 0) {
            rb_json = ring_buffer_init(ndo, use_json_buffer_count, snaplen_json, "json-buffer");

            if (!rb_json) {
                fprintf(stderr, "Failed to initialize JSON ring buffer\n");
                exit(EXIT_FAILURE);
            }

            ndo->ids_rb_json = rb_json;
            size_t total_buffer_size = (size_t) use_json_buffer_count * snaplen_json;
            double total_buffer_size_mb = (double) total_buffer_size / (1024.0 * 1024.0);

            fprintf(
                stderr,
                "JSON ring buffer compressed = %s initialized with %d json buffers: storage ratio (raw -> json): %.2f Total size: %.2f MB\n",
                use_compression ? "true" : "false", use_json_buffer_count,
                compression_ratio, total_buffer_size_mb
                );

            //size_t available_space = ring_buffer_available_space(ndo->ids_rb_json);
            //fprintf(stderr, "json ring buffer available space: %zu packets\n", available_space);

        }
    } else {
        fprintf(stderr, "Key 'capture.tcpdump.buffer_count' not found in config.\n");
    }
}
