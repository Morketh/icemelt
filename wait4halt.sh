#!/bin/bash
PID=$(ps aux | grep [m]ysql | awk '{print $2}')

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
