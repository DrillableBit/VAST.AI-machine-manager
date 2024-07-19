# import subprocess

# def run_command(command, contract_id):
#     print(command, contract_id)

# def run_task(task, contract_id, details):
#     if task == 'jupyter_lab':
#         # Example of running Jupyter Lab
#         command = "jupyter lab"
#         run_command(command, contract_id)
#         # You can expand this to include more complex task logic
#     else:
#         print(f"Unknown task '{task}' for contract ID {contract_id}")


import subprocess
import os

from command_logger import log_command

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

def run_task(task, contract_id, details):
    log_command(f"Task {task}", 'Attempting to find task file.', contract_id)
    task_dir = os.path.join(os.path.dirname(os.path.realpath(__file__)), 'tasklist')
    task_formats = ['.sh', '.py', '.pl']

    task_file = None
    for format in task_formats:
        potential_task_file = os.path.join(task_dir, f"{task}{format}")
        if os.path.isfile(potential_task_file):
            task_file = potential_task_file
            break
    
    if task_file:
        print(f"Running task file '{task_file}' for contract ID {contract_id}")
        log_command(f"Task {task}", f'Task file {task_file} initiated.', contract_id)
        if task_file.endswith('.sh'):
            run_command(f"bash {task_file}", contract_id)
        elif task_file.endswith('.py'):
            run_command(f"python3 {task_file}", contract_id)
        elif task_file.endswith('.pl'):
            run_command(f"perl {task_file}", contract_id)
    else:
        print(f"Unknown task '{task}' for contract ID {contract_id}")
        log_command(f"Task {task}", 'Unknown task.', contract_id)