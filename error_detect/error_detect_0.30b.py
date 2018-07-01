# v0.30b
# port error detector
# mcs
# 5/1/2017
#
#  rows 18 - 27

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
outp = remote_conn.recv(5000)
mystring = outp.decode("utf-8")
print("*********")
print(mystring)
print("*********")
mystring = ''
print("*********")
print(mystring)
print("*********")
remote_conn.send("show ip int brief" + "\n")
time.sleep(1)
outp = remote_conn.recv(5000)
mystring = outp.decode("utf-8")
ipbrieflist = mystring.splitlines()
ipbrieflen = int(len(ipbrieflist) - 3)
del ipbrieflist[:2]
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

remote_conn.send("terminal length 0" + "\n")
remote_conn.send("show int f0/1" + "\n")
time.sleep(1)
outp = remote_conn.recv(5000)
shintstring = outp.decode("utf-8")
print("#####")
print(shintstring)
print("#####")
shintlist = shintstring.splitlines()
shintlen = int(len(shintlist) - 3)
del shintlist[:2]
del shintlist[shintlen]
print()
errors = shintlist[23]
print(errors)
errors_list = errors.split(",")
print("shintlist: " + str(errors_list))
print()


def striplist(errlist):
    return [item.strip() for item in errlist]


errors_list = striplist(errors_list)
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
