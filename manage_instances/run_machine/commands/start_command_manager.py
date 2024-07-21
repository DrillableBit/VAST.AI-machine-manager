import subprocess
from run_machine.command_logger import log_command
from run_machine.parse_ssh_url import parse_ssh_url

def run_command_manager(command, contract_id, ssh_url):
    try:
        user, host, port = parse_ssh_url(ssh_url)
        
        full_command = f"ssh -o StrictHostKeyChecking=no -o LogLevel=ERROR {user}@{host} -p {port} '{command}'"
        
        print(f"Executing Start command: {full_command}")
        
        result = subprocess.run(full_command, shell=True, check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        output = result.stdout.decode('utf-8')
        log_message = f"Start command '{command}' for contract ID {contract_id} succeeded with output:\n{output}"
        print(log_message)
    except ValueError as ve:
        output = str(ve)
        log_message = f"Start command failed to parse SSH URL for contract ID {contract_id} with error:\n{output}"
        print(log_message)
    except subprocess.CalledProcessError as e:
        output = e.stderr.decode('utf-8')
        log_message = f"Start command '{command}' for contract ID {contract_id} failed with error:\n{output}"
        print(log_message)

    # Log the command and output
    log_command(command, output, contract_id)

def run_start_command_manager(command, contract_id, ssh_url):
    run_command_manager(command, contract_id, ssh_url)