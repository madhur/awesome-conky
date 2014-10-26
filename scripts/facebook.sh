#!/bin/bash

msgcount=$(fbcmd NOTIFY | grep MESSAGES_UNREAD | grep -oE "[[:digit:]]{1,}")
notifycount=$(fbcmd NOTICES unread | grep -c :title)
friendcount=$(fbcmd NOTIFY | grep FRIEND_REQUESTS | grep -oE "[[:digit:]]{1,}")
currenttime=$(date +%I:%M)

if [[ "$msgcount" -eq "0" ]] && [[ "$notifycount" -eq "0" ]] && [[ "$friendcount" -eq "0" ]]
then
	
	echo '${color}No new updates ${alignr}Updated: ${color white}'$currenttime
else
	echo '${color white}'$msgcount'${color aaaaaa} NEW MESSAGE(S) ${alignr}Updated: ${color white}'$currenttime
	echo '${color white}'$notifycount'${color aaaaaa} NEW NOTIFICATION(S)'
	echo '${color white}'$friendcount'${color aaaaaa} NEW Friend Request(s)'

fi	
