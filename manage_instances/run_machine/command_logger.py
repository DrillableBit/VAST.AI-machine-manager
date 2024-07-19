import os

def log_command(command, output, contract_id):
    log_dir = os.path.join(os.path.dirname(os.path.dirname(os.path.realpath(__file__))), 'logs', str(contract_id))
    os.makedirs(log_dir, exist_ok=True)
    log_file = os.path.join(log_dir, 'commands.log')

    with open(log_file, 'a') as f:
        f.write(f"Command: {command}\n")
        f.write(f"Output: {output}\n\n")