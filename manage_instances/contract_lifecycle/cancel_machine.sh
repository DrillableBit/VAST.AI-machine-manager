#!/bin/bash
# Path to the Python script
# Determine the script's directory and set the path to the Python script
script_dir=$(dirname "$0")
python_log_script="$script_dir/../run_machine/command_logger.py"

# Check if a contract ID is provided
if [ -z "$1" ]; then
    echo "Usage: $0 <contract_id>"
    exit 1
fi

contract_id=$1

# Cancel the contract
# Execute the Python script with the provided arguments
python3 "$python_log_script" "Vast.AI_Machine_Manager" "Attempting to destroy instance $contract_id." "$contract_id"
cancel_response=$(vastai destroy instance "$contract_id")
echo "$cancel_response"
python3 "$python_log_script" "Vast.AI_Machine_Manager" "VAST_AI responded: $cancel_response" "$contract_id"

# Remove the contract from active_contracts.json
if [ -f active_contracts.json ]; then
    jq --argjson contract "$contract_id" 'del(.active_contracts[] | select(. == $contract))' active_contracts.json > tmp.$$.json && mv tmp.$$.json active_contracts.json
fi