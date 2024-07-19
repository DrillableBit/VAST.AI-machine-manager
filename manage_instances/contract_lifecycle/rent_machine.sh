#!/bin/bash

# Check if machine ID, image, and disk are provided
if [ -z "$1" ] || [ -z "$2" ] || [ -z "$3" ]; then
    echo "Usage: $0 <machine_id> <image> <disk>"
    exit 1
fi
machine_id=$1
image=$2
disk=$3

# Rent the machine
rent_response=$(vastai create instance "$machine_id" --image "$image" --disk "$disk")
echo "$rent_response" >&2  # Print the entire response to stderr

# Extract the new contract ID from the response using grep and sed
new_contract=$(echo "$rent_response" | grep -oP "(?<=new_contract': )\d+")

if [ -n "$new_contract" ]; then
    echo "$new_contract"  # Print only the new contract ID to stdout
else
    echo "Failed to create instance." >&2
    exit 1
fi