import time
import subprocess
import sys
import os
import json

# Add the current directory to the system path
sys.path.append(os.path.dirname(os.path.realpath(__file__)))

from run_machine.parse_ssh_url import parse_ssh_url
from run_machine.commands.start_command_manager import run_start_command_manager
from run_machine.commands.end_command_manager import run_end_command_manager
from run_machine.tasks.task_manager import run_task_manager
from run_machine.command_logger import log_command
from run_machine.initiate_ssh_tunnel import initiate_ssh_tunnel

def get_ssh_url(contract_id, retries=3, delay=5):
    for attempt in range(retries):
        try:
            result = subprocess.run(f"vastai ssh-url {contract_id}", shell=True, check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            ssh_url = result.stdout.decode('utf-8').strip()
            if ssh_url:
                return ssh_url
        except subprocess.CalledProcessError as e:
            print(f"Attempt {attempt + 1} to get SSH URL for contract ID {contract_id} failed with error:\n{e.stderr.decode('utf-8')}")
        
        print(f"Retrying in {delay} seconds...")
        time.sleep(delay)
    
    print(f"Failed to get SSH URL for contract ID {contract_id} after {retries} attempts.")
    return None


def wait_for_ssh_connection(contract_id, ssh_url, timeout=300, interval=10):
    user, host, port = parse_ssh_url(ssh_url)
    start_time = time.time()
    attempt = 0

    while True:
        attempt += 1
        elapsed_time = time.time() - start_time
        remaining_time = timeout - elapsed_time
        
        if remaining_time <= 0:
            print(f"SSH connection timed out after {timeout} seconds.")
            return False
        log_command(contract_id=contract_id,command="SSH",output=f"Attempt: {attempt} - Attempting to establish connection to: {user}@{host} -p {port}.")
        print(f"Attempt: {attempt} - awaiting client SSH initiation at: Contract {contract_id}: {user}@{host}:{port}.")
        print(f"Trying again in {interval} seconds. Remaining time before termination: {int(remaining_time)} seconds.")
        full_command = f"ssh -o StrictHostKeyChecking=no -o LogLevel=ERROR {user}@{host} -p {port} 'echo connection successful'"
        try:
            result = subprocess.run(full_command, shell=True, check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            if result.returncode == 0:
                print("SSH connection successful.")
                return True
        except subprocess.CalledProcessError:
            pass

        time.sleep(interval)


def manage_machine(contract_id, details):
    try:
        contract_id = int(contract_id)
        log_command(contract_id=contract_id,command="Vast.AI_Machine_Manager",output=f"Vast.AI_Machine_Manager succesfully engaged. Managing machine {details}")
        log_command(contract_id=contract_id,command="SSH-URL",output="Attempting to obtain SSH url.")
        ssh_url = get_ssh_url(contract_id)
        if not ssh_url:
            print(f"Could not obtain SSH URL for contract ID {contract_id}. Exiting...")
            log_command(contract_id=contract_id,command="SSH-URL",output="Unable to obtain SSH url.")
            return
        

        log_command(contract_id=contract_id,command="SSH-URL",output=F"Sucessfully obtained SSH url: {ssh_url}")
        start_command = details.get('start_command')
        task = details.get('task')
        end_command = details.get('end_command')
        tunnel_port = details.get('tunnel_port')
        local_port = details.get('local_port', tunnel_port)
        
        if not wait_for_ssh_connection(contract_id, ssh_url):
            print(f"Could not establish SSH connection for contract ID {contract_id}. Exiting...")
            log_command(contract_id=contract_id,command="SSH",output="Unable to establish SSH connection.")
            return
            
        log_command(contract_id=contract_id,command="SSH",output="Sucessfully established SSH connection.")

        if tunnel_port:
            user, host, port = parse_ssh_url(ssh_url)
            log_command(contract_id=contract_id,command="SSH",output=f"Establishing SSH tunnel from local port {local_port} to remote port {tunnel_port}")
            print(f"Establishing SSH tunnel from local port {local_port} to remote port {tunnel_port}")
            initiate_ssh_tunnel(contract_id, user, host, port, tunnel_port, local_port)

        if start_command:
            print(f"Running start command for contract ID {contract_id}")
            run_start_command_manager(start_command, contract_id, ssh_url)
        
        if task:
            print(f"Running task for contract ID {contract_id}")
            run_task_manager(task, contract_id, details, ssh_url, tunnel_port)
        
        if end_command:
            print(f"Running end command for contract ID {contract_id}")
            run_end_command_manager(end_command, contract_id, ssh_url)

        # Path to the active contracts file
        script_dir = os.path.dirname(os.path.realpath(__file__))
        active_contracts_file = os.path.join(script_dir, '..', 'contract_lifecycle', 'active_contracts.json')

        # Check if the active contracts file exists
        if not os.path.exists(active_contracts_file):
            print(f"Active contracts file not found: {active_contracts_file}")
            sys.exit(1)

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
        log_command(contract_id=contract_id, command="Vast.AI_Machine_Manager",output=f"An error occurred while managing the machine with contract ID {contract_id}: {e}")

if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage: python3 machine_manager.py <contract_id> <details>")
        sys.exit(1)
    
    contract_id = sys.argv[1]
    details = json.loads(sys.argv[2])
    
    manage_machine(contract_id, details)
