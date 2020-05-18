#!/usr/bin/env python3

import socket
import select
import time
import os
import sys
import argparse
import logging
import dns.resolver
from pymongo import MongoClient, errors


class ParserWithHelp(argparse.ArgumentParser):
    def error(self, message):
        sys.stderr.write('error: %s\n' % message)
        self.print_help()
        sys.exit(1)


class MongoServers:
    def __init__(self, mongo_domain_name):
        self.mongo_domain_name = mongo_domain_name

    def get(self):
        mongo_servers_list = []

        try:
            get_srv_records = dns.resolver.query('_mongodb._tcp.' + self.mongo_domain_name, 'SRV')

            for srv in get_srv_records:
                mongo_server = {}
                mongo_server['address'] = str(srv.target).rstrip('.')
                mongo_server['port'] = srv.port

                if not mongo_server['address'] or not mongo_server['port']:
                    log.error("SRV record is incorrect")
                    sys.exit(1)

                mongo_servers_list.append(mongo_server)

            if not mongo_servers_list:
                log.error("No mongo servers were found")
                sys.exit(1)
            else:
                return mongo_servers_list
        except OSError as e:
            log.error(e)
            sys.exit(1)


class MongoGetPrimary:
    def __init__(self, mongo_servers_list: list):
        self.mongo_servers_list = mongo_servers_list

    def connect(self):
        mongo_connect_string = 'mongodb://'
        for item, server in enumerate(self.mongo_servers_list):
            if item:
                mongo_connect_string+=','
            mongo_connect_string+=str(server['address'] + ':' + str(server['port']))

        try:
            log.info("Connecting to mongo primary server")
            connect_to_mongo = MongoClient(mongo_connect_string)
            db_handler = connect_to_mongo["admin"]
            primary = db_handler.command('isMaster')['primary'].split(':')
            log.info("Connected to mongo primary server")
            return primary
        except errors.PyMongoError as e:
            log.error(e)
            sys.exit(1)


class Redirect:
    def __init__(self):
        self.redirect = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    def start(self, host, port):
        try:
            self.redirect.connect((host, port))
            return self.redirect
        except Exception as e:
            log.error(e)
            return False


class ProxyServerToMongo:
    input_list = []
    channel = {}

    def __init__(self, host, port, delay: float, buffer_size: int, mongo_domain_name):
        self.host = host
        self.port = port
        self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.server.bind((self.host, self.port))
        self.server.listen(200)
        self.delay = delay
        self.buffer_size = buffer_size
        self.mongo_domain_name = mongo_domain_name
        self.mongo_servers_list = MongoServers(self.mongo_domain_name)

    def start_server(self):
        self.input_list.append(self.server)
        log.info("Server started on " + str(self.host) + ":" + str(self.port))
        while True:
            time.sleep(self.delay)
            ss = select.select
            inputready, outputready, exceptready = ss(self.input_list, [], [])
            for self.s in inputready:
                if self.s == self.server:
                    self.on_accept()
                    break

                self.data = self.s.recv(self.buffer_size)
                if len(self.data) == 0:
                    self.on_close()
                    break
                else:
                    self.on_receive()

    def on_accept(self):
        mongo_servers_list = self.mongo_servers_list.get()
        redirect_to = MongoGetPrimary(mongo_servers_list).connect()
        redirect = Redirect().start(redirect_to[0], int(redirect_to[1]))
        clientsock, clientaddr = self.server.accept()
        if redirect:
            log.info(str(clientaddr[0]) + ":" + str(clientaddr[1]) + " has connected")
            self.input_list.append(clientsock)
            self.input_list.append(redirect)
            self.channel[clientsock] = redirect
            self.channel[redirect] = clientsock
        else:
            log.error("Can't establish connection with remote server.")
            log.error("Closing connection with client side - " + clientaddr)
            clientsock.close()

    def on_close(self):
        try:
            current_peer = self.s.getpeername()
            log.info(str(current_peer[0]) + ":" + str(current_peer[1]) + " has disconnected")
            self.delete_channels()  
        except:
            log.error("interrupt call")
            self.delete_channels()
            server.start_server()

    def delete_channels(self):
        self.input_list.remove(self.s)
        self.input_list.remove(self.channel[self.s])
        out = self.channel[self.s]
        self.channel[out].close()
        self.channel[self.s].close()
        del self.channel[out]
        del self.channel[self.s]

    def on_receive(self):
        data = self.data
        self.channel[self.s].send(data)

if __name__ == '__main__':
        log = logging.getLogger()
        log.setLevel(logging.INFO)
        handler = logging.StreamHandler(sys.stdout)
        handler.setLevel(logging.INFO)
        formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
        handler.setFormatter(formatter)
        log.addHandler(handler)

        parser = ParserWithHelp()
        parser.add_argument('-p', dest="port", help='Port to listen on', default=9211)
        parser.add_argument('-n', dest="domain_name", help='MongoDB cluster domain name', required=True)
        args = parser.parse_args()

        server_listen_ip = '0.0.0.0'
        server_listen_port = int(args.port)
        buffer_size = 4096
        delay = 0.0001
        mongo_domain_name = args.domain_name

        server = ProxyServerToMongo(server_listen_ip, server_listen_port, delay, buffer_size, mongo_domain_name)

        try:
            log.info("Starting server...")
            server.start_server()
        except OSError as e:
            log.error(e)
            sys.exit(1)
