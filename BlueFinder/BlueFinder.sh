#!/bin/bash

# set for user input in terminal
sel=$1
BT_ADDR=$2

# set for a single device
HCI=hci0
#hciconfig $HCI down
#hciconfig $HCI up 

if [ "$sel" = "" ]
then
	echo -e "\n              BlueFinder v1.2 "
	echo -e "        ./BlueFinder.sh <sel> <BT_Addr>"
	echo -e "\n\n                DESCRIPTION"
        echo -e "	<sel>          C - Classic, B - Low-Energy"
	echo -e "	<BT_Addr>      Bluetooth Address\n"

elif [ "$sel" = 'C' ]; then
	echo -e "\nScanning..."
	while /bin/true
	do
	RTT=`l2ping -i $HCI -c 1 $BT_ADDR -f | grep time| awk '{print $8}'`;
		for ((i=0;i<=100;i++));
		do
		# Pull data from bluetooth device
		# echo "$RTT"
		RSSI[i]=`hcitool -i $HCI rssi $BT_ADDR | grep RSSI | awk '{print $4}'`;
		done
		# Call python script to calculate the distance using RSSI
		python rangefinder.py $sel "${RSSI[@]}"
	#echo "RSSI:"	
	#echo "${RSSI[@]}"
	done

elif [ "$sel" = 'B' ]; then
	echo -e "\nScanning..."
	
	while /bin/true
	do
		rm output.txt
		# Pull data from bluetooth device & kill after 5 secs
		hcitool -i $HCI lescan --duplicates >/dev/null & 
		hcidump -i $HCI > output.txt & sleep 2
		pkill --signal SIGINT hcitool
	
		# read bdaddr and RSSI
		bdaddr=(`grep -E "bdaddr.* " output.txt | awk '{print $2}'`)
		RSSI=(`grep -E "RSSI:.* " output.txt | cut -f2 -d ':'`)
	
		# set n = to length of bdaddr and loop
		n="${#bdaddr[@]}"
		for ((i=0;i<=n;i++));
		do
			# delete elements that dont equal BT_ADDR
			if [ "${bdaddr[i]}" != "$BT_ADDR" ]; then
			unset bdaddr[i]
			unset RSSI[i]
			fi
		done

		# Call python script to calculate the distance using RSSI
		python rangefinder.py $sel "${RSSI[@]}"
	done
else
	echo "Error"
fi



