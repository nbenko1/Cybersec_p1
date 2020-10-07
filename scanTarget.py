# Nicholai Benko
# Cybersecurity Project 1
# 10/7/20


import argparse
from socket import *
from threading import *

semLock = Semaphore(value = 1)

def connScan(tgtHost, tgtPort):
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.settimeout(5)
        s.connect(tgtHost, tgtPort)
        s.send('root\r\n')
        data = s.recv(4096)
        semLock.acquire()
        print("port %d is open on target", tgtPort)
        print(data)
    except:
        semLock.acquire()
        print("port %d is filtered or closed", tgtPort)
    finally:
        semLock.release()
        s.close()

def portScan(tgtHost, tgtPorts):
    try:
        tgtIP = gethostbyname(tgtHost)
        print(tgtIP)
    except: 
        print("[-] Cannot resolve %s: Unknown Host", tgtHost)
        return

    for tgtPort in tgtPorts:
        t = Thread(target="connScan", args=(tgtHost,tgtPort))
        t.start()

    #set timeout

def main():
    parser = argparse.Argument()
    parser.add_argument('-H', dest='tgtHost', require=True, help='specify target host')
    parser.add_argument('-p', dest='tgtPorts', default='21, 22, 23, 25, 80, 443', help='specify target port(s)')
     
    args = parser.parse_args()
    tgtHost = args.tgtHost
    tgtPorts = str(args.tgtPorts).split(', ')

    portScan(tgtHost, tgtPorts)

if __name__ == "__main__":
    main()