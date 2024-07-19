#!/bin/bash

# Determine the directory of the current script
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

# Use the script directory to reference fetch_machines/executable.sh
"$SCRIPT_DIR/fetch_machines/executable.sh"
FETCH_DIR=$SCRIPT_DIR/fetch_machines
FILTER_DIR=$SCRIPT_DIR/filter
CONTRACT_DIR=$SCRIPT_DIR/contract_lifecycle


# Filter machines
echo "..."
python3 $FILTER_DIR/filter_machine.py $SCRIPT_DIR/config.yaml $FETCH_DIR/results.json $FILTER_DIR/filtered_results.json
echo "Filter Complete."
echo "..."
python3 $FILTER_DIR/priority.py $SCRIPT_DIR/config.yaml $FILTER_DIR/filtered_results.json $FILTER_DIR/sorted_results.json
echo "Sort Complete."
echo " "
echo "Machines have been fetched, filtered, and sorted."
echo " "
echo "__________________________________________________"
python3  $CONTRACT_DIR/instance_mapper.py $SCRIPT_DIR/config.yaml $FILTER_DIR/sorted_results.json
echo "Tasks have been mapped."
echo " "
echo "__________________________________________________"
python3  $CONTRACT_DIR/lifecycle.py $CONTRACT_DIR/assignments.json
echo " "
echo "--------------------------------------------------"
echo " "
echo "               Session Completed"
echo " "
echo "--------------------------------------------------"
