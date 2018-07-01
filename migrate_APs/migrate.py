Text = "d:\\python\\projects\\migrate_APs\\show_ap_summary.txt"
newfile = "d:\\python\\projects\\migrate_APs\\config_ap_primary.txt"

ignore = ('(Cisco Controller)',
          'Number of APs',
          'Global AP username',
          'Global AP User Name',
          'Global AP Dot1x username',
          'Global AP Dot1x User Name',
          'AP Name',
          '----------')

apnamelist = []
with open(Text, 'r') as fh:
    for line in fh:
        if line.startswith(ignore) or len(line) <= 1:
            continue
        templist = line.split()
        apnamelist.append(templist[0])

newcontroller_name = 'NewController'
newcontroller_ip_addr = '10.0.0.1'

with open(newfile, "a") as file2:
    counter = 0
    for name in apnamelist:
        file2.write("config ap primary-base {0} {2} {1}\n".format(newcontroller_name, newcontroller_ip_addr, name))
        counter += 1
        if counter == 20:
            file2.write("\n")
            counter = 0
