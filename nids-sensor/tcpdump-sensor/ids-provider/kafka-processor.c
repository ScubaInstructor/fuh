#include "kafka-processor.h"
#include "ring-buffer.h"
#include "common-util.h"

#include <sys/ioctl.h>
#include <net/if.h>
#include <unistd.h>

#include <stdlib.h>
#include <stdio.h>
#include <lz4.h>
#include <librdkafka/rdkafka.h>
#include <strings.h>
#include <net/if_var.h>
#include <sys/ioctl.h>
#include <sys/sockio.h>

#define MAX_JSON_SIZE 65536

kafka_processor *kafka_processor_create(netdissect_options *ndo, char *device) {
    kafka_processor *kp = malloc(sizeof(kafka_processor));

    if (kp) {
        struct kv_pair *pairs = ndo->ids_pairs;
        const size_t count = ndo->ids_pairs_count;

        kp->ndo = ndo;
        kp->running = 1;
        kp->enable_kafka = strcasecmp(get_option_value(pairs, count,
                                                       "kafka.enable_capture_traffic_to_kafka"), "TRUE") == 0;
        kp->device = device;
        kp->packet_compression = strcasecmp(get_option_value(pairs, count, "dissect.json.compression"), "TRUE") == 0;


        int fd;
        struct ifreq ifr;

        fd = socket(AF_INET, SOCK_DGRAM, 0);

        ifr.ifr_addr.sa_family = AF_INET;
        strncpy(ifr.ifr_name, device, IFNAMSIZ - 1);

        ioctl(fd, SIOCGIFADDR, &ifr);
        close(fd);

        strncpy(kp->ip_address, inet_ntoa(((struct sockaddr_in *)&ifr.ifr_addr)->sin_addr), INET_ADDRSTRLEN);
        kp->ip_address[INET_ADDRSTRLEN - 1] = '\0';
    }

    return kp;
}

void kafka_processor_destroy(kafka_processor *kp) {
    free(kp);
}

void kafka_processor_run(const kafka_processor *kp) {
    if (!kp) return;

    netdissect_options *ndo = kp->ndo;
    struct ring_buffer *rb_in = ndo->ids_rb_json;

    rd_kafka_t *producer = NULL;
    const char *kafka_topic;
    if (kp->enable_kafka) {
        struct kv_pair *pairs = ndo->ids_pairs;
        const size_t count = ndo->ids_pairs_count;

        const char *kafka_host = get_option_value(pairs, count, "kafka.packet_topic.host");
        const char *kafka_port = get_option_value(pairs, count, "kafka.packet_topic.port");
        kafka_topic = get_option_value(pairs, count, "kafka.packet_topic.topic");

        // Topic handle
        rd_kafka_topic_t *topic_handle = NULL;

        // Connect to Kafka
        producer = connect_to_kafka(kafka_host, kafka_port, kafka_topic, &topic_handle);
        if (producer == NULL) {
            fprintf(stderr, "Failed to connect to Kafka\n");
            return;
        }
    } else {
        fprintf(stderr, "Sending capture packets to Kafka is DISABLED.\n");
    }

    // Allocate a buffer to hold the uncompressed JSON
    char *uncompressed_buffer = (char *) malloc(MAX_JSON_SIZE);
    if (!uncompressed_buffer) {
        fprintf(stderr, "Failed to allocate uncompressed buffer\n");
        return;
    }

    char partition_key[256];
    snprintf(partition_key, sizeof(partition_key), "%s-%s", kp->ip_address, kp->device);

    static time_t last_poll_time = 0;

    while (kp->running) {
        size_t compressed_size;
        struct timeval ts;
        const uint8_t *data = ring_buffer_dequeue(rb_in, &compressed_size, &ts);

        if (!data) {
            usleep(1000);
            continue;
        }

        size_t message_size;
        const char *message_to_send;

        if (kp->packet_compression) {
            if (compressed_size == 0) {
                fprintf(stderr, "Received empty compressed data, skipping\n");
                continue;
            }

            int decompressed_size = LZ4_decompress_safe((const char *)data, uncompressed_buffer, compressed_size, MAX_JSON_SIZE);
            if (decompressed_size < 0) {
                fprintf(stderr, "LZ4 decompression failed\n");
                continue;
            }

            uncompressed_buffer[decompressed_size] = '\0';
            message_size = decompressed_size;
            message_to_send = uncompressed_buffer;
        } else {
            message_size = compressed_size;
            message_to_send = (const char *)data;
        }

        if (kp->enable_kafka) {
            rd_kafka_resp_err_t err = rd_kafka_producev(
                producer,
                RD_KAFKA_V_TOPIC(kafka_topic),
                RD_KAFKA_V_PARTITION(RD_KAFKA_PARTITION_UA),
                RD_KAFKA_V_MSGFLAGS(0),  // Removed RD_KAFKA_MSG_F_COPY to improve performance
                RD_KAFKA_V_KEY(partition_key, strlen(partition_key)),
                RD_KAFKA_V_VALUE((void *)message_to_send, message_size),
                RD_KAFKA_V_END
            );

            if (err != RD_KAFKA_RESP_ERR_NO_ERROR) {
                fprintf(stderr, "Failed to produce message: %s\n", rd_kafka_err2str(err));
            } else {
                ++ndo->ids_kafkaMessagesSent;
            }

            time_t current_time = time(NULL);
            if (current_time > last_poll_time + 0.1) {
                rd_kafka_poll(producer, 0);
                last_poll_time = current_time;
            }
        }
    }

    free(uncompressed_buffer);
}



