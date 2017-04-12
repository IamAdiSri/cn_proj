#!/usr/bin/python

##########################
# PROXY SERVER
# Last Modified: 12th April, 2017
##########################

import os
import re
import socket
import sys
import threading
import time
# import requests

def request_handler(conn, addr):
    client_req = conn.recv(1024)
    # print client_req

    req = client_req.split("\r\n")
    url = req[0].split(" ")[1]

    host = req[1].split(":")[1][1:]
    if len(req[1].split(":")) < 3:
        port = 80
    else:
        port = int(req[1].split(":")[2])

    # headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.102 Safari/537.36'}
    # r = requests.post(url)
    # print r

    print "??? Opening socket to end server at", host+":"+str(port)
    sock = socket.socket()
    sock.connect((host, port))

    print "??? Forwarding request on behalf of client to origin server at", url
    
    if host == "localhost" or host == "127.0.0.1":
        print "??? Origin server is located locally"

        method = req[0].split(" ")[0]
        
        http_pos = url.find("://")
        if http_pos != -1:
            url = url[(http_pos + 3):]
        
        file_pos = url.find("/")
        url = url[file_pos:]

        http_ver = req[0].split(" ")[2]

        req[0] = "%s %s %s" % (method, url, http_ver)

        new_req = ""
        for l in req:
            new_req += (l + "\r\n")

#         new_req = """GET /2.data HTTP/1.1
# Host: localhost:20101
# User-Agent: Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:52.0) Gecko/20100101 Firefox/52.0
# Accept: text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8
# Accept-Language: en-US,en;q=0.5
# Accept-Encoding: gzip, deflate
# Connection: keep-alive
# Upgrade-Insecure-Requests: 1


# """

        print new_req
        sock.send(new_req)

    else:
        print "??? Origin server is located externally"

        print client_req
        sock.send(client_req)
        
    print "??? Recieving response from origin server"
    response = sock.recv(1024)
    print response

    print "??? Forwarding response to client"
    conn.send(response)

    print "??? Recieving data from origin server and forwarding to client"
    while True:
        data = sock.recv(1024)
        conn.send(data)
        if not data:
            break
    print "??? Client request fulfilled"

    # conn.send("<html>\n\nSending this from the proxy server to" + str(addr) + "!!!\n\n</html>\r\n")
    print "??? Closing connection to client"
    conn.close()

    print "??? Exiting thread"
    print "??? --------------------------------------------------\n\n"
    exit()

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print "Usage: proxy.py <PORT_NUMBER>"
        exit()
    
    port = int(sys.argv[1])
    
    host = ""
    sock = socket.socket()
    sock.bind((host, port))
    sock.listen(5)

    while (1):
        conn, addr = sock.accept()
        print ">>> Connection accepted", addr

        global must_quit
        must_quit = threading.Event()
        threading.Timer(0, request_handler, [conn, addr]).start()

        print ">>> thread_initialised"
