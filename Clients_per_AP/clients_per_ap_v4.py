# v0.42
# show client summary processing
# @author mcs
# 4/25/2018

# https://stackoverflow.com/questions/41879712/python-list-of-lists-to-dataframe-assertionerror

# https://stackoverflow.com/questions/42869544/dictionary-of-lists-to-dataframe

# https://stackoverflow.com/questions/25292568/converting-a-dictionary-with-lists-for-values-into-a-dataframe

# https://stackoverflow.com/questions/50008491/trying-to-create-a-seaborn-heatmap-from-a-pandas-dataframe/50008537?noredirect=1#comment87033687_50008537

import paramiko
import time
import re
import csv
from collections import defaultdict
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt


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
    time.sleep(1.0)
    discard = ssh_channel.recv(10000)
    ssh_channel.send("show ap summary" + "\n")
    time.sleep(1.0)
    outp = ssh_channel.recv(100000)
    shapsumstring = outp.decode("utf-8")
    shapsumlist = shapsumstring.splitlines()
    shapsumlist = shapsumlist[9:-2]
    regex1 = re.compile(r'(.+?)(?: 2)')
    regex2 = re.compile(r'(?:(?:(?:[0-9a-f]{2}[:-]){5})(?:[0-9a-f]{2}))(?:\s)(.+?)(?:\s)')

    d = defaultdict(int)
    e = {}
    cols = []
    index = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I']
    c = 0
    x = 0

    for line in shapsumlist:
        mo = regex1.search(line)
        ap_name = mo.group(1).rstrip()
        e[ap_name] = []
        cols.append(ap_name)

    while x < 9:

        ssh_channel.send("show client summary" + "\n")

        time.sleep(1.0)
        outp = ssh_channel.recv(150000)
        shclisumstring = outp.decode("utf-8")
        shclisumlist = shclisumstring.splitlines()
        # print("shclisumlist.splitlines(): {}".format(shclisumlist))

        del shclisumlist[:12]
        del shclisumlist[-3:]

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

        if x == 8:

            df = pd.DataFrame(e, index=index, columns=cols)
            df = df.transpose()

            my_dpi = 96
            sns.set(font_scale=2)
            # plt.figure(figsize=(13, 91))
            plt.figure(figsize=(2016 / my_dpi, 9120 / my_dpi), dpi=my_dpi)

            sns.heatmap(df, cmap='RdYlGn_r', linewidths=0.5, annot=True, annot_kws={"size": 20})

            plt.savefig('d:\\python\\projects\\clients_per_ap\\ac.png')
            plt.show()

        # time.sleep(15.0 - ((time.time() - starttime) % 15.0))
        time.sleep(15.0 - time.time() % 15.0)

        x += 1


def main():
    # Get all devices from csv_file
    csvfile = "d:\python\projects\Clients_per_AP\SwitchData.csv"
    device_list = csv_reader(csvfile)

    # Establish SSH connections
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
