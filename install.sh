#!/bin/sh

sudo apt-get install python-pip python-dev python-scipy python-matplotlib python-wheel
sudo pip install -r requirements.txt
cp ocean.cron /etc/cron.d/ocean


