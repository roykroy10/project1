# Welcome to Roy's project for PERCEPTO

MYPORT = 8021 # Defines the Port
ADDR = ('localhost',MYPORT) # Defines the address to broadcast/receive

import os, json, sys, time # Imports os to communicate with terminal, json to encode and decode, sys to exit and time for sleep function

from socket import *

def getTermAns(str): # This function gets a string to input to the terminal and returns the answer from the terminal
    p = os.popen(str)
    ans = p.readline()
    p.close()
    return ans

def getAllData(): # This function uses getTermAns to get the information needed and puts it in a string

    s = 'CPU: \n' + getTermAns("cat /proc/cpuinfo | grep 'model name' | uniq") # Get the CPU model name and add to a string

    s += getTermAns("cat /proc/cpuinfo | grep 'MHz' ") # Clock speed

    s += 'Number of cores: ' + getTermAns("cat /proc/cpuinfo | grep processor | wc -l") # Number of cores

    s += 'CPU load percentage: ' + getTermAns("top -d 0.5 -b -n2 | grep 'Cpu(s)'|tail -n 1 | awk '{print $2 + $4}' ") # CPU load percentage

    s += 'Total RAM Size: ' + getTermAns("cat /proc/meminfo | grep 'MemTotal' | awk '{print $2}' ") # Total RAM memory size

    s += 'Free RAM Percantage: ' + getTermAns("free | grep Mem | awk '{print 100-($3/$2 * 100.0)}'") # Calculates Free RAM percentage

    s += 'Uptime: ' + getTermAns("uptime | awk '{print $3}' ") # Gets Uptime

    s += 'Kernel Version: ' + getTermAns("uname -r ") # Gets the Kernel version

    s += getNetHW()

    return s

def getNetHW(): # This is the bonus function to get the network interfaces and MAC addresses
    p = os.popen("ifconfig | grep HWaddr ")  # Gets network interfaces
    netAns = 'Active network interfaces and their MAC addresses: \n'
    for line in p.readlines(): # Puts the answer in a string
        netAns += line
    p.close()
    return netAns

def myBroadcast(): # This function broadcasts
    sock = socket(AF_INET,SOCK_DGRAM)
    sock.bind(('',0))
    sock.setsockopt(SOL_SOCKET,SO_BROADCAST,1)
    try:
        while True:
            data = getAllData() # Gets the data to broadcast
            sock.sendto(json.dumps(data), ADDR) # Uses json to encode and broadcasting
            time.sleep(2) # Takes a couple of seconds between broadcasts
    except KeyboardInterrupt:
        sock.close()
        print(' Shutting down')
        sys.exit()
    return

def receiveBr(): # This function receives the data and prints it
    sock = socket(AF_INET, SOCK_DGRAM)
    sock.bind(ADDR)
    try:
        while True:
            data, adr = sock.recvfrom(1024) # Receives the data
            print "Received message: \n", json.loads(data) # Uses json to decode and prints

    except KeyboardInterrupt:
        sock.close()
        print(' Shutting down')
        sys.exit()
    return

print(
'Welcome to my Project \n'
'To Broadcast, enter "b"\n'
'To Receive, enter "r"''\n'
'To Print only, press "p" \n'
'Press any other key to exit ')

ans = raw_input("Please type your response now\n") # Gets an input from the user

if (ans == 'b'):
    print('Broadcasting... \n'
          'Press CTRL+C to stop')
    myBroadcast() # Calls the function to broadcast

elif (ans == 'r'):
    print('Receiving... \n'
          'Press CTRL+C to stop')
    receiveBr() # Calls the function to receive

elif (ans == 'p'):
    print getAllData()

else:
    sys.exit()
