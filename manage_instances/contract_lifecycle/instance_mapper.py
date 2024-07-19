import yaml
import sys
import os
import json

def instance_mapper(config_file, filtered_results_file):
    # Ensure config file exists
    if not os.path.exists(config_file):
        print(f"Config file not found: {config_file}")
        sys.exit(1)

        # Ensure filtered results file exists
    if not os.path.exists(filtered_results_file):
        print(f"Filtered results file not found: {filtered_results_file}")
        sys.exit(1)



    with open(config_file, 'r') as file:
        config = yaml.safe_load(file)

    with open(filtered_results_file, 'r') as file:
        filtered_results = json.load(file)

    if not filtered_results:
        print("Error: No machines found in the filtered results.")
        sys.exit(1)

    # Check for contracts in the configuration
    if 'contracts' not in config or not config['contracts']:
        print("Error: No contracts found in the configuration.")
        sys.exit(1)

    contracts = config['contracts']
    sorted_contracts = sorted(contracts.items(), key=lambda x: x[1].get('priority', float('inf')))

    machine_assignments = {}
    for i, (machine, details) in enumerate(sorted_contracts):
        if i < len(filtered_results):
            machine_data = filtered_results[i]
            assignment = {k: v for k, v in details.items()}
            assignment['assigned_machine'] = machine_data
            machine_assignments[machine] = assignment
        else:
            print(f"Warning: Not enough machines in filtered results to assign to {machine}.")

    # Path to the assignments file
    script_dir = os.path.dirname(os.path.realpath(__file__))
    assignments_file = os.path.join(script_dir, 'assignments.json')

    # Check if assignments.json exists, if not create it
    if not os.path.exists(assignments_file):
        with open(assignments_file, 'w') as file:
            json.dump({}, file)

    # Write the assignments to a JSON file
    with open(assignments_file, 'w') as file:
        json.dump(machine_assignments, file, indent=4)

    for machine, assignment in machine_assignments.items():
        print(f"Machine: {machine}")
        print(f"  Priority: {assignment['priority']}")
        print(f"  Image: {assignment['image']}")
        print(f"  Disk: {assignment['disk']}")
        print(f"  Duration: {assignment['duration']}")
        print(f"  Assigned Machine ID: {assignment['assigned_machine']['ID']}")
        print("")

def main():
    if len(sys.argv) != 3:
        print("Usage: python3 instance_mapper.py <config_file> <filtered_results_file>")
        sys.exit(1)

    config_file = sys.argv[1]
    filtered_results_file = sys.argv[2]
    instance_mapper(config_file, filtered_results_file)

if __name__ == "__main__":
    main()