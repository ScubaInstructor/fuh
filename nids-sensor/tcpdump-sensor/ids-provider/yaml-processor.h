#ifndef YAML_PROCESSOR_H
#define YAML_PROCESSOR_H

#include "common-util.h"

struct kv_pair {
    char* key;
    char* value;
};

// Load a YAML file and return a pointer to an array of strings (lines).
char** loadYamlFile(const char* filePath, int* lineCount);

// Flatten the YAML structure into a key-value pair array.
struct kv_pair* flattenYamlNode(char **lines, int lineCount, int *pairCount);

// Free memory allocated for key-value pairs.
void freeKvPairs(struct kv_pair* pairs, int pairCount);

#endif // YAML_PROCESSOR_H
