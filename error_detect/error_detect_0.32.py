# v0.32
# port error detector
# mcs
# 5/6/2017

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
time.sleep(0.6)
outp = remote_conn.recv(5000)
mystring = outp.decode("utf-8")
ipbrieflist = mystring.splitlines()
hostnamelist = ipbrieflist[1].split('>')
hostname = hostnamelist[0]
del ipbrieflist[:4]
del ipbrieflist[-1]
print()

ipbriefRegex = re.compile(r'(\S+)(.+)')

ipbriefintlist = []
for elem in ipbrieflist:
    mo = ipbriefRegex.search(elem)
    if (mo.group(1)).startswith('Loop') or (mo.group(1)).startswith('Vlan'):
        continue
    ipbriefintlist.append(mo.group(1))

# print("*********")
# print(ipbriefintlist[0])
# print(ipbriefintlist[1])
# print("*********")
# print()
print(hostname)

for intf in ipbriefintlist:
    print("Interface " + intf)
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
    for k, v in errdict.items():
        print(k, v)

    print()
    
    
# I am in the process of writing a program that connects to a Cisco switch or
# router and then examines the output of a 'show int '. I then process\parse the
# data to the point where I have a dictionary of twenty-one key\value pairs.
# All values are integers.
for device in devices:
    s = run_show_interfaces(device)
    d = preprocess_parse(s)

    # Check each value. If ALL values are zero, then skip that dictionary. If ANY
    # single value is non-zero (it will be a positive integer if it is not zero),
    # then I want to save to a file the entire dictionary.
    if any(d.values()):
        filename = os.path.join(device, '.txt')
        with open(filename, 'w') as f:
            json.dump(d, f)

# FYI, the any() function has an early-out and will stop looking as soon as 
# it finds a non-zero value. In Python 3, values() returns a view of the data
# so it doesn't copy all of information. In Python 2, use viewvalues() to 
# achieve the same effect. Taken together, this will give you great preformance.


d = {"name":"interpolator",
     "children":[{'name':key,"size":value} for key,value in sample.items()]}
j = json.dumps(d, indent=4)
f = open('sample.json', 'w')
print >> f, j
f.close()

# It this way, I got a pretty-print json file. 
# The tricks print >> f, j is found from here: http://www.anthonydebarros.com/2012/03/11/generate-json-from-sql-using-python/


# As a second example, the script next builds a list of dictionaries, 
# with each row in the database becoming one dictionary and each field 
# in the row a key-value pair:

objects_list = []
for row in rows:
    d = collections.OrderedDict()
    d['id'] = row.ID
    d['FirstName'] = row.FirstName
    d['LastName'] = row.LastName
    d['Street'] = row.Street
    d['City'] = row.City
    d['ST'] = row.ST
    d['Zip'] = row.Zip
    objects_list.append(d)
 
j = json.dumps(objects_list)
objects_file = 'student_objects.js'
f = open(objects_file,'w')
print >> f, j