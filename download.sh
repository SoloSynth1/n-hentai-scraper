#!/usr/bin/env bash

for arg; do
  nohup python main.py $arg &;
done