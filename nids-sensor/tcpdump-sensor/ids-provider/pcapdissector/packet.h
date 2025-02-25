#ifndef PACKET_H
#define PACKET_H

#include <stdint.h>
#include <stdlib.h>
#include <pcap.h>
#include "layer.h"

// Forward declaration
struct layer;

#define MAX_LAYERS 10
#define MAX_PACKET_SIZE 65536

typedef struct packet_t {
    uint8_t raw_data[MAX_PACKET_SIZE];
    size_t len;
    struct pcap_pkthdr pkthdr;
    layer_t layers[MAX_LAYERS];
    int num_layers;
} packet_t;


/* Function prototypes */
packet_t* packet_create(const uint8_t* data, const struct pcap_pkthdr *pkt_hdr, int linktype);
void packet_destroy(packet_t* pkt);
int determine_first_layer(int linktype, packet_t* pkt, const uint8_t* data, size_t len);
char* packet_to_json(packet_t* packet);
char* build_protocol_chain(packet_t* pkt, int dlt);

#endif /* PACKET_H */
