#ifndef RINGBUFFER_H
#define RINGBUFFER_H

#include <stddef.h>
#include <stdint.h>
#include <sys/time.h>
#include <stdatomic.h>
#include <netdissect.h>

struct packet_entry {
    size_t length;           // length of the stored packet data
    struct timeval ts;       // timestamp
};

struct ring_buffer {
    uint8_t *buffer;            // large buffer holding all packets
    struct packet_entry *meta;  // per-slot metadata (length, ts)
    size_t count;               // number of slots
    size_t snaplen;             // max size per packet
    _Atomic size_t head;        // producer writes here
    _Atomic size_t tail;        // consumer reads here
    const char *buffer_id;
};

// Function prototypes
struct ring_buffer* ring_buffer_init(netdissect_options *ndo, size_t count, size_t snaplen, const char *buffer_id);
void ring_buffer_free(struct ring_buffer* rb);
int ring_buffer_enqueue(struct ring_buffer* rb, const uint8_t *sp, size_t length, const struct timeval *ts);
const uint8_t* ring_buffer_dequeue(struct ring_buffer* rb, size_t *out_length, struct timeval *out_ts);
int ring_buffer_push(netdissect_options *ndo, struct ring_buffer *rb, const void *data, size_t length, const struct timeval *ts);
size_t ring_buffer_available_space(struct ring_buffer *rb); // New function declaration
void initialize_ring_buffer_after_open(netdissect_options *ndo);

#endif // RINGBUFFER_H
