#!/bin/bash

cd sbhs_server 

mkdir -p RPi_data
mkdir -p RPi_data/map RPi_data/report

# Get map_machine_ids.txt and server reports from all connected Raspberry Pi's
while read -r ip
do
    echo $ip
    curl -o RPi_data/map/$ip.txt $ip/map_machine_ids.txt
    curl -o RPi_data/report/$ip.txt $ip/report.json
    rsync -arz --exclude="django_error.log" -e "ssh -o StrictHostKeyChecking=no -o UserKnownHostsFile=/dev/null" --progress pi@$ip:/home/pi/sbhs-pi/log/ /home/vlabs-sbhs/code/sbhs/log/
    rsync -arz --remove-source-files -e "ssh -o StrictHostKeyChecking=no -o UserKnownHostsFile=/dev/null" --progress pi@$ip:/home/pi/sbhs-pi/experiments/ /home/vlabs-sbhs/code/sbhs/experiments/
done < "RPi_data/ipaddrs.txt"

# Execute script to create IP map
python create_ip_map.py

