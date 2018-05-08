import os
import time
import subprocess


date = time.strftime('%m%d%y')
tick = time.strftime('%T ')
hostsFile = os.path.dirname(os.path.realpath('hosts.txt'))


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


def init(host):
    """Initialize host file with false count(for poll funct)"""
    with open('hosts.txt', 'r') as f:
        for host in f:
            hosts.setdefault(host, 0)


def ping_hosts(hosts):
    """Use poll function to ping the hosts and change values inside the host
       dictionary"""
    with open('hosts.txt', 'r') as f:
        for host in f:
            # If host is up set counter to zero
            if poll(host):
                # Write to file if host came back from down state and speak
                if hosts[host] / 2 > 5:
                    upAlert = os.system('espeak ' + host.strip() + '"is up"')
                    print(tick + host.strip().ljust(15) + ' Came Up',
                          file=open(date + '.txt.', 'a'))
                    upAlert
                hosts[host] = 0
            # If host is down add to counter
            else:
                hosts[host] = hosts[host] + 1


def check_hosts(threshold=5):
    """Checks to see if the host is above the threshold and prints to the
       screen"""
    # Write to file the time host goes down
    os.system('clear')
    for host in hosts:
        # If it hits the threshold write to file and speak
        if hosts[host] / 2 == 5:
            downAlert = os.system('espeak ' + host.strip() + '"is down"')
            print(tick + host.strip().ljust(15) + ' Went Down',
                  file=open(date + '.txt', 'a'))
            downAlert
            print(host.strip().ljust(15)
                  + ' is '
                  + colors.WARN
                  + 'Down!'
                  + colors.END)
        # Print to screen the Status of hosts
        elif (hosts[host] / 2) > 5:
            print(host.strip().ljust(15)
                  + ' is '
                  + colors.WARN
                  + 'DOWN!'
                  + colors.END)
        else:
            print(host.strip().ljust(15)
                  + ' is '
                  + colors.OK
                  + 'UP'
                  + colors.END)


if __name__ == '__main__':
    hosts = {}
    # Initialize hosts
    init(hosts)
    # Print to file that program has started
    print("*****Starting Program*****",
          file=open(date + '.txt', 'a'))
    while True:
        ping_hosts(hosts)
        check_hosts()
        time.sleep(10)
