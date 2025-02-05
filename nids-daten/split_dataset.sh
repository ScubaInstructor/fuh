#!/bin/bash

# Check if input and output directories are provided
if [ "$#" -ne 2 ]; then
    echo "Usage: $0 <input_directory> <output_directory>"
    exit 1
fi

input_dir="$1"
output_dir="$2"

# Create output directory if it doesn't exist
mkdir -p "$output_dir"

# Process each CSV file in the input directory
for input_file in "$input_dir"/*.csv; do
    base_filename=$(basename "$input_file" .csv)
    
    header=$(head -n 1 "$input_file")

    awk -F',' -v base_name="$base_filename" -v out_dir="$output_dir" -v header="$header" '
    NR > 1 {
        category = $(NF-1)
        file = out_dir "/" base_name "_" category ".csv"
        if (!seen[file]++) {
            print header > file
        }
        print >> file
    }
    ' "$input_file"

    # Add row count to filenames for this input file
    for file in "$output_dir"/${base_filename}_*.csv; do
        count=$(wc -l < "$file")
        mv "$file" "${file%.csv}_$((count-1)).csv"
    done
done

echo "Split CSV files have been created in $output_dir"
