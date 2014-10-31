#!/bin/bash

##
## Simple script to enable WIFI monitor mode on multiple 
## channels at the same time
##
## Used for WIFI testing on our campus environment
##

date=`date +%Y-%m-%d-%H-%M-%S`

echo "Turning off interface"
ifconfig wlan1 down
ifconfig wlan2 down
ifconfig wlan3 down
ifconfig wlan4 down

echo "Setting Monitor Mode"
iwconfig wlan1 mode monitor
iwconfig wlan2 mode monitor
iwconfig wlan3 mode monitor
iwconfig wlan4 mode monitor

echo "Bringing up interface"
ifconfig wlan1 up
ifconfig wlan2 up
ifconfig wlan3 up
ifconfig wlan4 up

echo "Setting channels"
iwconfig wlan1 channel 6
iwconfig wlan2 channel 36
iwconfig wlan3 channel 11
iwconfig wlan4 channel 153

echo "Starting Captures in this local directory"
tcpdump -i wlan1 -n -s0 -w wlan1-$date.pcap &
tcpdump -i wlan2 -n -s0 -w wlan2-$date.pcap &
tcpdump -i wlan3 -n -s0 -w wlan3-$date.pcap &
tcpdump -i wlan4 -n -s0 -w wlan4-$date.pcap &

echo "*********************************"
echo "*********************************"
echo "*********************************"
echo "*********************************"
echo "When you are finished press ENTER"
echo "*********************************"
echo "*********************************"
echo "*********************************"
echo "*********************************"
echo "*********************************"
read

echo "Stopping tcpdump"
sudo pkill tcpdump

echo "!!!!!!"
echo "Opening captures in wireshark, press ENTER to continue or CTRL-C to quit"
echo "!!!!!!"
read
wireshark wlan1-$date.pcap &
wireshark wlan2-$date.pcap &
wireshark wlan3-$date.pcap &
wireshark wlan4-$date.pcap &
