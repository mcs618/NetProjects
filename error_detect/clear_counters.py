# v0.1
# clear counters
# mcs
# 5/16/2017

import paramiko
import time
import csv

csvfile = "d:\\mark\\python\\Projects\\error_detect\\SwitchData.csv"

with open(csvfile, "r") as datafile:
    datareader = csv.DictReader(datafile)
    for row in datareader:
        if datareader.line_num == 1:
            continue
        ip_addr = row['IP_address']
        username = row['Username']
        password = row['Password']

        ssh = paramiko.SSHClient()
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        ssh.connect(ip_addr, username=username, password=password, look_for_keys=False, allow_agent=False)
        ssh_channel = ssh.invoke_shell()
        
        ssh_channel.send("enable" + "\n")
        time.sleep(0.5)
        outp = ssh_channel.recv(1000)
        output = outp.decode("utf-8")
        if 'Password:' in output:
            ssh_channel.send(password + "\n")
            time.sleep(0.5)
            outp = ssh_channel.recv(1000)
            output = outp.decode("utf-8")
        print(output)
        
        ssh_channel.send("clear counters" + "\n")
        time.sleep(0.5)
        outp = ssh_channel.recv(1000)
        output = outp.decode("utf-8")
        if 'confirm' in output:
            ssh_channel.send("\n")
            time.sleep(0.5)
            outp = ssh_channel.recv(1000)
            output = outp.decode("utf-8")
        print(output)
        
        ssh_channel.send("exit" + "\n")
        time.sleep(0.3)
        print("  Exiting...")
