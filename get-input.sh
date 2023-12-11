#!/usr/bin/env bash

day=$(date |cut -d\  -f3)

if [ -f ../.cookies ]; then
	curl -sL -b .cookies https://adventofcode.com/2023/day/${day}/input > input_${day}.txt
else
	echo "You need a cookie file with your session cookie"
	cat <<- EOF
	adventofcode.com	TRUE	/	FALSE	0	session	SESSION-COOKIE
	EOF
fi	
