#!/bin/bash

# Determine the directory of the current script
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

# Path to the JSON file
json_file="$SCRIPT_DIR/results.json"

# Initialize or clear the JSON file
echo "[]" > "$json_file"

# Run the search_my_machines.sh script
"$SCRIPT_DIR/fetch_available.sh"

# Check the JSON file for more than 0 entries
json_file="$SCRIPT_DIR/results.json"

# Read the JSON file and count the number of entries
entry_count=$(jq length "$json_file")

# Check the number of entries and print the appropriate message
if [ "$entry_count" -gt 0 ]; then
    echo "_______________________________________________________"
    echo " "
    if [ "$entry_count" -eq 1 ]; then
        echo "Config successful, $entry_count machine available."
    else
        echo "Config successful, $entry_count machines available."
    fi
else
    echo "No machines found"
fi
echo " "