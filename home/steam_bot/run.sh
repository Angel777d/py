#!/bin/bash

# script_name=$0
run_option=$1


case ${run_option} in

setup)
echo "setup python env for home bot"
python3 -m venv env
echo "env created"
source ./env/bin/activate
echo "env activated"
python3 -m pip install -r requirements.txt
export PYTHONPATH=$PYTHONPATH:$DIRSTACK"/../base_bot":$DIRSTACK"/../localization"
echo "modules from requirements.txt installed"
echo "PYTHONPATH " $PYTHONPATH
;;

stop)
pkill -f steam_bot.py
echo "steam_bot stopped"
;;

*) # default case
source ./env/bin/activate
nohup python3 steam_bot.py &
echo "steam_bot started pid" $!
echo "use ./run.sh stop to stop service."
echo "use ./run.sh setup to setup bot environment."
echo "\r\n"

esac

exit 0
