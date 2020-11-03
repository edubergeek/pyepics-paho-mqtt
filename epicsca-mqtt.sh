#!/bin/bash

# this script is intended to be run by cron every 5 minutes
source /epics/startup/unix.sh
export PYEPICS_LIBCA=/epics/lib/linux-x86_64/libcas.so.3.15.8
export EPICS_CA_ADDR_LIST="10.10.10.11"
export PATH=$PATH:/epics/bin/linux-x86_64

cd ~/pyepics-paho-mqtt
nohup python3 ./weather.py >ca.log 2>&1 &
