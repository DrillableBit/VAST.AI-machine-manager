import json
import os
from command_logger import log_command

# Path to the JSON file storing active connections
active_connections_file = 'active_connections.json'

def read_active_connections():
    if os.path.exists(active_connections_file):
        with open(active_connections_file, 'r') as f:
            return json.load(f)
    return {}

def write_active_connections(connections):
    with open(active_connections_file, 'w') as f:
        json.dump(connections, f, indent=4)

def record_pid(contract_id, pid, user, host, port, tunnel_port, local_port):
    print("WROTE CONNECTION PID")
    connections = read_active_connections()
    connections[contract_id] = {
        'pid': pid,
        'user': user,
        'host': host,
        'port': port,
        'tunnel_port': tunnel_port,
        'local_port': local_port
    }
    write_active_connections(connections)
    log_command("Record PID", f"Recorded PID {pid} for contract ID {contract_id}", contract_id)
    print(f"Recorded PID {pid} for contract ID {contract_id}")


import signal

def terminate_tunnel_by_contract_id(contract_id):
    connections = read_active_connections()
    if contract_id in connections:
        pid = connections[contract_id]['pid']
        try:
            os.kill(pid, signal.SIGTERM)
            log_command("Terminate Tunnel", f"Terminated SSH tunnel with PID {pid} for contract ID {contract_id}", contract_id)
            print(f"Terminated SSH tunnel with PID {pid} for contract ID {contract_id}")
            del connections[contract_id]
            write_active_connections(connections)
        except ProcessLookupError:
            log_command("Terminate Tunnel", f"No process with PID {pid} found.", contract_id)
            print(f"No process with PID {pid} found.")
        except Exception as e:
            log_command("Terminate Tunnel", f"Failed to terminate SSH tunnel with PID {pid}: {str(e)}", contract_id)
            print(f"Failed to terminate SSH tunnel with PID {pid}: {str(e)}")
    else:
        log_command("Terminate Tunnel", f"No active connection found for contract ID {contract_id}", contract_id)
        print(f"No active connection found for contract ID {contract_id}")


def terminate_all_tunnels():
    connections = read_active_connections()
    for contract_id, info in connections.items():
        pid = info['pid']
        try:
            os.kill(pid, signal.SIGTERM)
            log_command("Terminate All Tunnels", f"Terminated SSH tunnel with PID {pid} for contract ID {contract_id}", contract_id)
            print(f"Terminated SSH tunnel with PID {pid} for contract ID {contract_id}")
        except ProcessLookupError:
            log_command("Terminate All Tunnels", f"No process with PID {pid} found for contract ID {contract_id}", contract_id)
            print(f"No process with PID {pid} found.")
        except Exception as e:
            log_command("Terminate All Tunnels", f"Failed to terminate SSH tunnel with PID {pid} for contract ID {contract_id}: {str(e)}", contract_id)
            print(f"Failed to terminate SSH tunnel with PID {pid}: {str(e)}")
    # Clear the JSON file
    write_active_connections({})
    print("All SSH tunnels terminated.")
    log_command("Terminate All Tunnels", "All SSH tunnels terminated.", "ALL")