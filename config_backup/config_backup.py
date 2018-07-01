# @version 0.1
# device backup
# @author mcs
# 5/18/2017

import paramiko
import csv
import time
import os


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
        time.sleep(0.3)
        outp = ssh_channel.recv(1000)
        output = outp.decode("utf-8")
        if 'Password:' in output:
            ssh_channel.send(password + "\n")
            time.sleep(0.3)
            outp = ssh_channel.recv(1000)
            output = outp.decode("utf-8")
        hostlist = output.splitlines()
        hostname1 = hostlist[1]
        hostname = hostname1[:-1]

        ssh_channel.send("config t" + "\n")
        time.sleep(0.3)

        ssh_channel.send("file prompt quiet" + "\n")
        time.sleep(0.3)

        ssh_channel.send("exit" + "\n")
        time.sleep(0.3)

        today = time.strftime("%x")
        timenow = time.strftime("%X")
        filename = (hostname + '-' + '%s' + '_' + '%s') % (today, timenow)
        filename = filename.replace("/", "-")
        filename = filename.replace(":", "-")
        
        if os.path.isfile("flash:vlan.dat"):
            ssh_channel.send("copy flash:vlan.dat flash:" + filename + ".dat" + "\n")
            time.sleep(0.3)

            ssh_channel.send("copy flash:" + filename + ".dat" " tftp://192.168.1.106/" + filename + ".dat" + "\n")
            time.sleep(0.3)

        ssh_channel.send("copy run tftp://192.168.1.106/" + filename + ".cfg" + "\n")
        time.sleep(0.3)
        
        ssh_channel.send("config t" + "\n")
        time.sleep(0.3)

        ssh_channel.send("file prompt noisy" + "\n")
        time.sleep(0.3)

        ssh_channel.send("exit" + "\n")
        time.sleep(0.3)
        
        ssh_channel.send("exit" + "\n")
        time.sleep(0.3)
