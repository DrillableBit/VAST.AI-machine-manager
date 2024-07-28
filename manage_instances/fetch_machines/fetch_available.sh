#!/bin/bash

# List of headers to filter
headers=("ID" "CUDA" "N" "Model" "PCIE" "cpu_ghz" "vCPUs" "RAM" "Disk" "\$/hr" "DLP" "DLP/\$" "score" "NV_Driver" "Net_up" "Net_down" "R" "Max_Days" "mach_id" "status" "ports" "country")

# Function to search for machine ID in vastai search offers result
search_machine_id_in_vastai() {
    local machine_id=$1

    # Fetch the result from vastai
    result=$(vastai search offers "machine_id = $machine_id verified = any")

    # Check if the result contains the machine_id
    if echo "$result" | grep -q "$machine_id"; then

        # Extract header and data lines
        header=$(echo "$result" | head -n 1)
        data=$(echo "$result" | tail -n +2)

        # Split header and data into arrays
        IFS=' ' read -r -a header_array <<< "$header"
        IFS=' ' read -r -a data_array <<< "$data"

        # Handle multi-word headers
        header_map=()
        index=0
        while [[ $index -lt ${#header_array[@]} ]]; do
            if [[ ${header_array[$index]} =~ NV ]]; then
                header_map+=("${header_array[$index]}_${header_array[$((index + 1))]}")
                index=$((index + 2))
            else
                header_map+=("${header_array[$index]}")
                index=$((index + 1))
            fi
        done

        # Format the data as JSON
        json_data="{"
        for key in "${headers[@]}"; do
            value=""
            for i in "${!header_map[@]}"; do
                if [[ "${header_map[$i]}" == "$key" || "${header_map[$i]}" == "${key// /_}" ]]; then
                    value="${data_array[$i]}"
                    key=$(echo "$key" | sed 's/ /_/g')
                    json_data+="\"$key\": \"$value\""
                    json_data+=", "
                    break
                fi
            done
        done

        # Remove trailing comma and space, then close JSON object
        json_data="${json_data%, }"
        json_data+="}"

        echo "$json_data"
    else
        echo ""
    fi
}

# Determine the directory of the current script
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

# Path to the file containing machine IDs in the root directory
machine_file="$SCRIPT_DIR/../my_machines.txt"
# Path to the JSON file to save results
json_file="$SCRIPT_DIR/results.json"

# Initialize the JSON file
echo "[" > "$json_file"

# Read each machine_id from the file and call the function
first_entry=true
while IFS= read -r machine_id; do
    echo "Processing machine_id: $machine_id"  # Debug statement
    json_data=$(search_machine_id_in_vastai "$machine_id")
    if [ "$json_data" != "" ]; then
        if [ "$first_entry" = true ]; then
            first_entry=false
        else
            echo "," >> "$json_file"
        fi
        echo "$json_data" >> "$json_file"
    fi
done < "$machine_file"

# Finalize the JSON array
echo "]" >> "$json_file"

# Format JSON file using jq
jq '.' "$json_file" > tmp.$$.json && mv tmp.$$.json "$json_file"

# Print final json_file content for debugging
cat "$json_file"