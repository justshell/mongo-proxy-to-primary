FROM python:3.8.3-alpine3.11

RUN set -eux \
  ; pip3 install --quiet --no-cache-dir --disable-pip-version-check \
        pymongo==3.10.1 \
        dnspython==1.16.0

COPY mongo_proxy_to_primary.py /opt/mongo_proxy_to_primary.py
