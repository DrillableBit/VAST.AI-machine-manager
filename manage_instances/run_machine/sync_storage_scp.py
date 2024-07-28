import subprocess
import sys
import os
import logging



def log_command(contract_id, command, output):
    logging.basicConfig(filename='/tmp/machine_manager.log', level=logging.INFO)
    logging.info(f"Contract ID: {contract_id}, Command: {command}, Output: {output}")

def scp_to_remote(contract_id, user, host, port, local_path, remote_path="/root/storage"):
    try:
        scp_command = f"scp -r -P {port} {local_path} {user}@{host}:{remote_path}"
        subprocess.run(scp_command, shell=True, check=True)
        print(f"Successfully copied {local_path} to {remote_path} on {host}.")
        log_command(contract_id, "SCP to Remote", f"Successfully copied {local_path} to {remote_path} on {host}.")
    except subprocess.CalledProcessError as e:
        print(f"Failed to copy to remote: {e}")
        log_command(contract_id, "SCP to Remote", f"Failed to copy to remote: {e}")

def scp_from_remote(contract_id, user, host, port, local_path, remote_path="/root/storage"):
    try:
        scp_command = f"scp -r -P {port} {user}@{host}:{remote_path} {local_path}"
        subprocess.run(scp_command, shell=True, check=True)
        print(f"Successfully copied {remote_path} from {host} to {local_path}.")
        log_command(contract_id, "SCP from Remote", f"Successfully copied {remote_path} from {host} to {local_path}.")
    except subprocess.CalledProcessError as e:
        print(f"Failed to copy from remote: {e}")
        log_command(contract_id, "SCP from Remote", f"Failed to copy from remote: {e}")

if __name__ == "__main__":
    if len(sys.argv) != 7:
        print("Usage: python3 sync_storage_scp.py <contract_id> <user> <host> <port> <local_path> <direction>")
        print("direction should be 'to' or 'from'")
        sys.exit(1)
    
    contract_id = sys.argv[1]
    user = sys.argv[2]
    host = sys.argv[3]
    port = int(sys.argv[4])
    local_path = sys.argv[5]
    direction = sys.argv[6]

    if direction == 'to':
        scp_to_remote(contract_id, user, host, port, local_path)
    elif direction == 'from':
        scp_from_remote(contract_id, user, host, port, local_path)
    else:
        print("Invalid direction. Use 'to' for copying to remote or 'from' for copying from remote.")
        sys.exit(1)