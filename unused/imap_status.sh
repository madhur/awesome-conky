#!/bin/bash

# imap_status.sh by drphibes 
#
# Script to query dovecot's PREAUTH imap binary for maildir status with an imap STATUS command.
# RFC3501 defines the following valid status items:
#
#     MESSAGES
#        The number of messages in the mailbox.
#
#     RECENT
#        The number of messages with the \Recent flag set.
#
#     UIDNEXT
#        The next unique identifier value of the mailbox.  Refer to
#        section 2.3.1.1 for more information.
#
#     UIDVALIDITY
#        The unique identifier validity value of the mailbox.  Refer to
#        section 2.3.1.1 for more information.
#
#     UNSEEN
#        The number of messages which do not have the \Seen flag set.
#
#
# Pump a STATUS command into the PREAUTH imap binary and parse for the return value.
#
# Examples: 
#
# ./imap_status.sh inbox UNSEEN
# ./imap_status.sh inbox MESSAGES
#

PREAUTH_SERVER="MAIL=maildir:~/.maildir /usr/libexec/dovecot/imap 2>&1"

if [ "$#" != "2" ]; then
    echo "usage: imap_status.sh <mailbox> <item>"
    exit 2
fi

echo "a1 status $1 ($2)" | eval $PREAUTH_SERVER | grep '^* STATUS' \
	| sed -e "s/\(.*\) ($2 \(.*\))/\2/" | tr -d '\015'
