*** Remember to set up ssh keys and vastai api key ***

Add your machine IDs to my_machines.txt

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