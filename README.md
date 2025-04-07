# Mongo Proxy To Primary

Project Forked from: https://github.com/Agisoft-Cloud/mongo-proxy-to-primary
Server that proxies all requests to primary member in the MongoDB replica set.

## Building and running

Origin Repository includes Dockerfile to build. Release builds are available on [dockerhub](https://hub.docker.com/r/agisoft/mongo-proxy).
Current Repository includes Dockerfile to build.

### How it works

DNS mode ('-n' option):
The proxy gets MongoDB replica set members addresses and ports from DNS SRV records, than executes isMaster() on every member and connects to member that returns True on isMaster().

Static RS mode ('-c' option):
The proxy gets MongoDB replica set members addresses and ports from string at startup, than executes isMaster() on every member and connects to member that returns True on isMaster().

### Usage

The proxy can be used by developers or DBA to connect to primary replica set member for write operations, for example, via kubectl port-forward or via ingress-controller

### Command Line Options

  -p 		    Port to listen on. Defaults to 9211.
  -n 		    DNS name of MongoDB servers replica set. Required if '-c' is undefined
  -c 		    MongoDB servers replica set servers string <hostname|ip>:<port>. Required if '-n' is undefined
            Example:
              -c 192.168.0.1:27017,192.168.0.2:27017,192.168.0.3:27017
