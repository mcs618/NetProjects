# v0.34
# port error detector
# mcs
# 5/9/2017

import paramiko
import time
import re
import json

ip_addr = '192.168.1.206'
username = 'admin'
password = 'mcs618'

remote_conn_pre = paramiko.SSHClient()
remote_conn_pre.set_missing_host_key_policy(paramiko.AutoAddPolicy())
remote_conn_pre.connect(ip_addr, username=username, password=password, look_for_keys=False, allow_agent=False)
remote_conn = remote_conn_pre.invoke_shell()

remote_conn.send("terminal length 0" + "\n")
remote_conn.send("show version | inc System serial|uptime|image|Model number" + "\n")
# remote_conn.send("show version | inc \*|uptime|image" + "\n")
time.sleep(0.6)
outp = remote_conn.recv(5000)
shverstring = outp.decode("utf-8")
shverlist = shverstring.splitlines()
del shverlist[:3]
del shverlist[-1]
uptimelist = shverlist[0].split('is ')
uptime = uptimelist[1]
imagelist = shverlist[1].split('/')
imagetemp = imagelist[1]
image = imagetemp[:-1]
modellist = shverlist[2].split(': ')
model = modellist[1]
serialnumlist = shverlist[3].split(': ')
serialnum = serialnumlist[1]

remote_conn.send("terminal length 0" + "\n")
# remote_conn.send("show ip int brief | exc down" + "\n")
remote_conn.send("show ip int brief" + "\n")
time.sleep(0.6)
outp = remote_conn.recv(5000)
mystring = outp.decode("utf-8")
ipbrieflist = mystring.splitlines()
hostnamelist = ipbrieflist[1].split('>')
hostname = hostnamelist[0]
del ipbrieflist[:4]
del ipbrieflist[-1]

ipbriefRegex = re.compile(r'(\S+)(.+)')

ipbriefintlist = []
for elem in ipbrieflist:
    mo = ipbriefRegex.search(elem)
    if (mo.group(1)).startswith('Loop') or (mo.group(1)).startswith('Vlan'):
        continue
    ipbriefintlist.append(mo.group(1))

print('\n')
print("=" * 54 + "\n" + 13 * " " + "Device Port Error Report" + "\n" + "=" * 54)
print("Hostname:\t" + hostname)
print("IP address:\t" + ip_addr)
print("Model:\t\t" + model)
print("Serial:\t\t" + serialnum)
print("Uptime:\t\t" + uptime)
print("Version:\t" + image)
print()

output_lines = []
for intf in ipbriefintlist:
    remote_conn.send("show int " + intf + "\n")
    time.sleep(0.6)
    outp = remote_conn.recv(5000)
    shintstring = outp.decode("utf-8")
    shintlist = shintstring.splitlines()

    if shintlist[3].startswith('  Internet'):
        del shintlist[:19]
        del shintlist[-1]
    elif shintlist[8].startswith('  input flow-control'):
        del shintlist[:19]
        del shintlist[-1]
    else:
        del shintlist[:18]
        del shintlist[-1]


    def striplist(errlist):
        return [item.strip() for item in errlist]


    errdict = {}
    for line in shintlist:
        errors_list = striplist(line.split(","))

        errRegex = re.compile(r'(\d+)(\s)(\D+)')

        for elem in errors_list:
            mo = errRegex.search(elem)
            errdict[mo.group(3)] = int(mo.group(1))

    del errdict['packets output']
    del errdict['bytes']
    if 'multicast' in errdict:
        del errdict['multicast']

    if any(errdict.values()):
        output_lines.append("Interface " + intf)
        output_lines.append(errdict)

outputfile = ("d:\\mark\\python\\Projects\\error_detect\\" + hostname)
str_object = json.dumps(output_lines, indent=4, separators=(',', ': '))
repr(str_object)
with open(outputfile, 'w') as f:
    f.write("=" * 54 + "\n" + 13 * " " + "Device Port Error Report" + "\n" + "=" * 54 + "\n")
    f.write("Hostname:\t" + hostname + "\n")
    f.write("IP address:\t" + ip_addr + "\n")
    f.write("Model:\t\t" + model + "\n")
    f.write("Serial:\t\t" + serialnum + "\n")
    f.write("Uptime:\t\t" + uptime + "\n")
    f.write("Version:\t" + image + "\n")
    f.write(str_object)
