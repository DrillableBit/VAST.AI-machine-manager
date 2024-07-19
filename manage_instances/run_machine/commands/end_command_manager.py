import subprocess
from run_machine.command_logger import log_command

def run_command(command, contract_id):
    try:
        result = subprocess.run(command, shell=True, check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        output = result.stdout.decode('utf-8')
        log_message = f"Command '{command}' for contract ID {contract_id} succeeded with output:\n{output}"
        print(log_message)
    except subprocess.CalledProcessError as e:
        output = e.stderr.decode('utf-8')
        log_message = f"Command '{command}' for contract ID {contract_id} failed with error:\n{output}"
        print(log_message)

    # Log the command and output
    log_command(command, output, contract_id)

def run_end_command(command, contract_id):
    run_command(command, contract_id)