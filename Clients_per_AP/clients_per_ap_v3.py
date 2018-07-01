# v0.30
# show client summary processing
# @author mcs
# 4/24/2018

# https://stackoverflow.com/questions/41879712/python-list-of-lists-to-dataframe-assertionerror

# https://stackoverflow.com/questions/42869544/dictionary-of-lists-to-dataframe

# https://stackoverflow.com/questions/25292568/converting-a-dictionary-with-lists-for-values-into-a-dataframe


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
    ssh_channel.send("config paging disable" + "\n")
    time.sleep(0.9)
    discard = ssh_channel.recv(10000)
    ssh_channel.send("show ap summary" + "\n")
    time.sleep(0.9)
    outp = ssh_channel.recv(100000)
    shapsumstring = outp.decode("utf-8")
    shapsumlist = shapsumstring.splitlines()
    shapsumlist = shapsumlist[9:-2]
    regex1 = re.compile(r'(.+?)(?: 2)')

    d = defaultdict(int)
    e = {}

    for line in shapsumlist:
        mo = regex1.search(line)
        ap_name = mo.group(1).rstrip()
        e[ap_name] = []

    c = 0
    x = 0
    starttime = time.time()
    while x < 5:

        ssh_channel.send("show client summary" + "\n")

        time.sleep(0.9)
        outp = ssh_channel.recv(150000)
        shclisumstring = outp.decode("utf-8")
        shclisumlist = shclisumstring.splitlines()
        # print("shclisumlist.splitlines(): {}".format(shclisumlist))

        del shclisumlist[:12]
        del shclisumlist[-3:]

        regex2 = re.compile(r'(?:(?:(?:[0-9a-f]{2}[:-]){5})(?:[0-9a-f]{2}))(?:\s)(.+?)(?:\s)')

        for line in shclisumlist:
            mo = regex2.search(line)
            ap_name = mo.group(1)
            d[ap_name] += 1

        for k, v in d.items():
            e[k].append(v)

        d.clear()
        shclisumstring = ''
        shclisumlist.clear()

        for key in e:
            if len(e[key]) == c:
                e[key].append(0)
        c += 1

        if x == 4:
            print()
            print('{:25}{:1}'.format('       AP', '               Count', ))
            print('=' * 43)

            for k, v in e.items():
                print('{:25}'.format(k), end='')
                for i in v:
                    print('{:6}'.format(i), end='')
                print()
            break

        time.sleep(15.0 - ((time.time() - starttime) % 15.0))

        x += 1


def main():
    # Get all devices from csv_file
    csvfile = "d:\python\projects\Clients_per_AP\SwitchData.csv"
    device_list = csv_reader(csvfile)

    #  Establish SSH connections
    ssh_conns = []
    ssh_save = []
    for a_device in device_list:
        ssh_pre, ssh_conn = login(**a_device)
        # Save the SSH connection to a list
        ssh_conns.append(ssh_conn)
        # Save the SSH preliminary connection to a separate list just to avoid a problem that otherwise happens
        ssh_save.append(ssh_pre)

    for a_connection in ssh_conns:
        ap_data(a_connection)


if __name__ == "__main__":
    main()
