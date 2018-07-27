#!/usr/bin/env python3
import os
import time
import subprocess
#comment to be removed
date = time.strftime('%m%y')
tick = time.strftime('%d @ %T ')
start = time.strftime('%m/%d/%y %T')
# This makes it so it does not matter where you run the script from, it will
# always find the hosts.txt file inside the directory the script is located.
CURRENT_DIR = os.path.dirname(__file__)
working_dir = os.path.join(CURRENT_DIR + 'data/')


class colors:
    WARN = '\033[91m'
    END = '\033[0m'
    OK = '\033[36m'


def poll(host):
    """Ping the hosts in the host file"""
    # Create subprocess object for ping
    up = True
    p = subprocess.run('ping -c 1 -W 1 '
                       + str(host),
                       stdout=subprocess.PIPE,
                       shell=True)
    # Create object to store the text from the ping
    text = p.stdout.decode('utf-8')
    # Split ping response into separate lines for parsing
    line = text.split('\n')
    # Parses the lines from stdout to see if a ping failed or succeeded
    for item in line:
        if '0 packets received' in item:
            print(str(time.time()) + ' ' + str(host) + ' Failed Ping',
                  file=open(working_dir + time.strftime('%m%d@' + host)
                            + '.txt', 'a+'))
            up = False
        if 'time' in item:
            ms = item.split('time=', 1)[1]
            if float(ms.rstrip(' ms')) > 100:
                print(str(time.time()) + ' ' + str(host) + ' High(' + ms + ')',
                      file=open(working_dir + time.strftime('%m%d@'+host)
                                + '.txt', 'a+'))

    # Ping the host and return True if it is up
    return up


def init(entry):
    """Initialize host file with false count(for poll funct), and adds
    a place to store the ping in milliseconds to the file"""
    with open(CURRENT_DIR + 'hosts.txt', 'r') as f:
        for line in f:
            data = line.split()
            master.append({'host': data[0], 'label': data[1], 'count': 0, 'pms':0})


def ping_hosts():
    """Use poll function to ping the hosts and change values inside the host
       dictionary"""
    for entry in master:
        # If host is up set counter to zero
        if poll(entry['host']):
            # Write to file if host came back from down state and speak
            if entry['count'] / 2 > 5:
                upAlert = os.system('espeak ' + entry['label'] + '"is up"')
                print(tick + entry['host'].ljust(15) + ' Came Up',
                      file=open(CURRENT_DIR + date
                                + '.txt', 'a'))
                upAlert
            entry['count'] = 0
        # If host is down add to counter
        else:
            entry['count'] = entry['count'] + 1


def check_hosts(threshold=5):
    """Checks to see if the host is above the threshold and prints to the
       screen"""
    # Write to file the time host goes down
    os.system('clear')
    for entry in master:
        # If it hits the threshold write to file and speak
        if entry['count'] / 2 == 5:
            downAlert = os.system('espeak ' + entry['label'] + '"is down"')
            print(tick + entry['host'].ljust(15) + ' Went Down',
                  file=open(CURRENT_DIR + date + '.txt', 'a'))
            downAlert
            print(entry['host'].ljust(15)
                  + entry['label'].ljust(13)
                  + ' is '
                  + colors.WARN
                  + 'Down!'
                  + colors.END)
        # Print to screen the Status of hosts
        elif (entry['count'] / 2) > 5:
            print(entry['host'].ljust(15)
                  + entry['label'].ljust(13)
                  + ' is '
                  + colors.WARN
                  + 'DOWN!'
                  + colors.END)
        else:
            print(entry['host'].ljust(15)
                  + entry['label'].ljust(13)
                  + ' is '
                  + colors.OK
                  + 'UP'
                  + colors.END)


if __name__ == '__main__':
    master = []
    # Initialize hosts
    init(master)
    # Print to file that program has started
    print("*****Starting Program*****\n*****" + start + '****',
          file=open(date + '.txt', 'a'))
    while True:
        ping_hosts()
        check_hosts()
        time.sleep(1)
