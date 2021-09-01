FROM python:3.8.12-alpine3.13

RUN set -eux \
  ; mkdir -p /tmp/pip \
  ; pip3 install --quiet --cache-dir /tmp/pip --disable-pip-version-check \
        pymongo==3.12.0 \
        dnspython==2.1.0 \
  ; rm -rf /tmp/pip

COPY mongo_proxy_to_primary.py /opt/mongo_proxy_to_primary.py
