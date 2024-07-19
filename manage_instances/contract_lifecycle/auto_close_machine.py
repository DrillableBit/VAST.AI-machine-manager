import time
import subprocess
import json

def autoclose_machine(contract_id, duration, script_dir, active_contracts_file):
    # Wait for the specified duration
    time.sleep(duration)
    
    # Construct the command to run the cancel_machine.sh script
    cancel_command = f"{script_dir}/cancel_machine.sh {contract_id}"
    
    # Execute the cancel command
    cancel_process = subprocess.Popen(cancel_command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    cancel_output, cancel_error = cancel_process.communicate()

    if cancel_process.returncode == 0:
        print(f"Contract {contract_id} canceled successfully.")

        # Remove the contract from active_contracts.json
        with open(active_contracts_file, 'r+') as file:
            active_contracts = json.load(file)
            active_contracts["active_contracts"].remove(int(contract_id))
            file.seek(0)
            json.dump(active_contracts, file, indent=4)
            file.truncate()
    else:
        print(f"Failed to cancel contract {contract_id}. Error: {cancel_error.decode('utf-8')}")