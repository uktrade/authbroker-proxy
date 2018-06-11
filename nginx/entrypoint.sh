#!/bin/bash

set -euo pipefail

# Validate environment variables
: "${APP_PROXY_TARGET:?Set APP_PROXY_TARGET using --env}"
: "${APP_PROXY_PORT:?Set APP_PROXY_PORT using --env}"
: "${ABC_PROXY_TARGET:?Set ABC_PROXY_TARGET using --env}"
: "${ABC_PROXY_PORT:?Set ABC_PROXY_PORT using --env}"
: "${DNS_RESOLVER:?Set DNS_RESOLVER using --env}"

APP_PROXY_PROTOCOL="${APP_PROXY_PROTOCOL:-http}"

echo ">> generating self signed cert"
openssl req -x509 -newkey rsa:4086 \
-subj "/C=XX/ST=XXXX/L=XXXX/O=XXXX/CN=localhost" \
-keyout "/key.pem" \
-out "/cert.pem" \
-days 3650 -nodes -sha256

envsubst '\$DNS_RESOLVER \$APP_PROXY_TARGET \$APP_PROXY_PORT \$ABC_PROXY_TARGET \$ABC_PROXY_PORT \$APP_PROXY_PROTOCOL' < /etc/nginx/conf.d/default.conf.template > /etc/nginx/conf.d/default.conf

echo ">> running nginx"

/usr/sbin/nginx -g "daemon off;"
