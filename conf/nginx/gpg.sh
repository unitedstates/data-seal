#!/bin/bash

#echo "Enter Site Name: "
read SITENAME

#echo "Enter Email Address: "
read EMAIL

printf "GNUPG_IDENTITY_DEFAULTS = {\n   \
    # This is displayed on the key; make it something that identifies this website. \n\
    'name_real': '$SITENAME',   \n \
    # Make this a real address that will never change. ('support@example.com', etc) \n\
    'name_email': '$EMAIL',   \n\
    # Don't edit this (it is set as GNUPG_PASSPHRASE, above). \n  \
    'passphrase': GNUPG_PASSPHRASE  \n\
}\n"