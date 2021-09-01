#!/bin/sh

if [ $# -gt 0 ]; then
    if [ "$1" = "-p" ] || [ "$1" = "-n" ]; then
        exec python3 /opt/mongo_proxy_to_primary.py "$@"
    else
        exec "$@"
    fi
else
    echo "Usage: -p <port> -n <server>" >&2
    echo "More info: https://github.com/AgisoftCloud/mongo-proxy-to-primary" >&2
    exit 1
fi
