#!/bin/bash

# Synchronize Raspberry Pi server time with master server
# This script should be run whenever an RPi reboots

cd sbhs_server/RPi_data

for ip in $(cat ipaddrs.txt) 
do
    echo $ip
    ssh pi@$ip "sudo date --set \"$(date)\""
done
