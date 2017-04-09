#!/usr/bin/python

##########################
# PROXY SERVER
# Last Modified: 
##########################

import os
import re
import socket
import sys
import threading
import time
import requests

###################
# SOCKET PARAMETERS
###################

s = socket.socket()
host = ""
adrs = "."

if __name__ == "__main__":
    global port
    port = int(sys.argv[1])

    s.bind((host, port))
    s.listen(5)

    global conn
    global addr
    conn, addr = s.accept()

    print "connection_accepted", addr

    print conn.recv(1024)
    print "done"

    conn.send("<html>\n\nSending this from the proxy server!!!\n\n</html>")
