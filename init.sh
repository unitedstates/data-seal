#!/bin/bash
sudo apt-get update
sudo apt-get install -y gnupg2
sudo apt-get install -y python
sudo apt-get install -y python-pip
sudo apt-get install -y python-dev
sudo apt-get install -y git
sudo apt-get install -y haveged
sudo apt-get install -y nano
cd /vagrant/
sudo pip install -r requirements.txt
