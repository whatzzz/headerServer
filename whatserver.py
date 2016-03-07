#!/usr/bin/env python
# coding=utf-8
# code by 92ez.com

import threading
import requests
import Queue
import sys
import re

#ip to num
def ip2num(ip):
    ip = [int(x) for x in ip.split('.')]
    return ip[0] << 24 | ip[1] << 16 | ip[2] << 8 | ip[3]

#num to ip
def num2ip(num):
    return '%s.%s.%s.%s' % ((num & 0xff000000) >> 24,(num & 0x00ff0000) >> 16,(num & 0x0000ff00) >> 8,num & 0x000000ff)

#
def ip_range(start, end):
    return [num2ip(num) for num in range(ip2num(start), ip2num(end) + 1) if num & 0xff]

#
def bThread(iplist):
    
    threadl = []
    queue = Queue.Queue()
    for host in iplist:
        queue.put(host)

    for x in xrange(0, int(SETTHREAD)):
        threadl.append(tThread(queue))
        
    for t in threadl:
        t.start()
    for t in threadl:
        t.join()        

#create thread
class tThread(threading.Thread):
    def __init__(self, queue):
        threading.Thread.__init__(self)
        self.queue = queue

    def run(self):
        
        while not self.queue.empty(): 
            host = self.queue.get()
            try:
                checkServer(host)
            except:
                continue

def checkServer(host):

    ports = [80,81,82,83,84,85,86,87,88,89,90,8080,8081,8082,8083,8084,8085,8086,8087,8088,8089,8090]

    for k in ports:
        try:
            aimurl = "http://"+host+":"+str(k)

            response = requests.get(url=aimurl,timeout=5)
            serverText = response.headers['server']
            titleText = re.findall(r'<title>(.*?)</title>',response.text)[0] 

            if len(serverText) > 0:
                print  "-"*50+"\n"+aimurl +"\nServer: "+serverText +"\nTitle: "+titleText

        except:
            pass


if __name__ == '__main__':
    print '\n############# HTTP Server Show  #############'
    print '                Author 92ez.com'
    print '################################################\n'

    global SETTHREAD

    try:
        SETTHREAD = sys.argv[2]

        iplist = ip_range(sys.argv[1].split('-')[0], sys.argv[1].split('-')[1])
        
        print '\n[Note] Will scan '+str(len(iplist))+" host...\n"

        bThread(iplist)
    except KeyboardInterrupt:
        print 'Keyboard Interrupt!'
        sys.exit()
