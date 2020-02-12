#!/usr/bin/env bash

for arg; do
	echo $arg;
	screen -dmL python main.py $arg ;
done
