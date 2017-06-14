#!/bin/bash

mkdir -p temp
nmap -n -sP 10.42.0.255/24 | grep -E -o "(([0-9]|[1-9][0-9]|1[0-9]{2}|2[0-4][0-9]|25[0-5])\.){3}([0-9]|[1-9][0-9]|1[0-9]{2}|2[0-4][0-9]|25[0-5])" | grep -v "10.42.0.1" > temp/ipaddrs.txt

while read -r ip
do
	curl -o temp/$ip.txt $ip/map_machine_ids.txt
done < "temp/ipaddrs.txt"

python create_ip_map.py