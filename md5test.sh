#!/usr/bin/sh

PATH=/volume1/share

nohup python md5auto.py --test --path $PATH --log ./logs/all.log ./md5s/*.md5
