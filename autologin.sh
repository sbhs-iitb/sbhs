#!/bin/bash
rm notworking.txt working.txt
for each in {1..32};
	do
		login=$(echo "username=suser$each&password=suser"$each"4229")
		output=$(curl --silent --data $login http://vlabs.iitb.ac.in/sbhs/experiment/initiate/) && \
		chars=$(echo -n $output | wc -c) &&\
		if [ "$chars" -lt 100 ]; 
		then 
			echo  suser$each     $output; 
			echo suser$each >> working.txt
		else
			echo "ERROR 500";
			echo suser$each >> notworking.txt
fi
		sleep 0.2 && echo ;
	done
