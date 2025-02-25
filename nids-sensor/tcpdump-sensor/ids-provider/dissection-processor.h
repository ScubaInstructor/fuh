#ifndef DISSECTION_PROCESSOR_H
#define DISSECTION_PROCESSOR_H

#include "netdissect-alloc.h"
#include <pcap.h>
#include <stdbool.h>

typedef struct {
    struct pcap_file_header *global_header; // Pointer to global header
    struct pcap_pkthdr packet_header; // Packet header
    uint8_t *data;
} reusable_pcap;


typedef struct {
    netdissect_options *ndo;
    volatile int running;
    const char *device;
    char ip_address[INET_ADDRSTRLEN];
    bool drop_ipv4_packets;
    bool drop_ipv6_packets;
    bool drop_no_ip_packets;
    bool drop_no_cicfm_packets;
    size_t non_ip_packets_dropped;

    bool attach_pcap_file;
    bool packet_compression;

    int dlt;
    const char *dlt_name;
} dissection_processor;

dissection_processor *dissection_processor_create(netdissect_options *ndo, char *device);

void dissection_processor_destroy(dissection_processor *dp);

void dissection_processor_run(const dissection_processor *dp, char *device);

void dissection_processor_stop(dissection_processor *dp);

int initialize_reusable_pcap(reusable_pcap *pcap, const struct pcap_file_header *hdr);

void free_reusable_pcap(reusable_pcap *pcap);

//static int rotate_json_file(const char *base_filename,
//                            FILE **json_file,
//                            size_t *current_packet_count,
//                            time_t *last_rotation_time);

static int rotate_json_file(const char *base_filename,
                            FILE **file_ptr,
                            size_t *packet_count_ptr,
                            time_t *last_rotation_ptr,
                            int file_index);

static int rotate_pcap_file(const char *base_filename,
                            const char *device,
                            pcap_t *pcap_dead,
                            pcap_dumper_t **pcap_dumper,
                            size_t *current_packet_count_pcap,
                            time_t *last_rotation_time_pcap);

void add_pcap_to_json(char* json_result, const struct pcap_pkthdr* pkt_hdr, const uint8_t* pkt_data, int attach_pcap);

/*static int rotate_pcap_file(const char *base_filename,
                            const char *device,
                            pcap_t *pcap_dead,
                            pcap_dumper_t **pcap_dumper,
                            size_t *current_packet_count,
                            time_t *last_rotation_time);*/
#endif // DISSECTION_PROCESSOR_H
