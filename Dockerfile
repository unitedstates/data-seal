#Dockerfile for authentication.io

FROM ubuntu:14.04

# Maintainer: V. David Zvenyach <dave at esq io> (@vzvenyach)
MAINTAINER V. David Zvenyach, dave@esq.io

# Initialize
RUN apt-get update && apt-get install -y gnupg2 \
	python \ 
	python-pip \
	python-dev \
	git \
	haveged \ 
	nano \
	postgresql postgresql-contrib \
	python-psycopg2 \
	libpq-dev \
	libxml2-dev libxslt1-dev \
	libncurses5-dev

RUN git clone https://github.com/unitedstates/authentication.git
WORKDIR authentication

RUN pip install -r requirements.txt

RUN mv authentication/local_settings.py.example authentication/local_settings.py
RUN printf '\nGNUPG_BINARY = "/usr/local/opt/gnupg2/bin/gpg2"  # for *nix"\n' >> authentication/local_settings.py
RUN ./authentication/manage.py make_secret_key >> authentication/local_settings.py

ENV FQDN authentication.dccode.gov
ENV EMAIL_ADDRESS administrator@dccode.gov

RUN printf "$FQDN\n$EMAIL_ADDRESS" | ./conf/nginx/gpg.sh >> authentication/local_settings.py

# ENTRYPOINT ["./gpg_init.sh"]
# RUN ./authentication/manage.py syncdb
# RUN cd authentication && gunicorn authentication.wsgi:application -b 0.0.0.0:5000 --log-file /var/log/gunicorn.log
# sudo docker run -ti -v /dev/urandom:/dev/random -P --name auth authentication /bin/bash

EXPOSE 5000