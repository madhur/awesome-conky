#!/bin/sh
#curl -u ahuja.madhur:cmu@word10 --silent "https://mail.google.com/mail/feed/atom/unread" | tr -d '\n' | awk -F '<entry>' '{for (i=2; i<=NF; i++) {print $i}}' | sed -n "s/<title>\(.*\)<\/title.*name>\(.*\)<\/name>.*/\${color1}\2 \${goto 160} \${color2}\1/p"
curl -u ahuja.madhur:cmu@word10 --silent "https://mail.google.com/mail/feed/atom/unread" | tr -d '\n' | awk -F '<entry>' '{for (i=2; i<=NF; i++) {print $i}}' | sed -n "s/<title>\(.*\)<\/title.*name>\(.*\)<\/name>.*/\${color1}\2 \${goto 160} \${color2}\1/p"

notify-send "Gmail Updated"