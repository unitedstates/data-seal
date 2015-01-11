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
git checkout origin dc
cd authentication
sudo pip install -r requirements.txt
cd authentication
cp local_settings.py.example local_settings.py

printf 'GNUPG_BINARY = "/usr/local/opt/gnupg2/bin/gpg2"  # for *nix"\n' >> authentication/local_settings.py
./authentication/manage.py make_secret_key >> authentication/local_settings.py 
echo "Enter FQDN:"
read FQDN
echo "Enter Email Address:"
read EMAIL_ADDRESS
printf "$FQDN\n$EMAIL_ADDRESS" | ./conf/nginx/gpg.sh >> authentication/local_settings.py
./authentication/manage.py gpginit >> authentication/local_settings.py
gpg --armor --homedir gpgdata --export $EMAIL_ADDRESS > gpgdata/pubkey.asc
ln -s gpgdata/pubkey.asc authentication/authentication/authapp/static/pubkey.asc 
# ./manage syncdb
# Will get prompted to make a superuser
# ./conf/nginx/bootstrap.sh
# gunicorn authentication.wsgi:application -b 0.0.0.0:5000 --log-file /var/log/gunicorn.log --pid /tmp/gunicorn.pid --daemon