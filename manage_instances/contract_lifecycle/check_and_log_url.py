import json
import sys
import subprocess
import logging
import time
import re
import os

def log_command(contract_id, command, output):
    logging.basicConfig(filename='/tmp/machine_manager.log', level=logging.INFO)
    logging.info(f"Contract ID: {contract_id}, Command: {command}, Output: {output}")

def read_json(json_file):
    with open(json_file, 'r') as file:
        return json.load(file)

def get_contract_info(json_data, contract_id):
    for key, value in json_data.items():
        if value.get("contract_id") == contract_id:
            return value
    return {}

def check_storage_path(contract_info, contract_id):
    storage_path = contract_info.get('output_storage')
    
    if storage_path:
        log_command(contract_id, "Check Storage Path", f"Storage path specified: {storage_path}")
    else:
        log_command(contract_id, "Check Storage Path", "No storage path specified in the JSON.")
    
    return storage_path

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

def parse_ssh_url(ssh_url):
    match = re.match(r'ssh://(.*)@(.*):(\d+)', ssh_url)
    if not match:
        raise ValueError(f"Invalid SSH URL format: {ssh_url}")
    
    user = match.group(1)
    host = match.group(2)
    port = match.group(3)
    return user, host, port

def create_directory_if_not_exists(path):
    if not os.path.exists(path):
        os.makedirs(path)
        print(f"Created directory: {path}")
        log_command(contract_id, "Create Directory", f"Created directory: {path}")

