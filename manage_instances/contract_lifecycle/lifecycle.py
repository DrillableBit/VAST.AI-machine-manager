import json
import os
import subprocess
import sys
from concurrent.futures import ThreadPoolExecutor, as_completed
# Add the parent directory to the system path
sys.path.append(os.path.dirname(os.path.dirname(os.path.realpath(__file__))))

from run_machine.machine_manager import manage_machine  # Use absolute import

from auto_close_machine import autoclose_machine


def rent_machine(details, script_dir, active_contracts_file):
    assigned_machine_id = details['assigned_machine']['ID']
    image = details['image']
    disk = details['disk']
    duration = details['duration']

    print(f"Renting machine {assigned_machine_id} with image {image} and disk {disk} for {duration} seconds.")
    
    # Construct the command to run the rent_machine.sh script
    rent_command = f"{script_dir}/rent_machine.sh {assigned_machine_id} {image} {disk}"
    
    # Execute the rent command
    rent_process = subprocess.Popen(rent_command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    rent_output, rent_error = rent_process.communicate()

    if rent_process.returncode == 0:
        new_contract = rent_output.decode('utf-8').strip()
        if new_contract.isdigit():
            print(f"New contract ID: {new_contract}")

            # Update active_contracts.json
            with open(active_contracts_file, 'r+') as file:
                active_contracts = json.load(file)
                active_contracts["active_contracts"].append(int(new_contract))
                file.seek(0)
                json.dump(active_contracts, file, indent=4)
                file.truncate()

            return new_contract
        else:
            print(f"Failed to extract new contract ID from the response: {rent_output.decode('utf-8')}")
    else:
        print(f"Failed to rent machine {assigned_machine_id}. Error: {rent_error.decode('utf-8')}")
    
    return None

def lifecycle(assignments_file):
    # Ensure assignments file exists
    if not os.path.exists(assignments_file):
        print(f"Assignments file not found: {assignments_file}")
        sys.exit(1)

    with open(assignments_file, 'r') as file:
        assignments = json.load(file)
    script_dir = os.path.dirname(os.path.realpath(__file__))
    
    # Ensure active_contracts.json exists
    active_contracts_file = os.path.join(script_dir, 'active_contracts.json')
    if not os.path.exists(active_contracts_file):
        with open(active_contracts_file, 'w') as file:
            json.dump({"active_contracts": []}, file)

    with ThreadPoolExecutor() as executor:
        futures = []
        for machine, details in assignments.items():
            contract_id = rent_machine(details, script_dir, active_contracts_file)
            if contract_id:
                details['contract_id'] = contract_id
                futures.append(executor.submit(autoclose_machine, contract_id, details['duration'], script_dir, active_contracts_file))
                futures.append(executor.submit(manage_machine, contract_id, details))
        # Write updated assignments with Contract IDs back to the file
        with open(assignments_file, 'w') as file:
            json.dump(assignments, file, indent=4)
            
        for future in as_completed(futures):
            try:
                future.result()
            except Exception as e:
                print(f"Exception occurred: {e}")

def main():
    if len(sys.argv) != 2:
        print("Usage: python3 lifecycle.py <assignments_file>")
        sys.exit(1)

    assignments_file = sys.argv[1]
    lifecycle(assignments_file)

if __name__ == "__main__":
    main()

# import json
# import os
# import time
# import subprocess
# import sys
# from concurrent.futures import ThreadPoolExecutor, as_completed

# def rent_and_cancel_machine(machine, details, script_dir, active_contracts_file):
#     assigned_machine_id = details['assigned_machine']['ID']
#     image = details['image']
#     disk = details['disk']
#     duration = details['duration']

#     print(f"Renting machine {assigned_machine_id} with image {image} and disk {disk} for {duration} seconds.")
    
#     # Construct the command to run the rent_machine.sh script
#     rent_command = f"{script_dir}/rent_machine.sh {assigned_machine_id} {image} {disk}"
    
#     # Execute the rent command
#     rent_process = subprocess.Popen(rent_command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
#     rent_output, rent_error = rent_process.communicate()

#     if rent_process.returncode == 0:
#         new_contract = rent_output.decode('utf-8').strip()
#         if new_contract.isdigit():
#             print(f"New contract ID: {new_contract}")

#             # Update active_contracts.json
#             with open(active_contracts_file, 'r+') as file:
#                 active_contracts = json.load(file)
#                 active_contracts["active_contracts"].append(int(new_contract))
#                 file.seek(0)
#                 json.dump(active_contracts, file, indent=4)
#                 file.truncate()

#             # Wait for the specified duration
#             time.sleep(duration)
            
#             # Construct the command to run the cancel_machine.sh script
#             cancel_command = f"{script_dir}/cancel_machine.sh {new_contract}"
            
#             # Execute the cancel command
#             cancel_process = subprocess.Popen(cancel_command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
#             cancel_output, cancel_error = cancel_process.communicate()

#             if cancel_process.returncode == 0:
#                 print(f"Contract {new_contract} canceled successfully.")

#                 # Remove the contract from active_contracts.json
#                 with open(active_contracts_file, 'r+') as file:
#                     active_contracts = json.load(file)
#                     active_contracts["active_contracts"].remove(int(new_contract))
#                     file.seek(0)
#                     json.dump(active_contracts, file, indent=4)
#                     file.truncate()
#             else:
#                 print(f"Failed to cancel contract {new_contract}. Error: {cancel_error.decode('utf-8')}")
#         else:
#             print(f"Failed to extract new contract ID from the response: {rent_output.decode('utf-8')}")
#     else:
#         print(f"Failed to rent machine {assigned_machine_id}. Error: {rent_error.decode('utf-8')}")

# def lifecycle(assignments_file):
#     # Ensure assignments file exists
#     if not os.path.exists(assignments_file):
#         print(f"Assignments file not found: {assignments_file}")
#         sys.exit(1)

#     with open(assignments_file, 'r') as file:
#         assignments = json.load(file)
#     script_dir = os.path.dirname(os.path.realpath(__file__))
    
#     # Ensure active_contracts.json exists
#     active_contracts_file = os.path.join(script_dir, 'active_contracts.json')
#     if not os.path.exists(active_contracts_file):
#         with open(active_contracts_file, 'w') as file:
#             json.dump({"active_contracts": []}, file)

#     with ThreadPoolExecutor() as executor:
#         futures = []
#         for machine, details in assignments.items():
#             futures.append(executor.submit(rent_and_cancel_machine, machine, details, script_dir, active_contracts_file))

#         for future in as_completed(futures):
#             try:
#                 future.result()
#             except Exception as e:
#                 print(f"Exception occurred: {e}")

# def main():
#     if len(sys.argv) != 2:
#         print("Usage: python3 lifecycle.py <assignments_file>")
#         sys.exit(1)

#     assignments_file = sys.argv[1]
#     lifecycle(assignments_file)

# if __name__ == "__main__":
#     main()