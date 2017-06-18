#!/bin/bash

cd sbhs_server 

mkdir -p RPi_data
mkdir -p RPi_data/map RPi_data/report

# get IP addresses of connected Raspberry Pi's
nmap -n -sP 10.42.0.255/24 | grep -E -o "(([0-9]|[1-9][0-9]|1[0-9]{2}|2[0-4][0-9]|25[0-5])\.){3}([0-9]|[1-9][0-9]|1[0-9]{2}|2[0-4][0-9]|25[0-5])" | grep -v "10.42.0.1" > RPi_data/ipaddrs.txt

# Get map_machine_ids.txt and server reports from all connected Raspberry Pi's
while read -r ip
do
	curl -o RPi_data/map/$ip.txt $ip/map_machine_ids.txt
	curl -o RPi_data/report/$ip.txt $ip/report.json
done < "RPi_data/ipaddrs.txt"

# Execute script to create IP map
python create_ip_map.py