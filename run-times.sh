#!/bin/bash

for day in Day-* ; do
	
	(cd $day; 
		prog=$(ls -1 *.py);
		echo "Running ${day} [${prog}] input.txt"
		time python ./${prog} input.txt
	)

done