#! /usr/bin/env python3

# Echo client program
import socket, sys, re,os

sys.path.append("../lib")       # for params
import params

from framedSock import framedSend, framedReceive


inputFile = input("Please enter file name: ")

if(not os.path.isfile(inputFile)):
    print("No such file exist")
    exit()

switchesVarDefaults = (
    (('-s', '--server'), 'server', "127.0.0.1:50001"),
    (('-d', '--debug'), "debug", False), # boolean (set if present)
    (('-?', '--usage'), "usage", False), # boolean (set if present)
    )

progname = "framedClient"
paramMap = params.parseParams(switchesVarDefaults)

server, usage, debug  = paramMap["server"], paramMap["usage"], paramMap["debug"]

if usage:
    params.usage()


try:
    serverHost, serverPort = re.split(":", server)
    serverPort = int(serverPort)
except:
    print("Can't parse server:port from '%s'" % server)
    sys.exit(1)

s = None
for res in socket.getaddrinfo(serverHost, serverPort, socket.AF_UNSPEC, socket.SOCK_STREAM):
    af, socktype, proto, canonname, sa = res
    try:
        print("creating sock: af=%d, type=%d, proto=%d" % (af, socktype, proto))
        s = socket.socket(af, socktype, proto)
    except socket.error as msg:
        print(" error: %s" % msg)
        s = None
        continue
    try:
        print(" attempting to connect to %s" % repr(sa))
        s.connect(sa)
    except socket.error as msg:
        print(" error: %s" % msg)
        s.close()
        s = None
        continue
    break

if s is None:
    print('could not open socket')
    sys.exit(1)



framedSend(s,inputFile.encode(), debug)

if(framedReceive(s,debug).decode() == "Ready"):
    sentFile = open(inputFile, "r")
    data = sentFile.read(100)
    while(data):
        framedSend(s,data.encode(),debug)
        data = sentFile.read(100)
    framedSend(s,b"exit",debug)
else:
    print("File already exist in server")
    exit()
    

print("received:", framedReceive(s, debug))

