#!/usr/bin/expect -f
spawn telnet 192.168.1.1
expect -re "Login"
send "admin\n"
expect "Password:"
send "goldi25\n"
#interact
expect ">"
send "lan showhosts all\n"
#send "exit\n"