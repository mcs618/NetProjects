# v0.47
# device port error report
# mcs
# 5/26/2017

import paramiko
import time
import re
import json
import csv


def errordetect():
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
            ssh_channel.send("terminal length 0" + "\n")
            ssh_channel.send("show version | inc System serial|uptime|image|Model number|\*" + "\n")

            time.sleep(0.6)
            outp = ssh_channel.recv(5000)
            shverstring = outp.decode("utf-8")
            shverlist = shverstring.splitlines()
            del shverlist[:3]
            del shverlist[-1]
            uptimelist = shverlist[0].split('is ')
            uptime = uptimelist[1]
            imagelist = shverlist[1].split(':')
            imagetemp = imagelist[1]

            if imagetemp.startswith('/'):
                image = imagetemp[1:-1]

            else:
                image = imagetemp[:-1]

            if shverlist[2].startswith('Model'):
                modellist = shverlist[2].split(': ')
                model = modellist[1]
                serialnumlist = shverlist[3].split(': ')
                serialnum = serialnumlist[1]
            else:
                rtrRegex = re.compile(r'(\*0\s+)(CISCO\d+)(\s+)(\w+)(\s+)')
                mo = rtrRegex.search(shverlist[2])
                model = mo.group(2)
                serialnum = mo.group(4)

            ssh_channel.send("terminal length 0" + "\n")
            ssh_channel.send("show ip int brief | exc down" + "\n")
            # ssh_channel.send("show ip int brief" + "\n")
            time.sleep(0.6)
            outp = ssh_channel.recv(5000)
            mystring = outp.decode("utf-8")
            ipbrieflist = mystring.splitlines()
            hostnamelist = re.split('[>#]', ipbrieflist[1])
            hostname = hostnamelist[0]
            del ipbrieflist[:3]
            del ipbrieflist[-1]

            ipbriefRegex = re.compile(r'(\S+)(.+)')

            ipbriefintlist = []
            for elem in ipbrieflist:
                if elem == '':
                    continue
                mo = ipbriefRegex.search(elem)
                if (mo.group(1)).startswith('Loop') or (mo.group(1)).startswith('Vlan'):
                    continue
                if (mo.group(1)).startswith('Tunnel') or (mo.group(1)).startswith('Port-channel'):
                    continue
                ipbriefintlist.append(mo.group(1))

            print('\n')
            print("=" * 54 + "\n" + 14 * " " + "Physical Port Error Report" + "\n" + "=" * 54)
            print("Hostname:\t" + hostname)
            print("IP address:\t" + ip_addr)
            print("Model:\t\t" + model)
            print("Serial:\t\t" + serialnum)
            print("Uptime:\t\t" + uptime)
            print("Version:\t" + image)
            print()

            output_lines = []
            for intf in ipbriefintlist:
                print("Interface " + intf)
                ssh_channel.send("show int " + intf + "\n")
                time.sleep(0.6)
                outp = ssh_channel.recv(5000)
                shintstring = outp.decode("utf-8")
                shintlist = shintstring.splitlines()

                if shintlist[3].startswith('  Description'):
                    del shintlist[3]
                if shintlist[19].startswith('     Received'):
                    del shintlist[19]
                del shintlist[:19]
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

            today = time.strftime("%x")
            timenow = time.strftime("%X")
            filename = (hostname + '_' + '%s' + '_' + '%s') % (today, timenow)
            filename = filename.replace("/", "-")
            filename = filename.replace(":", "-")

            outputfile = ("d:\\mark\\python\\Projects\\error_detect\\" + filename)
            str_object = json.dumps(output_lines, indent=4, separators=(',', ': '))
            repr(str_object)
            with open(outputfile, 'w') as f:
                f.write("=" * 54 + "\n" + 14 * " " + "Physical Port Error Report" + "\n" + "=" * 54 + "\n")
                f.write("Hostname:\t" + hostname + "\n")
                f.write("IP address:\t" + ip_addr + "\n")
                f.write("Model:\t\t" + model + "\n")
                f.write("Serial:\t\t" + serialnum + "\n")
                f.write("Uptime:\t\t" + uptime + "\n")
                f.write("Version:\t" + image + "\n")
                f.write(str_object)
                

def main():
    x = 0
    starttime = time.time()
    while x < 12:
        errordetect()
        time.sleep(300.0 - ((time.time() - starttime) % 300.0))
        x += 1

if __name__ == "__main__":
    main()

"""
>>> platforms = ('cisco_nxos', 'cisco_ios', 'cisco_xr', 'cisco_asa', 'juniper_junos', 'arista_eos')
>>> if 'f5' in platforms:
...   print "FOUND"
... 
>>> if 'cisco_asa' in platforms:
...   print "FOUND"
... 
FOUND
"""