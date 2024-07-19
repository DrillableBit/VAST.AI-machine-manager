#!/bin/bash

# Check if a machine ID is provided
if [ -z "$1" ]; then
    echo "Usage: $0 <machine_id>"
    exit 1
fi

machine_id=$1

# Rent the machine
./rent_machine.sh "$machine_id"

# Get the most recent contract ID from active_contracts.json
if [ -f active_contracts.json ]; then
    contract_id=$(jq '.active_contracts | last' active_contracts.json)
    
    if [ -n "$contract_id" ]; then
        # Wait for 10 seconds
        sleep 10

        # Cancel the contract
        ./cancel_machine.sh "$contract_id"
    else
        echo "No contract found to cancel."
    fi
else
    echo "active_contracts.json not found."
fi