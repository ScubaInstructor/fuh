#ifndef LAYER_H
#define LAYER_H

#include <stdint.h>
#include <stdlib.h>

struct packet_t;

typedef struct layer {
    const char* protocol_name;
    void* parsed_data;
    int (*dissect)(struct layer*, struct packet_t*, const uint8_t*, size_t);
    char* (*to_json)(struct layer*);
} layer_t;

typedef struct {
    int id;
    const char* protocol_name;
    int (*dissect)(layer_t* layer, struct packet_t* packet, const uint8_t* data, size_t len);
    int group;
} handler_t;

extern handler_t handlers[];
extern handler_t udp_port_handlers[];

void layer_free(layer_t* layer);
#endif // LAYER_H
