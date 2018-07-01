# v0.30d
# port error detector
# mcs
# 5/1/2017
#
# rows 0 - 8

import paramiko
import time
import re

ip_addr = '192.168.1.204'
username = 'admin'
password = 'mcs618'

remote_conn_pre = paramiko.SSHClient()
remote_conn_pre.set_missing_host_key_policy(paramiko.AutoAddPolicy())
remote_conn_pre.connect(ip_addr, username=username, password=password, look_for_keys=False, allow_agent=False)
remote_conn = remote_conn_pre.invoke_shell()
remote_conn.send("terminal length 0" + "\n")
remote_conn.send("show ip int brief" + "\n")
time.sleep(1)
outp = remote_conn.recv(5000)
mystring = outp.decode("utf-8")
ipbrieflist = mystring.splitlines()
hostnamelist = ipbrieflist[1].split('>')
hostname = hostnamelist[0]
ipbrieflen = int(len(ipbrieflist) - 5)
del ipbrieflist[:4]
del ipbrieflist[ipbrieflen]
print()

ipbriefRegex = re.compile(r'(\S+)(.+)')

ipbriefintlist = []
for elem in ipbrieflist:
    mo = ipbriefRegex.search(elem)
    if (mo.group(1)).startswith('Loop') or (mo.group(1)).startswith('Vlan'):
        continue
    ipbriefintlist.append(mo.group(1))

print("*********")
print(ipbriefintlist[0])
print(ipbriefintlist[1])
print("*********")
print()
print(hostname)

for intf in ipbriefintlist:
    print("*****")
    print("Interface " + intf)
    remote_conn.send("show int " + intf + "\n")
    time.sleep(1)
    outp = remote_conn.recv(5000)
    shintstring = outp.decode("utf-8")
    shintlist = shintstring.splitlines()
    
    if not shintlist[3].startswith('  Internet'):
        shintlen = int(len(shintlist) - 20)
        del shintlist[:19]
        del shintlist[shintlen]
    else:
        shintlen = int(len(shintlist) - 21)
        del shintlist[:20]
        del shintlist[shintlen]

    def striplist(errlist):
        return [item.strip() for item in errlist]

    errdict = {}
    for line in shintlist:
        errors_list = striplist(line.split(","))

        errRegex = re.compile(r'(\d+)(\s)(\D+)')

        for elem in errors_list:
            mo = errRegex.search(elem)
            errdict[mo.group(3)] = int(mo.group(1))

        if len(errdict) == 21:
            del errdict['packets output']
            del errdict['bytes']
            for k, v in errdict.items():
                print(k, v)

            print()

        # if counter = 19 and value = 0, continue
        
        # if len(errdict) == 21:
            # for k, v in errdict.items():
                # print(k, v)
            # print()
 
        # for elem in errors_list:
            # mo = errRegex.search(elem)
            # errdict[mo.group(3)] = int(mo.group(1))
            # if int(mo.group(1)) > 0:
                # print("There are errors")
            # else:
                # print("There are no errors")

        # print(errdict)
        
        # Model for how to bypass unwanted lines

file = ['beef', 'string1', 'veal', 'string2', 'pork', 'string3', 'chicken']
strings = (
    "string1",
    "string2",
    "string3"
)

for item in file:
    if any(s in item for s in strings):
        print("yay!")
    else:
        continue
        
------------------------

for k, v in dict.items():
	    print(k,v)
