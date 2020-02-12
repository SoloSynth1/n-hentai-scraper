#!/usr/bin/env bash

for arg; do
	screen -dm python main.py $arg ;
	sleep 1;
done
