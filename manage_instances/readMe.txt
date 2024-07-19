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


