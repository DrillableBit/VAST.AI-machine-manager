import subprocess
from run_machine.command_logger import log_command
import time
from run_machine.ssh_helpers import record_pid

def initiate_ssh_tunnel(contract_id, user, host, port, remote_port, local_port):
    try:
        # Construct the SSH tunnel command with options for StrictHostKeyChecking and LogLevel
        # tunnel_command = f"ssh -o StrictHostKeyChecking=no -fN -L {local_port}:localhost:{remote_port} {user}@{host}"
        tunnel_command = f"ssh -fN -L {local_port}:localhost:{remote_port} {user}@{host} -p {port}"
        # Start the SSH tunnel
        subprocess.run(tunnel_command, shell=True, check=True)
        print(f"SSH tunnel established on local port {local_port} to remote port {remote_port} on {user}@{host}.")
        log_command(contract_id=contract_id, command="SSH-Tunnel", output=f"SSH tunnel established on local port {local_port} to remote port {remote_port} on {user}@{host}.")
    except subprocess.CalledProcessError as e:
        error_message = f"Failed to establish SSH tunnel: {e}"
        print(error_message)
        log_command(contract_id=contract_id, command="SSH-Tunnel", output=f"{error_message}")
        raise e
