# VAST.AI Host Machine Manager

Manage your VAST.AI host machines with ease. Automate renting, running commands, and managing tasks on multiple machines through a simple configuration.

---

## 📋 Setup Instructions

1. **Add your machine IDs**:
   - Populate the `my_machines.txt` file with your VAST.AI machine IDs.

2. **Configure commands and tasks**:
   - Define your desired setup in `config.yaml`.

3. **(Optional)**: Create custom tasks.
   - Add your custom tasks to `/run_machine/tasks/tasklist`.

4. **Setup SSH keys and VAST.AI API key**:
   - Ensure your keys are set up properly.

5. **Set executable permissions**:
   ```bash
   chmod +x run.sh
   chmod +x exit.sh
🚀 Commands
./run.sh
Purpose: Rents all your machines, executes the commands in config.yaml, and optionally cancels contracts after the set duration.
Auto-cancellation: If a duration is specified in config.yaml, contracts are automatically canceled after completion.
./exit.sh
Purpose: Cancels all active contracts forcibly.
Use case: Useful when you need to stop processes manually or if run.sh was interrupted.
📂 Logs & Results
Logs and results are stored in the logs directory and sorted by contract ID.

🛠️ Customizing Tasks
Add a file containing your custom tasklist in /run_machine/tasks/tasklist.
Assign the file by adding its name to the task key in config.yaml.
⚙️ YAML Configuration
Define machine filters and contract-specific settings in config.yaml.

Global Filters
Filters to customize machine searches:

yaml
Copy
Edit
global_filters:
  min_cuda: 12.2           # Minimum CUDA version
  max_cuda: 12.2           # Maximum CUDA version
  min_nv_driver: 535       # Minimum NVIDIA driver version
  max_nv_driver: 535       # Maximum NVIDIA driver version
  min_vCPU: 5              # Minimum virtual CPUs
  max_vCPU: 60             # Maximum virtual CPUs
  priority_condition: vCPUs # Criteria for assigning priority
Contracts
Define settings for individual machines:

yaml
Copy
Edit
contracts:
  machine_1:                   # Assign a name to your machine
    priority: 0                # Lower priority = better match based on priority_condition
    image: pytorch/pytorch     # VAST.AI Docker container
    disk: 32                   # Disk space in GB
    duration: 30               # Time (in seconds) to keep the machine alive
    tunnel_port: 8888          # SSH tunnel port
    local_port: 8888           # Optional local port mapping
    start_command: ls          # Command to run at start (optional)
    task: jupyter_lab          # Task file to execute (optional)
    end_command: uptime        # Command to run at the end (optional)

  machine_2:
    priority: 0
    image: pytorch/pytorch
    disk: 32
    duration: 3000
    start_command: whoami
    task: jupyter_lab
    end_command: ls
🧹 Cleaning Up
Run the following to forcibly cancel all contracts:

bash
Copy
Edit
./exit.sh
📖 Notes
Remember to set up SSH keys and the VAST.AI API key before running any commands.
Customize tasks through /run_machine/tasks/tasklist.
