# Nicholai Benko
# Cybersecurity Project 1
# 10/7/20


import argparse
#from socket import *
import socket
from threading import *

semLock = Semaphore() # defaults to value = 1

def connScan(tgtHost, tgtPort):
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM) # create socket
        s.settimeout(10) # set the socket timeout to 10 seconds
        s.connect((tgtHost, tgtPort)) # connect to the port on the subject computer
        # s.send('root\r\n') # send a data request
        # data = s.recv(4096) # safe the data that was returned
        semLock.acquire() # request the semaphore
        print "[+] port", tgtPort,  "is open on target" # print that that port is open
        #print(data) # print what was returned from the semaphore
        s.close() # close the connection
    except:
        semLock.acquire()
        print "[-] port", tgtPort,  "is filtered or closed" # if connectino was unsuccessful then print failure
    finally:
        semLock.release() # release the semaphore so other threads can print
        

def portScan(tgtHost, tgtPorts):
    try:
        tgtIP = socket.gethostbyname(tgtHost) # safe host IP
        print(tgtIP)
    except: 
        print "[-] Cannot resolve", tgtHost, ": Unknown Host" # if IP unavailable throw warning
        return

    for tgtPort in tgtPorts: # loop through each port
        port = int(tgtPort) # cast the port nunmber to an int
        t = Thread(target= connScan, args=(tgtHost, tgtPort)) # create a thread for each port
        t.start() # start the thread


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('-H', dest='tgtHost', required=True, help='specify target host') # parse first argument
    parser.add_argument('-p', dest='tgtPorts', default='21, 23, 25, 80, 443', help='specify target port(s)') # parse second argument
     
    args = parser.parse_args()
    tgtHost = args.tgtHost # create host variable
    tgtPorts = str(args.tgtPorts).split(', ') #create port variable

    portScan(tgtHost, tgtPorts) # call the methods

if __name__ == "__main__":
    main()