def remote_directory_exists(user, host, port, remote_path):
    try:
        check_command = f"ssh -p {port} {user}@{host} '[ -d {remote_path} ]'"
        result = subprocess.run(check_command, shell=True, check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        return result.returncode == 0
    except subprocess.CalledProcessError as e:
        print(f"Error checking remote directory: {e.stderr.decode('utf-8')}")
        return False

def scp_from_remote(contract_id, user, host, port, local_path, remote_path):
    create_directory_if_not_exists(local_path)  # Ensure the local directory exists

    if remote_directory_exists(user, host, port, remote_path):
        try:
            scp_command = f"scp -r -P {port} {user}@{host}:{remote_path} {local_path}"
            result = subprocess.run(scp_command, shell=True, check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            print(f"Successfully copied {remote_path} from {host} to {local_path}.")
            log_command(contract_id, "SCP from Remote", f"Successfully copied {remote_path} from {host} to {local_path}.")
        except subprocess.CalledProcessError as e:
            print(f"Failed to copy from remote: {e.stderr.decode('utf-8')}")
            log_command(contract_id, "SCP from Remote", f"Failed to copy from remote: {e.stderr.decode('utf-8')}")
    else:
        print(f"Remote directory {remote_path} does not exist on {host}.")
        log_command(contract_id, "Check Remote Directory", f"Remote directory {remote_path} does not exist on {host}.")

def adjust_path(path):
    if path.startswith('@relative_path/'):
        script_dir = os.path.dirname(os.path.realpath(__file__))
        adjusted_path = os.path.join(script_dir, '..', path.replace('@relative_path/', ''))
        return os.path.abspath(adjusted_path)
    return path

if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage: python3 check_and_log_url.py <json_file> <contract_id>")
        sys.exit(1)
    
    json_file = sys.argv[1]
    contract_id = sys.argv[2]
    
    json_data = read_json(json_file)
    contract_info = get_contract_info(json_data, contract_id)
    output_storage_path = check_storage_path(contract_info, contract_id)
    print(f"Output_storage Path: {output_storage_path}")  # Debug print
    
    if output_storage_path:
        ssh_url = get_ssh_url(contract_id)

        if ssh_url:
            print(f"Copying: /root/storage To:{output_storage_path} from Contract: {contract_id} using {ssh_url}")
            user, host, port = parse_ssh_url(ssh_url)
            output_storage_path = adjust_path(output_storage_path)
            local_path = output_storage_path  # The local path to copy TO
            remote_path = "/root/storage"  # The remote path to copy FROM, adjusted to match the specific path
            scp_from_remote(contract_id, user, host, port, local_path, remote_path)
        else:
            print(f"Failed to retrieve SSH URL for contract ID {contract_id}.")
            sys.exit(1)
    else:
        print("No output_storage path specified.")
        sys.exit(1)

# import json
# import sys
# import subprocess
# import logging
# import time
# import re
# import os 

# def log_command(contract_id, command, output):
#     logging.basicConfig(filename='/tmp/machine_manager.log', level=logging.INFO)
#     logging.info(f"Contract ID: {contract_id}, Command: {command}, Output: {output}")

# def read_json(json_file):
#     with open(json_file, 'r') as file:
#         return json.load(file)

# def get_contract_info(json_data, contract_id):
#     for key, value in json_data.items():
#         if value.get("contract_id") == contract_id:
#             return value
#     return {}

# def check_storage_path(contract_info, contract_id):
#     storage_path = contract_info.get('output_storage')
    
#     if storage_path:
#         log_command(contract_id, "Check Storage Path", f"Storage path specified: {storage_path}")
#     else:
#         log_command(contract_id, "Check Storage Path", "No storage path specified in the JSON.")
    
#     return storage_path

# def get_ssh_url(contract_id, retries=3, delay=5):
#     for attempt in range(retries):
#         try:
#             result = subprocess.run(f"vastai ssh-url {contract_id}", shell=True, check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
#             ssh_url = result.stdout.decode('utf-8').strip()
#             if ssh_url:
#                 return ssh_url
#         except subprocess.CalledProcessError as e:
#             print(f"Attempt {attempt + 1} to get SSH URL for contract ID {contract_id} failed with error:\n{e.stderr.decode('utf-8')}")
        
#         print(f"Retrying in {delay} seconds...")
#         time.sleep(delay)
    
#     print(f"Failed to get SSH URL for contract ID {contract_id} after {retries} attempts.")
#     return None

# def parse_ssh_url(ssh_url):
#     match = re.match(r'ssh://(.*)@(.*):(\d+)', ssh_url)
#     if not match:
#         raise ValueError(f"Invalid SSH URL format: {ssh_url}")
    
#     user = match.group(1)
#     host = match.group(2)
#     port = match.group(3)
#     return user, host, port

# def create_directory_if_not_exists(path):
#     if not os.path.exists(path):
#         os.makedirs(path)
#         print(f"Created directory: {path}")
#         log_command(contract_id, "Create Directory", f"Created directory: {path}")



# def scp_from_remote(contract_id, user, host, port, local_path, remote_path="/root/storage"):
#     create_directory_if_not_exists(local_path) 

#     try:
#         scp_command = f"scp -r -P {port} {user}@{host}:{remote_path} {local_path}"
#         subprocess.run(scp_command, shell=True, check=True)
#         print(f"Successfully copied {remote_path} from {host} to {local_path}.")
#         log_command(contract_id, "SCP from Remote", f"Successfully copied {remote_path} from {host} to {local_path}.")
#     except subprocess.CalledProcessError as e:
#         print(f"Failed to copy from remote: {e}")
#         log_command(contract_id, "SCP from Remote", f"Failed to copy from remote: {e}")

# def adjust_path(path):
#     if path.startswith('@relative_path/'):
#         script_dir = os.path.dirname(os.path.realpath(__file__))
#         adjusted_path = os.path.join(script_dir, '..', path.replace('@relative_path/', ''))
#         return os.path.abspath(adjusted_path)
#     return path

# if __name__ == "__main__":
#     if len(sys.argv) != 3:
#         print("Usage: python3 check_and_log_url.py <json_file> <contract_id>")
#         sys.exit(1)
    
#     json_file = sys.argv[1]
#     contract_id = sys.argv[2]
    
#     json_data = read_json(json_file)
#     contract_info = get_contract_info(json_data, contract_id)
#     output_storage_path = check_storage_path(contract_info, contract_id)
#     print(f"Output_storage Path: {output_storage_path}")  # Debug print
    
#     if output_storage_path:
#         ssh_url = get_ssh_url(contract_id)

#         if ssh_url:
#             print(f"Copying: {output_storage_path} from Contract: {contract_id} using {ssh_url}")
#             user, host, port = parse_ssh_url(ssh_url)
#             output_storage_path = adjust_path(output_storage_path) 
#             local_path = output_storage_path  # The local path to copy TO
#             remote_path = "/root/storage"  # The remote path to copy FROM;
#             scp_from_remote(contract_id, user, host, port, local_path, output_storage_path)
#         else:
#             print(f"Failed to retrieve SSH URL for contract ID {contract_id}.")
#             sys.exit(1)
#     else:
#         print("No output_storage path specified.")
#         sys.exit(1)