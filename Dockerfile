FROM python:3.8.12-alpine3.13

COPY --chown=0:0 docker-entrypoint.sh /usr/bin/docker-entrypoint

RUN set -eux \
  ; chmod 0755 /usr/bin/docker-entrypoint \
  ; mkdir -p /tmp/pip \
  ; pip3 install --quiet --cache-dir /tmp/pip --disable-pip-version-check \
        pymongo==3.12.0 \
        dnspython==2.1.0 \
  ; rm -rf /tmp/pip

COPY mongo_proxy_to_primary.py /opt/mongo_proxy_to_primary.py

ENTRYPOINT [ "/usr/bin/docker-entrypoint" ]
