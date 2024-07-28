import time
import subprocess

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