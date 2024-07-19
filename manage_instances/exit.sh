#!/bin/bash

# Determine the directory of the current script
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
CONTRACT_LIFECYCLE_DIR="$SCRIPT_DIR/contract_lifecycle"
ACTIVE_CONTRACTS_FILE="$CONTRACT_LIFECYCLE_DIR/active_contracts.json"

# Ensure active_contracts.json exists
if [ ! -f "$ACTIVE_CONTRACTS_FILE" ]; then
    echo "Active contracts file not found: $ACTIVE_CONTRACTS_FILE"
    exit 1
fi

# Function to remove a contract ID from active_contracts.json
remove_contract_id() {
    CONTRACT_ID=$1
    jq "del(.active_contracts[] | select(. == $CONTRACT_ID))" "$ACTIVE_CONTRACTS_FILE" > "$ACTIVE_CONTRACTS_FILE.tmp" && mv "$ACTIVE_CONTRACTS_FILE.tmp" "$ACTIVE_CONTRACTS_FILE"
}

# Read the active contracts from the JSON file
ACTIVE_CONTRACTS=$(jq -r '.active_contracts[]' "$ACTIVE_CONTRACTS_FILE")

# Cancel each active contract
for CONTRACT_ID in $ACTIVE_CONTRACTS; do
    echo "Cancelling contract ID: $CONTRACT_ID"
    "$CONTRACT_LIFECYCLE_DIR/cancel_machine.sh" "$CONTRACT_ID"
    if [ $? -eq 0 ]; then
        echo "Successfully cancelled contract ID: $CONTRACT_ID"
        remove_contract_id "$CONTRACT_ID"
    else
        echo "Failed to cancel contract ID: $CONTRACT_ID"
    fi
done

echo "All active contracts have been processed."