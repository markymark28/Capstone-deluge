#!/bin/sh
cd ../../..
python setup.py build
sudo python setup.py install
cd deluge
python deluge_login.py
