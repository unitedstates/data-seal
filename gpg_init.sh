#!/bin/bash

gpg-init./authentication/manage.py gpginit >> authentication/local_settings.py
gpg --armor --homedir authentication/gpgdata --export $EMAIL_ADDRESS > authentication/gpgdata/pubkey.asc
ln -s authentication/gpgdata/pubkey.asc authentication/authentication/authapp/static/authentication/pubkey.asc 

# RUN ./authentication/manage.py syncdb