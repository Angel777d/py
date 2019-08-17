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
echo "modules from requirements.txt installed"
;;

stop)
pkill -f run.py
echo "home_bot stopped"
;;

*) # default case
nohup python3 run.py &
echo "home_bot started pid" $!
echo "use ./run.sh stop to stop service."
echo "use ./run.sh setup to setup bot environment."
echo "\r\n"

esac

exit 0
