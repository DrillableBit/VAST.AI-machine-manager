import subprocess
import os
import time
import sys
from run_machine.command_logger import log_command
from run_machine.parse_ssh_url import parse_ssh_url

def run_command(command, contract_id, ssh_url, tunnel_port):
    try:
        user, host, port = parse_ssh_url(ssh_url)
        
        full_command = f"ssh -o StrictHostKeyChecking=no -o LogLevel=ERROR {user}@{host} -p {port} '{command} {tunnel_port}'"
        
        print(f"Executing command: {full_command}")
        log_command(contract_id=contract_id, command="Vast.AI_Task_Manager",output=f"Executing command: {full_command}")
        
        process = subprocess.Popen(full_command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
        while True:
            output = process.stdout.readline()
            if output:
                print(output.strip())
                log_command(contract_id=contract_id, command="Vast.AI_Task_Manager",output=output.strip())

            error = process.stderr.readline()
            if error:
                print(error.strip(), file=sys.stderr)
                log_command(contract_id=contract_id, command="Vast.AI_Task_Manager",output=(f"Error: {error.strip()}, File: {sys.stderr}") )
            
            if output == '' and error == '' and process.poll() is not None:
                break

        return_code = process.poll()
        if return_code != 0:
            raise subprocess.CalledProcessError(return_code, command)
    except ValueError as ve:
        output = str(ve)
        log_message = f"Command failed to parse SSH URL for contract ID {contract_id} with error:\n{output}"
        print(log_message)
        log_command(command, log_message, contract_id)
    except subprocess.CalledProcessError as e:
        output = e.stderr.decode('utf-8')
        log_message = f"Command '{command}' for contract ID {contract_id} failed with error:\n{output}"
        print(log_message)
        log_command(command, log_message, contract_id)

    # Log the command and output
    log_command(command, output, contract_id)

def run_task_manager(task, contract_id, details, ssh_url, tunnel_port=None):
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
        
        # Copy the task file to the remote machine
        user, host, port = parse_ssh_url(ssh_url)
        scp_command = f"scp -P {port} {task_file} {user}@{host}:/tmp/"
        subprocess.run(scp_command, shell=True, check=True)
        
        # Run the task file on the remote machine
        remote_task_file = f"/tmp/{os.path.basename(task_file)}"
        # run_command(f"python3 {remote_task_file} {tunnel_port}", contract_id, ssh_url, tunnel_port)
        run_command(f"python3 {remote_task_file}", contract_id, ssh_url, tunnel_port)
        # Stream the log file from the remote machine
        log_file_path = "/tmp/machine_manager_setup.log"
        # log_file_path = "/tmp/jupyter_lab_setup.log"
        stream_log_file(contract_id, ssh_url, log_file_path)
    else:
        print(f"Unknown task '{task}' for contract ID {contract_id}")
        log_command(f"Task {task}", 'Unknown task.', contract_id)

def stream_log_file(contract_id, ssh_url, log_file_path, interval=30):
    user, host, port = parse_ssh_url(ssh_url)
    remote_log_file = f"{user}@{host}:{log_file_path}"
    success_message = "Task completed successfully."

    while True:
        try:
            scp_command = f"scp -P {port} {remote_log_file} /tmp/{contract_id}_machine_manager_setup.log"
            # scp_command = f"scp -P {port} {remote_log_file} /tmp/{contract_id}_jupyter_lab_setup.log"
            result = subprocess.run(scp_command, shell=True, capture_output=True, text=True)
            log_command(scp_command, result.stdout + result.stderr, contract_id)  # Log the command and output

            if result.returncode != 0:
                error_message = f"Failed to fetch log file for contract ID {contract_id} with error:\n{result.stderr}"
                print(error_message)
                log_command("SCP Command Error", error_message, contract_id)
                break

            # with open(f"/tmp/{contract_id}_jupyter_lab_setup.log", 'r') as f:
            with open(f"/tmp/{contract_id}_machine_manager_setup.log", 'r') as f:
                log_content = f.read()
                print(f"Displaying machine log for {contract_id}:")
                print(log_content)
                log_command("Reading log file content", log_content, contract_id)  # Log the log file content

                if success_message in log_content:
                    print("Installation complete. Stopping log streaming.")
                    log_command("Hey from log content! Installation complete", "Jupyter Lab installed successfully.", contract_id)
                    break

            time.sleep(interval)
        except subprocess.CalledProcessError as e:
            error_message = f"Failed to fetch log file for contract ID {contract_id} with error:\n{e.stderr.decode('utf-8')}"
            print(error_message)
            log_command("Exception in stream_log_file", error_message, contract_id)  # Log the exception
            break
