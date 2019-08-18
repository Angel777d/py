#!/bin/bash

run_option=$1
script_name="steam_bot.py"
env_name=".env"
parent_dir="$(dirname "$PWD")"

case ${run_option} in

setup)
echo "setup python env for home bot"
python3 -m venv ${env_name}
echo "env created"
# shellcheck source=./.env/bin/activate
source ./${env_name}/bin/activate
echo "env activated"
python3 -m pip install -r requirements.txt
echo "modules from requirements.txt installed"
export PYTHONPATH=$PYTHONPATH:${parent_dir}"/base_bot":${parent_dir}"/localization"
echo "PYTHONPATH " $PYTHONPATH
deactivate
echo "Setup is done."
;;

stop)
pkill -f ${script_name}
echo "steam_bot stopped"
;;

*) # default case
 # shellcheck source=./.env/bin/activate
source ./${env_name}/bin/activate
nohup python3 ${script_name} &
echo "steam_bot started pid" $!
echo "use ./run.sh stop to stop service."
echo "use ./run.sh setup to setup bot environment."
printf "\r\n"

esac

exit 0
