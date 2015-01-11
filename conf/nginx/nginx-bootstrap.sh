#!/bin/bash
# This is a script to automatically load the nginx configuration

add-apt-repository ppa:nginx/stable
apt-get update
apt-get -y install nginx

# Create local files from the `conf` directory
cp conf/local.conf /etc/nginx/conf.d/local.conf
mkdir /etc/nginx/ssl
cp conf/ssl.rules /etc/nginx/ssl/ssl.rules
cp conf/nginx.conf /etc/nginx/nginx.conf

# Generate Diffie-Hellman Parameter key
openssl dhparam -outform pem -out /etc/nginx/ssl/dhparam2048.pem 2048

echo "Your server name, please?"
read SERVER_NAME

# This adds the allowed host in Djangom which is required in Production
# (even though it's served through a reverse proxy, so I'm not sure it matters)
IP_ADDRESS="$(ip addr | egrep -o -m 1 'inet addr:[0-9|.]+' | egrep -o '[0-9|.]+')"
sed -i "s/ALLOWED_HOSTS \= \[\]/ALLOWED_HOSTS \= \[$SERVER_NAME, $IP_ADDRESS\]" authentication/settings.py

# Update the nginx configuration to include server name
sed -i "s/SERVER_NAME/$SERVER_NAME" /etc/nginx/conf.d/local.conf