# v0.30
# port error detector
# mcs
# 5/1/2017

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
remote_conn.send("show ip int brief" + "\n")
time.sleep(1)
outp = remote_conn.recv(5000)
mystring = outp.decode("utf-8")
print()
print("*********")
print(mystring)
print("*********")
print()
remote_conn.send("terminal length 0" + "\n")
remote_conn.send("show int f0/1" + "\n")
time.sleep(1)
outp = remote_conn.recv(5000)
mystring = outp.decode("utf-8")
print(mystring)
mylist = mystring.splitlines()
print()
errors = mylist[21]
print(errors)
errors_list = errors.split(",")
print("errors_list: " + str(errors_list))
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


# for elem in range(2, mylist_len - 1):
    # print(mylist[elem])

# for elem in mylist:
    # if elem[0] or elem[1]:
        # continue
    # print(elem)

# 20 - 27

rtr-1841>
show ip int brief
Interface                  IP-Address      OK? Method Status                Protocol
FastEthernet0/0            unassigned      YES NVRAM  administratively down down    
FastEthernet0/1            192.168.1.204   YES NVRAM  up                    up      
Loopback0                  172.17.0.1      YES NVRAM  up                    up      
rtr-1841>
terminal length 0
rtr-1841>show int f0/1
FastEthernet0/1 is up, line protocol is up 
  Hardware is Gt96k FE, address is 0021.5500.4fa1 (bia 0021.5500.4fa1)
  Internet address is 192.168.1.204/24
  MTU 1500 bytes, BW 100000 Kbit/sec, DLY 100 usec, 
     reliability 255/255, txload 1/255, rxload 1/255
  Encapsulation ARPA, loopback not set
  Keepalive set (10 sec)
  Full-duplex, 100Mb/s, 100BaseTX/FX
  ARP type: ARPA, ARP Timeout 04:00:00
  Last input 00:00:00, output 00:00:00, output hang never
  Last clearing of "show interface" counters never
  Input queue: 0/75/0/0 (size/max/drops/flushes); Total output drops: 0
  Queueing strategy: fifo
  Output queue: 0/40 (size/max)
  5 minute input rate 1000 bits/sec, 1 packets/sec
  5 minute output rate 1000 bits/sec, 1 packets/sec
     2828 packets input, 267428 bytes
     Received 915 broadcasts (0 IP multicasts)
     0 runts, 0 giants, 0 throttles
     0 input errors, 0 CRC, 0 frame, 0 overrun, 0 ignored
     0 watchdog
     0 input packets with dribble condition detected
     3740 packets output, 453148 bytes, 0 underruns
     0 output errors, 0 collisions, 2 interface resets
     4 unknown protocol drops
     0 babbles, 0 late collision, 0 deferred
     0 lost carrier, 0 no carrier
     0 output buffer failures, 0 output buffers swapped out
