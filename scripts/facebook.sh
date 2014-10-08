#!/bin/bash

msgcount=$(fbcmd NOTIFY | grep MESSAGES_UNREAD | grep -oE "[[:digit:]]{1,}")
notifycount=$(fbcmd NOTICES unread | grep -c :title)
friendcount=$(fbcmd NOTIFY | grep FRIEND_REQUESTS | grep -oE "[[:digit:]]{1,}")
currenttime=$(date +%H:%M)

if [[ "$msgcount" -eq "0" ]] && [[ "$notifycount" -eq "0" ]] && [[ "$friendcount" -eq "0" ]]
then
	
	echo '${color}No new updates ${alignr}Last Check: ${color white}'$currenttime
else
	echo '${color white}'$msgcount'${color aaaaaa} NEW MESSAGE(S) Last Check: ${color white}${alignr}'$currenttime
	echo '${color white}'$notifycount'${color aaaaaa} NEW NOTIFICATION(S)'
	echo '${color white}'$friendcount'${color aaaaaa} NEW Friend Request(s)'

fi	
