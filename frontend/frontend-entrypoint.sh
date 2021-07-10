#!/bin/bash
#bash frontend-entrypoint.sh
envsubst '$SERVER_NAME' < /etc/nginx/conf.d/static.nginx.template > /etc/nginx/conf.d/static.nginx
nginx -g "daemon off;"
