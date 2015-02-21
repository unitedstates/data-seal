#!/bin/bash

./authentication/manage.py gpginit >> authentication/local_settings.py
gpg --armor --homedir authentication/gpgdata --export $EMAIL_ADDRESS > authentication/gpgdata/pubkey.asc
ln -s /authentication/authentication/gpgdata/pubkey.asc /authentication/authentication/authentication/authapp/static/authentication/pubkey.asc