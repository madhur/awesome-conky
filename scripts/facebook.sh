#!/bin/bash

if [ "$1" = "message" ]
then
	msgcount=$(fbcmd NOTIFY | grep MESSAGES_UNREAD | grep -oE "[[:digit:]]{1,}")

	if [ "$msgcount" -eq "0" ]
	then
		echo No New Messages

	elif [ "$msgcount" -eq "1" ]
	then
		echo '${color white}'$msgcount'${color aaaaaa}' NEW MESSAGE
	else

		echo '${color white}'$msgcount'${color aaaaaa}' NEW MESSAGES
	fi

elif [ "$1" = "poke" ]
then
	pokecount=$(fbcmd NOTIFY | grep POKES | grep -oE "[[:digit:]]{1,}")

	if [ "$pokecount" -eq "0" ]
	then
		echo No One Has Poked You

	elif [ "$pokecount" -eq "1" ]
	then
		echo '${color white}'$pokecount'${color aaaaaa}' PERSON HAS POKED YOU
	else

		echo '${color white}'$pokecount'${color aaaaaa}' PEOPLE HAVE POKED YOU
	fi

elif [ "$1" = "notify" ]
then
	notifycount=$(fbcmd NOTICES unread | grep -c :title)

	if [ "$notifycount" -eq "0" ]
	then
		echo No New Notifications

	elif [ "$notifycount" -eq "1" ]
	then
		echo '${color white}'$notifycount'${color aaaaaa}' NEW NOTIFICATION
	else

		echo '${color white}'$notifycount'${color aaaaaa}' NEW NOTIFICATIONS
	fi

elif [ "$1" = "friend" ]
then
	friendcount=$(fbcmd NOTIFY | grep FRIEND_REQUESTS | grep -oE "[[:digit:]]{1,}")

	if [ "$friendcount" -eq "0" ]
	then
		echo No New Friend Requests

	elif [ "$friendcount" -eq "1" ]
	then
		echo '${color white}'$friendcount'${color aaaaaa}' NEW Friend Request
	else

		echo '${color white}'$friendcount'${color aaaaaa}' NEW Friend Requests
	fi

elif [ "$1" = "group" ]
then
	groupcount=$(fbcmd NOTICES unread | grep -c :title)

	if [ "$groupcount" -eq "0" ]
	then
		echo No New Group Invites

	elif [ "$groupcount" -eq "1" ]
	then
		echo '${color white}'$groupcount'${color aaaaaa}' NEW Group Invite
	else

		echo '${color white}'$groupcount'${color aaaaaa}' NEW Group Invites
	fi

elif [ "$1" = "events" ]
then
	eventscount=$(fbcmd NOTICES unread | grep -c :title)

	if [ "$eventscount" -eq "0" ]
	then
		echo No New Events

	elif [ "$eventscount" -eq "1" ]
	then
		echo '${color white}'$eventscount'${color aaaaaa}' NEW Event
	else

		echo '${color white}'$eventscount'${color aaaaaa}' NEW Events
	fi

else
	echo "Please state a command, [message,poke,notify,friend,group,events]"
fi