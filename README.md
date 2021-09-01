# Mongo Proxy To Primary

Server that proxies all requests to primary member in the MongoDB replica set.

## Building and running

Repository includes Dockerfile to build. Release builds are available on [dockerhub](https://hub.docker.com/r/agisoft/mongo-proxy).

### How it works

The proxy gets MongoDB replica set members addresses and ports from DNS SRV records, than executes isMaster() on every member and connects to member that returns True on isMaster().

### Usage

The proxy can be used by developers or DBA to connect to primary replica set member for write operations, for example, via kubectl port-forward or via ingress-controller

### Command Line Options

	-p 		    Port to listen on. Defaults to 9211.
    -n 		    DNS name of MongoDB servers replica set. Required.
