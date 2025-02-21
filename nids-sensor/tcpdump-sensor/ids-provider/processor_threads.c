#include "processor_threads.h"
#include "dissection-processor.h"
#include "kafka-processor.h"
#include <pthread.h>
#include <signal.h>
#include <stdlib.h>
#include <stdio.h>

static pthread_t dissection_thread, kafka_thread;
static volatile sig_atomic_t threads_running = 1;
static dissection_processor *dp;
static kafka_processor *kp;

static void *dissection_processor_thread_wrapper(void *arg) {
    dissection_thread_args *args = arg;
    dissection_processor_run(args->dp, args->device);

    return NULL;
}

static void *kafka_processor_thread_wrapper(void *arg) {
    kafka_processor_run(kp);
    return NULL;
}

void start_processor_threads(netdissect_options *ndo, char *device) {
    dp = dissection_processor_create(ndo, device);
    kp = kafka_processor_create(ndo, device);

    // Dynamically allocate args
    dissection_thread_args *args = malloc(sizeof(dissection_thread_args));
    if (!args) {
        fprintf(stderr, "Failed to allocate memory for dissection_thread_args\n");
        exit(1);
    }

    args->dp = dp;
    args->device = device;

    if (pthread_create(&dissection_thread, NULL, dissection_processor_thread_wrapper, args) != 0) {
        fprintf(stderr, "Failed to create dissection thread\n");
        free(args); // Free memory if thread creation fails
        exit(1);
    }

    if (pthread_create(&kafka_thread, NULL, kafka_processor_thread_wrapper, NULL) != 0) {
        fprintf(stderr, "Failed to create Kafka thread\n");
        exit(1);
    }
}


void stop_processor_threads(void) {
    threads_running = 0;
    dissection_processor_stop(dp);
    kafka_processor_stop(kp);
}

void wait_for_processor_threads(void) {
    pthread_join(dissection_thread, NULL);
    pthread_join(kafka_thread, NULL);
    dissection_processor_destroy(dp);
    kafka_processor_destroy(kp);
}