void kafka_processor_stop(kafka_processor *kp) {
    kp->running = 0;
}

rd_kafka_t *connect_to_kafka(const char *kafka_host, const char *kafka_port, const char *kafka_topic,
                             rd_kafka_topic_t **topic_handle) {
    // Configuration
    char errstr[512];
    rd_kafka_conf_t *conf = rd_kafka_conf_new();
    // Set compression type (e.g., lz4)
    if (rd_kafka_conf_set(conf, "compression.type", "lz4", errstr, sizeof(errstr)) != RD_KAFKA_CONF_OK) {
        fprintf(stderr, "Error setting compression.type: %s\n", errstr);
        return NULL;
    }

    if (rd_kafka_conf_set(conf, "batch.size", "32768", errstr, sizeof(errstr)) != RD_KAFKA_CONF_OK) {
        fprintf(stderr, "Error setting batch.size: %s\n", errstr);
        return NULL;
    }

    // Set linger time (wait before sending batches)
    if (rd_kafka_conf_set(conf, "linger.ms", "10", errstr, sizeof(errstr)) != RD_KAFKA_CONF_OK) {
        fprintf(stderr, "Error setting linger.ms: %s\n", errstr);
        return NULL;
    }

    // Set buffer size (memory for buffered messages)
    if (rd_kafka_conf_set(conf, "queue.buffering.max.kbytes", "1048576", errstr, sizeof(errstr)) != RD_KAFKA_CONF_OK) {
        fprintf(stderr, "Error setting queue.buffering.max.kbytes: %s\n", errstr);
        return NULL;
    }

    // Set the maximum number of messages in the queue
    if (rd_kafka_conf_set(conf, "queue.buffering.max.messages", "100000", errstr, sizeof(errstr)) != RD_KAFKA_CONF_OK) {
        fprintf(stderr, "Error setting queue.buffering.max.messages: %s\n", errstr);
        return NULL;
    }

    // Set Kafka broker(s)
    if (rd_kafka_conf_set(conf, "bootstrap.servers", "broker1:9092,broker2:9092", errstr, sizeof(errstr)) !=
        RD_KAFKA_CONF_OK) {
        fprintf(stderr, "Error setting bootstrap.servers: %s\n", errstr);
        return NULL;
    }
    // Set broker list
    char brokers[256];
    snprintf(brokers, sizeof(brokers), "%s:%s", kafka_host, kafka_port);

    // Set the "bootstrap.servers" configuration
    if (rd_kafka_conf_set(conf, "bootstrap.servers", brokers, errstr, sizeof(errstr)) != RD_KAFKA_CONF_OK) {
        fprintf(stderr, "Configuration error: %s\n", errstr);
        rd_kafka_conf_destroy(conf);
        return NULL;
    }

    // Set optional configuration (e.g., client.id)
    if (rd_kafka_conf_set(conf, "client.id", "my_kafka_producer", errstr, sizeof(errstr)) != RD_KAFKA_CONF_OK) {
        fprintf(stderr, "Configuration error: %s\n", errstr);
        rd_kafka_conf_destroy(conf);
        return NULL;
    }

    // Create Kafka producer
    rd_kafka_t *producer = rd_kafka_new(RD_KAFKA_PRODUCER, conf, errstr, sizeof(errstr));
    if (!producer) {
        fprintf(stderr, "Failed to create Kafka producer: %s\n", errstr);
        rd_kafka_conf_destroy(conf); // Destroy configuration if producer creation fails
        return NULL;
    }

    // Check if brokers are reachable (poll for metadata)
    const struct rd_kafka_metadata *metadata = NULL;
    rd_kafka_resp_err_t metadata_err = rd_kafka_metadata(producer, 0, NULL, &metadata, 5000);

    if (metadata_err != RD_KAFKA_RESP_ERR_NO_ERROR) {
        fprintf(stderr, "Failed to fetch metadata: %s\n", rd_kafka_err2str(metadata_err));
        rd_kafka_destroy(producer);
        return NULL;
    }
    rd_kafka_metadata_destroy(metadata); // Free metadata when done

    // Create topic handle
    *topic_handle = rd_kafka_topic_new(producer, kafka_topic, NULL);
    if (!*topic_handle) {
        fprintf(stderr, "Failed to create topic handle for topic: %s\n", kafka_topic);
        rd_kafka_destroy(producer);
        return NULL;
    }

    printf("Connected to Kafka at %s:%s, topic: %s\n", kafka_host, kafka_port, kafka_topic);
    return producer;
}
