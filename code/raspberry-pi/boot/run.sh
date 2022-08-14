#!/bin/sh
sudo pigpiod # servo daemon
/usr/bin/python3 /home/pi/floating-navigation-sensor-assembly/code/raspberry-pi/NavUnit.py
