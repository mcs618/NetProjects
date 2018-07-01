# v0.30
# rssi snr processing
# @author mcs
# 4/12/2018

# https://stackoverflow.com/questions/4915920/how-to-delete-an-item-in-a-list-if-it-exists

# https://dbader.org/blog/python-generator-expressions

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


def rssi_snr(ssh_channel):
    ssh_channel.send("config paging disable" + "\n")
    time.sleep(0.9)
    outp = ssh_channel.recv(25000)
    shclisumstring = outp.decode("utf-8")
    shclisumstring = ''

    d = defaultdict(dict)

    x = 0
    starttime = time.time()
    while x < 1:

        ssh_channel.send("show client summary" + "\n")

        time.sleep(1.0)
        outp = ssh_channel.recv(150000)
        shclisumstring = outp.decode("utf-8")
        shclisumlist = shclisumstring.splitlines()
        # print("shclisumlist.splitlines(): {}".format(shclisumlist))

        del shclisumlist[:12]
        del shclisumlist[-3:]

        regex1 = re.compile(r'((?:(?:[0-9a-f]{2}[:-]){5})(?:[0-9a-f]{2}))')
        regex2 = re.compile(r'(.+?)(?:\.+?\s)(.*)')
        ap_MAC = set()

        # cleaned_list = [line for line in shclisumlist if 'AP5-Cafe_NW' in line]
        #                                                   AP5-213
        #                                                   AP5-ES_LMC

        ap = input("Please input the name of the AP we wish to examine: ")

        for line in (line for line in shclisumlist if ap in line):
            mo = regex1.search(line)
            ap_MAC.add(mo.group(1))

        ccounter = 1
        for mac in ap_MAC:
            ssh_channel.send("show client detail " + mac + "\n")

            time.sleep(1.0)
            outp = ssh_channel.recv(100000)
            shclidetstring = outp.decode("utf-8")
            shclidetlist = shclidetstring.splitlines()
            # print("shclisumlist.splitlines(): {}".format(shclisumlist))

            desired_info = []
            del shclidetlist[:1]
            del shclidetlist[111:]
            del shclidetlist[17:105]

            for line in shclidetlist:
                if line.startswith('Client MAC Address'):
                    desired_info.append(line)
                    break
            del shclidetlist[:9]
            for line in shclidetlist:
                if line.startswith('Wireless LAN Network Name'):
                    desired_info.append(line)
                    break
            del shclidetlist[:6]
            for line in shclidetlist:
                if line.startswith('IP Address'):
                    desired_info.append(line)
                    break
            del shclidetlist[:4]
            for line in shclidetlist:
                if line.startswith('      Radio Signal Strength Indicator'):
                    desired_info.append(line)
                    break
            for line in shclidetlist:
                if line.startswith('      Signal to Noise Ratio'):
                    desired_info.append(line)
                    break

            client = 'Client ' + str(ccounter)

            print(client)

            for line in desired_info:
                mo = regex2.search(line)
                d[client].update({mo.group(1).strip(): mo.group(2).strip()})

            ccounter += 1
            shclidetstring = ''
            shclidetlist.clear()

        x += 1

    for k, v in d.items():
        print(k, ' ', v)


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
        rssi_snr(a_connection)


if __name__ == "__main__":
    main()
