#Dockerfile for authentication.io

FROM ubuntu:14.04

# Maintainer: V. David Zvenyach <dave at esq io> (@vzvenyach)
MAINTAINER V. David Zvenyach, dave@esq.io

# Initialize
RUN mkdir /home/user-data
RUN apt-get update
RUN apt-get install -y gnupg2
RUN apt-get install -y python
RUN apt-get install -y python-pip
RUN apt-get install -y python-dev
RUN apt-get install -y git
RUN cd /home/user-data/; git clone https://github.com/unitedstates/authentication.git odi-authentication
RUN cd /home/user-data/odi-authentication; pip install -r requirements.txt

EXPOSE 8000
