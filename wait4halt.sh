#!/bin/bash

# This script will search and wait for Cold-air-funnel.py to finish before shutting down

PID=$(ps aux | grep "[C]old-air-funnel.py" | awk '{print $2}')

echo "$(date) Waiting for $PID to die before shutdown." > ice.log
echo "$(ps aux | grep [m]ysql)" >> ice.log

while [[ -n $(ps aux | grep "[C]old-air-funnel.py" | awk '{print $2}') ]]
do
#	sleep 3
#	echo $PID
	true
done
echo "$PID died....." >> ice.log
echo "$(date) System is now halting" >> ice.log
halt
