# Generate the Keys
# openssl genrsa -aes256 -out /etc/nginx/ssl/keys/private.key 2048
openssl genpkey -algorithm RSA -aes256 -out /etc/nginx/ssl/keys/private.key -pkeyopt rsa_keygen_bits:2048
# Note, this will ask you for your password twice.

openssl rsa -in /etc/nginx/ssl/keys/private.key -out /etc/nginx/ssl/keys/private-decrypted.key
# Note, this will ask for the password, too.

openssl req -new -sha256 -key /etc/nginx/ssl/keys/private-decrypted.key -out /etc/nginx/ssl/keys/$SERVER_NAME.csr
# Note, this will ask for...
# Country Name (2 letter code) [AU]:
# State or Province Name (full name) [Some-State]:
# Locality Name (eg, city) []:
# Organization Name (eg, company) [Internet Widgits Pty Ltd]:
# Organizational Unit Name (eg, section) []:
# Common Name (e.g. server FQDN or YOUR name) []:
# Email Address []:

# Please enter the following 'extra' attributes
# to be sent with your certificate request
# A challenge password []:
# An optional company name []:

openssl x509 -req -days 365 -in /etc/nginx/ssl/keys/$SERVER_NAME.csr -signkey /etc/nginx/ssl/keys/private.key -out /etc/nginx/ssl/keys/server.crt
# Will ask for the private key password again

openssl dhparam -outform pem -out /etc/nginx/ssl/dhparam2048.pem 2048

# Do some cleanup. Only leave the crt and the encrypted private key
rm /etc/nginx/ssl/keys/private-decrypted.key
rm /etc/nginx/ssl/keys/$SERVER_NAME.csr