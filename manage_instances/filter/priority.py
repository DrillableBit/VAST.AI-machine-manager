import json
import sys
import os
import yaml

def main():
    config_file = sys.argv[1]
    filtered_results_file = sys.argv[2]
    sorted_results_file = sys.argv[3]

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
        priority_condition = config['global_filters'].get('priority_condition', 'vCPUs')

    with open(filtered_results_file, 'r') as file:
        filtered_results = json.load(file)

    sorted_results = sorted(filtered_results, key=lambda x: float(x.get(priority_condition, 0)), reverse=True)

    with open(sorted_results_file, 'w') as file:
        json.dump(sorted_results, file, indent=4)

if __name__ == "__main__":
    main()