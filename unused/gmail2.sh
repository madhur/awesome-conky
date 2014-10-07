#!/bin/bash

wget -q -O - https://mail.google.com/a/gmail.com/feed/atom --http-user=${1}@gmail.com --http-password="${2}" --no-check-certificate | grep fullcount | sed 's/<[^0-9]*>//g'