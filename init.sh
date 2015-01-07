#!/bin/bash
sudo apt-get update
sudo apt-get install -y gnupg2
sudo apt-get install -y python
sudo apt-get install -y python-pip
sudo apt-get install -y python-dev
sudo apt-get install -y git
sudo apt-get install -y haveged
sudo apt-get install -y nano
sudo apt-get install -y postgresql postgresql-contrib
sudo apt-get install -y python-psycopg2
sudo apt-get install -y libpq-dev
git clone https://github.com/unitedstates/authentication.git
git checkout origin dc
cd authentication
sudo pip install -r requirements.txt
cd authentication
cp local_settings.py.example local_settings.py
echo '"GNUPG_BINARY = "/usr/local/opt/gnupg2/bin/gpg2"  # for *nix"' >> local_settings.py
./manage.py gpginit
./manage.py make_secret_key >> local_settings.py 
