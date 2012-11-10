#!/usr/bin/sh

PATH=/volume1/share

nohup python md5auto.py --test --path $PATH --log ./logs/log.txt ./md5s/*.md5
