VAST.AI host machine manager

Add your machine ids to my_machines.txt
Set up the desired commands and tasks in config.yaml
create optional custom tasks in run_machine/tasks/tasklist

Setup ________________________________________________
  *** Remember to set up ssh keys and vastai api key ***
  Run: 
  chmod +x run.sh
  chmod +x exit.sh
______________________________________________________

Commands  ____________________________________________
./run.sh rents all your machines, then executes commands set up in config.yaml
it then autocancels the contracts after the duration, if a duration is set. 

./exit.sh can be used if you had to cancel the run.sh script, and want to force exit out of all contracts. 
______________________________________________________
