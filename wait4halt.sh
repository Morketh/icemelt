#!/bin/bash

# This script will search and wait for Cold-air-funnel.py to finish before shutting down

PID=$(ps aux | grep "[C]old-air-funnel.py" | awk '{print $2}')

#first lets create/wipe ice.log and append all output to it
echo "$(date) Waiting for $PID to die before shutdown." | tee ice.log
echo "$(ps aux | grep '[C]old-air-funnel.py')" | tee -a ice.log

while [[ -n $(ps aux | grep "[C]old-air-funnel.py" | awk '{print $2}') ]]
do
#	sleep 3
#	echo $PID
	true
done
echo "$PID died....." | tee -a ice.log
echo "$(date) System is now halting" | tee -a ice.log
halt
