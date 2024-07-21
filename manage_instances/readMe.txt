VAST.AI host machine manager

Add your machine ids to my_machines.txt
Set up the desired commands and tasks in config.yaml
create optional custom tasks in run_machine/tasks/tasklist

*** Remember to set up ssh keys and vastai api key ***

Create a my_machines.txt file in the root directory. 
Add your machine IDs to my_machines.txt
It should look something like:

39919
20199
...
...

Run: 
chmod +x run.sh
chmod +x exit.sh

use config.yaml to set up tasks. 


______________________________________________________

run.sh rents all your machines, then executes commands set up in config.yaml
it then autocancels the contracts after the duration, if a duration is set. 

exit.sh can be used if you had to cancel the run.sh script, and want to force exit out of all contracts. 

logs and results are available at logs - sorted by the contract ID
customize tasks through /run_machine/tasks/tasklist   
- add a file with the tasklist.
- assign the file through adding the filename to your yaml "task: "




Yaml config:

global_filters:                               - Filters the machine search for the desired specifications.  
  min_cuda: 12.2
  max_cuda: 12.2
  min_nv_driver: 535
  max_nv_driver: 535
  min_vCPU: 5
  max_vCPU: 60
  priority_condition: vCPUs                  - Feature to sort for when assigning priority. 

contracts: 
   machine_1:                               - Name your machines anything.
     priority: 0                            - priority assigns resources based on priority. Lower priority = better machine based on priority_condition. 
     image: pytorch/pytorch                 - vast docker container to base the machine on.
     disk: 32                               - assigned diskspace (GB)
     duration: 30                           - seconds the machine will be kept alive
     tunnel_port: 8888                      - set up a ssh tunnel - defaults local port to same as tunnel port. 
     local_port: 8888                       - optional local port mapping
     start_command: ls                      - run start command (optional)
     task: jupyter_lab                      - copy over and run a task file (optional) 
     end_command: uptime                    - run end command (optional)

  machine_2: 
     priority: 0
     image: pytorch/pytorch
     disk: 32
     duration: 3000
     task: jupyter_lab
     start_command: whoami
     end_command: ls