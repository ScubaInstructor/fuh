#!/bin/bash

# Function to display usage help
usage() {
    echo "Usage: $0 -input=dir1,dir2 -output=dest_dir -exclude='string1 string2'"
    echo "\nParameters:"
    echo "  -input=     Comma-separated list of input directories"
    echo "  -output=    Destination directory for combined CSV files"
    echo "  -exclude=   Space-separated list of substrings to exclude from processing"
    exit 1
}

# Parse input arguments
INPUT_DIRS=""
DEST_DIR=""
EXCLUDED_STRINGS=()

while [[ "$#" -gt 0 ]]; do
    case "$1" in
        -input=*)
            IFS=',' read -r -a INPUT_DIRS <<< "${1#-input=}"
            shift
            ;;
        -output=*)
            DEST_DIR="${1#-output=}"
            shift
            ;;
        -exclude=*)
            IFS=' ' read -r -a EXCLUDED_STRINGS <<< "${1#-exclude=}"
            shift
            ;;
        *)
            echo "Unknown option: $1"
            usage
            ;;
    esac
done

# Ensure required parameters are set
if [[ -z "$DEST_DIR" || ${#INPUT_DIRS[@]} -eq 0 ]]; then
    echo "Missing required parameters."
    usage
fi

# Create destination directory if it doesn't exist
mkdir -p "$DEST_DIR"

# Process each CSV file in the source directories
for SOURCE_DIR in "${INPUT_DIRS[@]}"; do
    if [[ ! -d "$SOURCE_DIR" ]]; then
        echo "Warning: Source directory '$SOURCE_DIR' does not exist. Skipping."
        continue
    fi

    find "$SOURCE_DIR" -type f -name "*.csv" | while read -r file; do
        filename=$(basename "$file")

        # Check if filename contains any excluded strings
        for exclude in "${EXCLUDED_STRINGS[@]}"; do
            if [[ "$filename" == *"$exclude"* ]]; then
                echo "Skipping file: $filename"
                continue 2  # Skip to next file
            fi
        done

        # Extract category name by removing everything before the first underscore and filetype suffix
        attack_type=$(echo "$filename" | sed -E 's/^[^_]+_//; s/_[0-9]+\.csv$//')

        # Get output filename
        output_file="$DEST_DIR/${attack_type}.csv"

        # If output file doesn't exist, create it with header
        if [ ! -f "$output_file" ]; then
            head -n 1 "$file" > "$output_file"
        fi

        # Append data (excluding header) to output file
        tail -n +2 "$file" >> "$output_file"
    done
done

# Add row count to filenames in the destination directory
shopt -s nullglob  # Prevent errors if no files match
for file in "$DEST_DIR"/*.csv; do
    if [ -f "$file" ]; then
        rows=$(wc -l < "$file")
        rows=$((rows - 1))  # Subtract 1 to exclude header
        mv "$file" "${file%.csv}_${rows}.csv"
    fi
done
shopt -u nullglob  # Restore default globbing behavior

echo "Combined CSV files have been created in $DEST_DIR."
