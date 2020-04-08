FROM python:3.8.0-alpine3.10

RUN pip3 install pymongo==3.9.0

COPY mongo_proxy_to_primary.py /opt/mongo_proxy_to_primary.py
