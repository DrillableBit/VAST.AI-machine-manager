#!/bin/bash

# Check if a contract ID is provided
if [ -z "$1" ]; then
    echo "Usage: $0 <contract_id>"
    exit 1
fi

contract_id=$1

# Cancel the contract
cancel_response=$(vastai destroy instance "$contract_id")
echo "$cancel_response"

# Remove the contract from active_contracts.json
if [ -f active_contracts.json ]; then
    jq --argjson contract "$contract_id" 'del(.active_contracts[] | select(. == $contract))' active_contracts.json > tmp.$$.json && mv tmp.$$.json active_contracts.json
fi