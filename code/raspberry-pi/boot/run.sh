#!/bin/sh
pigpiod # servo daemon
/usr/bin/python3 /home/pi/chisel-bot-2/code/raspberry-pi/NavUnit.py
