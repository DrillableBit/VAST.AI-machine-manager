import json
import yaml
import sys
import os
from misc import version_in_range

def filter_vcpus(machine, config):
    try:
        if 'min_vCPU' in config and 'max_vCPU' in config:
            min_vcpus = config['min_vCPU']
            max_vcpus = config['max_vCPU']
            vcpus = float(machine.get('vCPUs', 0))
            return min_vcpus <= vcpus <= max_vcpus
        return True
    except Exception as e:
        print(f"Error while filtering vCPUs for machine {machine.get('ID', 'unknown')}: {e}")
        return False

def filter_nv_driver(machine, config):
    try:
        if 'min_nv_driver' in config and 'max_nv_driver' in config:
            min_nv_driver = config['min_nv_driver']
            max_nv_driver = config['max_nv_driver']
            return version_in_range(machine.get('NV_Driver', ''), min_nv_driver, max_nv_driver)
        return True
    except Exception as e:
        print(f"Error while filtering NV_Driver for machine {machine.get('ID', 'unknown')}: {e}")
        return False
    
def filter_cuda(machine, config):
    try:
        if 'min_cuda' in config and 'max_cuda' in config:
            min_cuda = config['min_cuda']
            max_cuda = config['max_cuda']
            return version_in_range(machine.get('CUDA', ''), min_cuda, max_cuda)
        return True
    except Exception as e:
        print(f"Error while filtering CUDA for machine {machine.get('ID', 'unknown')}: {e}")
        return False

def filter_machine(machine, config):
    if config is None:
        return True
    return (filter_vcpus(machine, config) and 
            filter_nv_driver(machine, config) and 
            filter_cuda(machine, config))


if __name__ == "__main__":
    config_file = sys.argv[1]
    results_file = sys.argv[2]
    filtered_results_file = sys.argv[3]

    # Ensure config file exists
    if not os.path.exists(config_file):
        print(f"Config file not found: {config_file}")
        sys.exit(1)

    # Ensure results file exists
    if not os.path.exists(results_file):
        print(f"Results file not found: {results_file}")
        sys.exit(1)

    with open(config_file, 'r') as file:
        config = yaml.safe_load(file)
        config = config.get('global_filters', {})  # Ensure global_filters key exists

    with open(results_file, 'r') as file:
        results = json.load(file)

    filtered_machines = [machine for machine in results if filter_machine(machine, config)]
      
    with open(filtered_results_file, 'w') as file:
        json.dump(filtered_machines, file, indent=4)