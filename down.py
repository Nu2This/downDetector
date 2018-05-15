#!/usr/bin/env python3
import os
import time
import subprocess


date = time.strftime('%m%y')
tick = time.strftime('%d @ %T ')
start = time.strftime('%m/%d/%y %T')
# This makes it so it does not matter where you run the script from, it will
# always find the hosts.txt file inside the directory the script is located.
scriptLocation = os.path.dirname(os.path.realpath(__file__))


class colors:
    WARN = '\033[91m'
    END = '\033[0m'
    OK = '\033[36m'


def poll(host):
    """Ping the hosts in the host file"""
    # Create subprocess object for ping
    p = subprocess.Popen('ping -c 1 -W 1 '
                         + str(host),
                         stdout=subprocess.PIPE,
                         shell=True)
    p.wait()
    # Ping the host and return True if it is up
    if p.poll() != 0:
        return False
    else:
        return True


def init(entry):
    """Initialize host file with false count(for poll funct)"""
    # Open hosts.txt file and create a master list to hold dicts
    with open(scriptLocation + '/hosts.txt', 'r') as f:
        for line in f:
            # create a list from the data in the line
            data = line.split()
            # Append to the master list a dictionary with labels and data
            # from the 'data' variable
            master.append({'host': data[0], 'label': data[1], 'count': 0})


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
                      file=open(scriptLocation + '/' + date + '.txt', 'a'))
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
                  file=open(scriptLocation + '/' + date + '.txt', 'a'))
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
        time.sleep(10)
