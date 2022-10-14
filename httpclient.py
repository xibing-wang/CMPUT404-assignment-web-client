#!/usr/bin/env python3
# coding: utf-8
# Copyright 2016 Abram Hindle, https://github.com/tywtyw2002, and https://github.com/treedust
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

# Do not use urllib's HTTP GET and POST mechanisms.
# Write your own HTTP GET and POST
# The point is to understand what you have to send and get experience with it

import sys
import socket
import re
# you may use urllib to encode data appropriately
import urllib.parse


def help():
    print("httpclient.py [GET/POST] [URL]\n")


class HTTPResponse(object):
    def __init__(self, code=200, body=""):
        self.code = code
        self.body = body


class HTTPClient(object):
    # def get_host_port(self,url):

    def connect(self, host, port):
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket.connect((host, port))
        return None

    def get_code(self, data):
        print("this is data\n", data)
        header = data.split("\r\n")
        list1 = header[0].split()
        print("code", header)
        try:
            return int(list1[1])
        except:
            return 404

    def get_headers(self, data):
        return data.split("\r\n\r\n")[0]

    def get_body(self, data):
        return data.split("\r\n\r\n")[1]

    def sendall(self, data):
        self.socket.sendall(data.encode('utf-8'))

    def close(self):
        self.socket.close()

    # read everything from the socket
    def recvall(self, sock):
        buffer = bytearray()
        done = False
        while not done:
            part = sock.recv(1024)
            if (part):
                buffer.extend(part)
            else:
                done = not part
        return buffer.decode('utf-8')

    def GET(self, url, args=None):
        code = 500
        body = ""
        u = urllib.parse.urlparse(url)
        scheme = u.scheme
        port = u.port
        if scheme == "http" and port == None:
            port = 80
        if scheme == "https" and port == None:
            port = 443
        if u.path == "":
            req = "GET / HTTP/1.1\r\n"
        else:
            req = "GET " + u.path + " HTTP/1.1\r\n"
        req += "HOST: " + u.hostname + "\r\n"
        req += "Accept: */*\r\n"
        req += "Connection: close\r\n\r\n"

        self.connect(u.hostname, port)
        self.sendall(req)
        response = self.recvall(self.socket)
        self.close()
        code = self.get_code(response)
        body = self.get_body(response)

        return HTTPResponse(code, body)

    def POST(self, url, args=None):
        code = 500
        body = ""
        u = urllib.parse.urlparse(url)
        scheme = u.scheme
        port = u.port
        if scheme == "http" and port == None:
            port = 80
        if scheme == "https" and port == None:
            port = 443
        if u.path == "":
            req = "POST / HTTP/1.1\r\n"
        else:
            req = "POST " + u.path + " HTTP/1.1\r\n"
        req += "HOST: " + u.hostname + "\r\n"
        req += "Content-Type: application/x-www-form-urlencoded\r\n"

        if args == None:
            body = ""
        else:
            body += urllib.parse.urlencode(args)

        req += "Content-Length: " + str(len(body)) + "\r\n"
        req += "Accept: */*\r\n"
        req += "Connection: close\r\n\r\n"
        if args == None:
            req += ""
        else:
            req += urllib.parse.urlencode(args)

        self.connect(u.hostname, port)
        self.sendall(req)
        response = self.recvall(self.socket)
        self.close()
        code = self.get_code(response)
        body = self.get_body(response)

        return HTTPResponse(code, body)

    def command(self, url, command="GET", args=None):
        if (command == "POST"):
            return self.POST(url, args)
        else:
            return self.GET(url, args)


if __name__ == "__main__":
    client = HTTPClient()
    command = "GET"

    if (len(sys.argv) <= 1):
        help()
        sys.exit(1)
    elif (len(sys.argv) == 3):
        print(client.command(sys.argv[2], sys.argv[1]))
    else:
        print(client.command(sys.argv[1]))
