# Nicholai Benko
# Cybersecurity Project 1
# 10/7/20


import argparse
from socket import *
from threading import *

semLock = Semaphore()

def connScan(tgtHost, tgtPort):
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.settimeout(5)
        s.connect(tgtHost, tgtPort)
        s.send('root\r\n')
        data = s.recv(4096)
        semLock.acquire()
        print("port", tgtPort,  "is open on target")
        print(data)
        s.close()
    except:
        semLock.acquire()
        print("port", tgtPort,  "is filtered or closed")
    finally:
        semLock.release()
        

def portScan(tgtHost, tgtPorts):
    try:
        tgtIP = gethostbyname(tgtHost)
        print(tgtIP)
    except: 
        print("[-] Cannot resolve", tgtHost, ": Unknown Host")
        return

    for tgtPort in tgtPorts:
        t = Thread(target= connScan, args=(tgtHost, tgtPort))
        t.start()

    print("finished scan")

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('-H', dest='tgtHost', required=True, help='specify target host')
    parser.add_argument('-p', dest='tgtPorts', default='21, 22, 23, 25, 80, 443', help='specify target port(s)')
     
    args = parser.parse_args()
    tgtHost = args.tgtHost
    tgtPorts = str(args.tgtPorts).split(', ')

    portScan(tgtHost, tgtPorts)

if __name__ == "__main__":
    main()