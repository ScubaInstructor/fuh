#ifndef KAFKA_PROCESSOR_H
#define KAFKA_PROCESSOR_H

#include <stdbool.h>

#include "netdissect-alloc.h"
#include <librdkafka/rdkafka.h>

typedef struct{
    netdissect_options *ndo;
    volatile int running;
    bool enable_kafka;
    const char *device;
    char ip_address[INET_ADDRSTRLEN];
    bool packet_compression;
}  kafka_processor ;

kafka_processor *kafka_processor_create(netdissect_options *ndo, char *device);
void kafka_processor_destroy(kafka_processor *kp);

void kafka_processor_run(const kafka_processor *kp);
void kafka_processor_stop(kafka_processor *kp);

rd_kafka_t *connect_to_kafka(const char *kafka_host, const char *kafka_port, const char *kafka_topic, rd_kafka_topic_t **topic_handle);


#endif // KAFKA_PROCESSOR_H

