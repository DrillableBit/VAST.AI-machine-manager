import time
import subprocess
import sys
import os
import json

# Add the current directory to the system path
sys.path.append(os.path.dirname(os.path.realpath(__file__)))

from run_machine.commands.start_command_manager import run_start_command
from run_machine.commands.end_command_manager import run_end_command
from run_machine.tasks.task_manager import run_task


def manage_machine(contract_id, details):
    try:
        contract_id = int(contract_id)
        start_command = details.get('start_command')
        task = details.get('task')
        end_command = details.get('end_command')
        
        if start_command:
            print(f"Running start command for contract ID {contract_id}")
            run_start_command(start_command, contract_id)
        
        if task:
            print(f"Running task for contract ID {contract_id}")
            run_task(task, contract_id, details)
        
        if end_command:
            print(f"Running end command for contract ID {contract_id}")
            run_end_command(end_command, contract_id)

        # Path to the active contracts file
        script_dir = os.path.dirname(os.path.realpath(__file__))
        active_contracts_file = os.path.join(script_dir, '..', 'contract_lifecycle', 'active_contracts.json')

        # Check if the active contracts file exists
        if not os.path.exists(active_contracts_file):
            print(f"Active contracts file not found: {active_contracts_file}")
            sys.exit(1)

        with open(active_contracts_file, 'r') as file:
            active_contracts = json.load(file)

        while True:
            if 'duration' in details:
                with open(active_contracts_file, 'r') as file:
                    active_contracts = json.load(file)
                
                if contract_id not in active_contracts.get("active_contracts", []):
                    print(f"Contract ID {contract_id} is no longer active. Machine manager shutting down...")
                    break

            print(f"Machine with contract ID: {contract_id} finished all its tasks and is currently idle.")
            time.sleep(1)  # Adjust the sleep duration as needed
    except Exception as e:
        print(f"An error occurred while managing the machine with contract ID {contract_id}: {e}")

if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage: python3 machine_manager.py <contract_id> <details>")
        sys.exit(1)
    
    contract_id = sys.argv[1]
    details = json.loads(sys.argv[2])
    
    manage_machine(contract_id, details)
