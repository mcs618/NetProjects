# v0.30c
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

for intf in ipbriefintlist:
    remote_conn.send("show int " + intf + "\n")
    time.sleep(1)
    outp = remote_conn.recv(5000)
    shintstring = outp.decode("utf-8")
    shintlist = shintstring.splitlines()
    if not shintlist[3].startswith('  Internet'):
        continue
    shintlen = int(len(shintlist) - 21)
    del shintlist[:20]
    del shintlist[shintlen]
    print("#####")
    print(shintstring)
    print("#####")
    
    errors = shintlist[4]
    errors_list = errors.split(",")


    def striplist(errlist):
        return [item.strip() for item in errlist]


    errors_list = striplist(errors_list)
    print()
    print("errors_list: " + str(errors_list))

    errRegex = re.compile(r'(\d+)(\s)(\D+)')

    errdict = {}
    for elem in errors_list:
        mo = errRegex.search(elem)
        errdict[mo.group(3)] = int(mo.group(1))
        if int(mo.group(1)) > 0:
            print("There are errors")
        else:
            print("There are no errors")

    print(errdict)
