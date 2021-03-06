# v0.10
# show client summary processing
# @author mcs
# 4/1/2018

import paramiko
import time
import re
# import json
import csv
from collections import defaultdict


def csv_reader(csvfile):
    """Read CSV file, return a list of devices."""
    device_list = []
    with open(csvfile, "r") as datafile:
        datareader = csv.DictReader(datafile)
        for row in datareader:
            if datareader.line_num == 1:
                continue
            ip_addr = row['IP_address']
            username = row['Username']
            password = row['Password']
            device_dict = {'ip_addr': ip_addr, 'username': username, 'password': password}
            # add device to device_list
            device_list.append(device_dict)

    return device_list


def login(ip_addr, username, password):
    """Establish SSH connection, return SSH conn object."""
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    ssh.connect(ip_addr, username=username, password=password, look_for_keys=False, allow_agent=False)
    ssh_channel = ssh.invoke_shell()
    ssh_channel.send("\n")
    ssh_channel.send(username + "\n")
    ssh_channel.send(password + "\n")
    # Need to return both ssh and ssh_channel
    return ssh, ssh_channel


def ap_data(ssh_channel):
    ssh_channel.send("\n")
    ssh_channel.send("config paging disable" + "\n")
    ssh_channel.send("show client summary" + "\n")
    d = defaultdict(int)

    time.sleep(0.9)
    outp = ssh_channel.recv(35000)
    shclisumstring = outp.decode("utf-8")
    shclisumlist = shclisumstring.splitlines()
    # print("shclisumlist.splitlines(): {}".format(shclisumlist))
    del shclisumlist[:22]
    del shclisumlist[-3:]
    for line in shclisumlist:
            regex = re.compile(r'([0-9a-f]{2}[:-]){5}([0-9a-f]{2})(\s)(.+?)(\s)')
            mo = regex.search(line)
            ap_name = mo.group(4)
            d[ap_name] += 1

    total = sum(d.values())
    print("The total number of attached clients is: ", total)
    print()

    print('{:25}{:5}'.format('       AP', 'Count'))
    print('-' * 30)

    for k, v in d.items():
        if v > 30:
            print('{:25}{:5}'.format(k, d[k]), "  <-----  Client count greater than 30.")
        else:
            print('{:25}{:5}'.format(k, d[k]))


def main():
    # Get all devices from csv_file
    # csvfile = "f:\mark\python\Projects\error_detect\SwitchData.csv"
    csvfile = "d:\python\projects\Clients_per_AP\SwitchData.csv"
    device_list = csv_reader(csvfile)

    # ip_addrs = [item['ip_addr'] for item in device_list]
    # for item in device_list:
    #     ip_addrs.append(item['ip_addr'])

    #  Establish SSH connections
    ssh_conns = []
    ssh_save = []
    for a_device in device_list:
        ssh_pre, ssh_conn = login(**a_device)
        # Save the SSH connection to a list
        ssh_conns.append(ssh_conn)
        # Save the SSH preliminary connection to a separate list just to avoid a problem that otherwise happens
        ssh_save.append(ssh_pre)

    x = 0
    starttime = time.time()
    while x < 1:
        i = 0
        for a_connection in ssh_conns:
            ap_data(a_connection)
            i += 1
        x += 1
        if x == 1:
            break
        time.sleep(15.0 - ((time.time() - starttime) % 15.0))


if __name__ == "__main__":
    main()
