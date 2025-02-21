#ifndef PROCESSOR_THREADS_H
#define PROCESSOR_THREADS_H

#include "netdissect-alloc.h"
#include "dissection-processor.h"

typedef struct {
    dissection_processor *dp;
    char *device;
} dissection_thread_args;

// Initialize and start the processor threads
void start_processor_threads(netdissect_options *ndo, char *device);

// Wait for processor threads to finish and clean up
void wait_for_processor_threads(void);

// Stop and clean up the processor threads
void stop_processor_threads(void);

#endif // PROCESSOR_THREADS_H
