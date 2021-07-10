#!/bin/bash
#bash frontend-entrypoint.sh

KEYFILE=/opt/nginx/certs/key.key
CRTFILE=/opt/nginx/certs/cert.crt

if [[ ! -f "$KEYFILE" ]]; then
        echo "$KEYFILE does not exist. Starting nginx without ssl"
        rm /etc/nginx/conf.d/ssl_*.conf
elif [[ ! -f "$CRTFILE" ]]; then
        echo "$CRTFILE does not exist. Starting nginx without ssl"
        rm /etc/nginx/conf.d/ssl_*.conf
else
        echo "$KEYFILE & $CRTFILE do exist. Starting nginx with ssl"
fi

envsubst '$SERVER_NAME' < /etc/nginx/conf.d/reverse_80.nginx.template > /etc/nginx/conf.d/reverse_80.nginx

nginx -g "daemon off;"
