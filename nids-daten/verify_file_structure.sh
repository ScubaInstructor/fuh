#!/bin/bash

if [ $# -lt 2 ]; then
    echo "Usage: $0 <reference_file> <directory1> [<directory2> ...]"
    exit 1
fi

reference_file="$1"
shift

reference_header=$(head -n 1 "$reference_file")

for dir in "$@"; do
    find "$dir" -type f -name "*.csv" | while read -r file; do
        file_header=$(head -n 1 "$file")
        if [ "$file_header" = "$reference_header" ]; then
            echo "Match: $file"
        else
            echo "Mismatch: $file"
        fi
    done
done
