#include "yaml-processor.h"
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <ctype.h>

#define INITIAL_CAPACITY 100
#define MAX_PAIRS 1000
#define MAX_LINE_LENGTH 512
#define MAX_DEPTH 20

char** loadYamlFile(const char* filePath, int* lineCount) {
    FILE* file = fopen(filePath, "r");
    if (!file) {
        fprintf(stderr, "Error: Unable to open file %s\n", filePath);
        *lineCount = 0;
        return NULL;
    }

    char** lines = NULL;
    int capacity = 10;
    *lineCount = 0;

    lines = (char**)malloc(capacity * sizeof(char*));
    if (!lines) {
        fclose(file);
        *lineCount = 0;
        return NULL;
    }

    char buffer[MAX_LINE_LENGTH];
    while (fgets(buffer, sizeof(buffer), file)) {
        if (*lineCount >= capacity) {
            capacity *= 2;
            char** newLines = (char**)realloc(lines, capacity * sizeof(char*));
            if (!newLines) {
                for (int i = 0; i < *lineCount; i++) {
                    free(lines[i]);
                }
                free(lines);
                fclose(file);
                *lineCount = 0;
                return NULL;
            }
            lines = newLines;
        }

        size_t len = strlen(buffer);
        if (len > 0 && buffer[len-1] == '\n') {
            buffer[len-1] = '\0';
        }

        lines[*lineCount] = strdup(buffer);
        if (!lines[*lineCount]) {
            for (int i = 0; i < *lineCount; i++) {
                free(lines[i]);
            }
            free(lines);
            fclose(file);
            *lineCount = 0;
            return NULL;
        }
        (*lineCount)++;
    }

    fclose(file);
    return lines;
}

// Function to determine indentation level
int getIndentLevel(const char* line) {
    int level = 0;
    while (*line == ' ' || *line == '\t') {
        level++;
        line++;
    }
    return level;
}

// Function to parse a YAML structure into key-value pairs
struct kv_pair* flattenYamlNode(char** lines, int lineCount, int* pairCount) {
    if (!lines || lineCount == 0) {
        *pairCount = 0;
        return NULL;
    }

    struct kv_pair* pairs = malloc(MAX_PAIRS * sizeof(struct kv_pair));
    if (!pairs) {
        fprintf(stderr, "Error: Memory allocation for key-value pairs failed.\n");
        *pairCount = 0;
        return NULL;
    }

    *pairCount = 0;
    char parentStack[MAX_DEPTH][MAX_LINE_LENGTH] = {""};
    int indentStack[MAX_DEPTH] = {0};
    int depth = 0;

    for (int i = 0; i < lineCount; i++) {
        char* line = lines[i];
        if (strlen(line) == 0 || line[0] == '#') continue; // Skip empty lines and comments

        int indentLevel = getIndentLevel(line);
        char* colonPos = strchr(line, ':');

        if (colonPos) {
            *colonPos = '\0';
            char* key = line + indentLevel;
            char* value = colonPos + 1;

            trimWhitespace(key);
            trimWhitespace(value);

            // Adjust depth based on indentation
            while (depth > 0 && indentLevel <= indentStack[depth - 1]) {
                depth--;  // Move up one level
            }

            // Store current key in stack
            strncpy(parentStack[depth], key, MAX_LINE_LENGTH - 1);
            parentStack[depth][MAX_LINE_LENGTH - 1] = '\0';

            // Build full path correctly
            char fullPath[MAX_LINE_LENGTH] = "";
            for (int j = 0; j <= depth; j++) {
                if (j > 0) strncat(fullPath, ".", MAX_LINE_LENGTH - strlen(fullPath) - 1);
                strncat(fullPath, parentStack[j], MAX_LINE_LENGTH - strlen(fullPath) - 1);
            }

            // Update stack
            indentStack[depth] = indentLevel;
            depth++;

            // If the key has an associated value, store it
            if (*value) {
                if (*pairCount < MAX_PAIRS) {
                    pairs[*pairCount].key = strdup(fullPath);
                    pairs[*pairCount].value = strdup(value);
                    if (!pairs[*pairCount].key || !pairs[*pairCount].value) {
                        fprintf(stderr, "Error: Memory allocation failed for key-value pair.\n");
                        free(pairs);
                        *pairCount = 0;
                        return NULL;
                    }
                    (*pairCount)++;
                } else {
                    fprintf(stderr, "Warning: Reached maximum key-value pair limit (%d).\n", MAX_PAIRS);
                    break;
                }
            }
        }
    }

    return pairs;
}

void freeKvPairs(struct kv_pair* pairs, int pairCount) {
    if (!pairs) return;

    for (int i = 0; i < pairCount; i++) {
        free((void*)pairs[i].key);
        free((void*)pairs[i].value);
    }
    free(pairs);
}
