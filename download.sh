#!/usr/bin/env bash

for arg; do
	nohup bash -c "python main.py $arg" &
done
