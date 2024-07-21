import os
import sys

def log_command(command, output, contract_id):
    log_dir = os.path.join(os.path.dirname(os.path.dirname(os.path.realpath(__file__))), 'logs', str(contract_id))
    os.makedirs(log_dir, exist_ok=True)
    log_file = os.path.join(log_dir, 'commands.log')

    with open(log_file, 'a') as f:
        f.write(f"Command: {command}\n")
        f.write(f"Output: {output}\n\n")

if __name__ == "__main__":
    if len(sys.argv) != 4:
        print("Usage: python command_logger.py <command> <output> <contract_id>")
        sys.exit(1)

    command = sys.argv[1]
    output = sys.argv[2]
    contract_id = sys.argv[3]
    log_command(command, output, contract_id)