# Mongo Proxy To Primary

Server that proxies all requests to primary member in the MongoDB replica set.

## Building and running

Repository includes simple Dockerfile to build

### Usage

The server can be used by developers or DBA to connect to primary replica set member for write operations via kubectl port-forward or via ingress-controller

### Command Line Options

	-p 		    Port to listen on. Defaults to 9211.
	-s 		    Mongo service name in kubernetes. Required.
    -n 		    Kubernetes namespace where mongo is installed. Defaults to "default".