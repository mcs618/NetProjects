Text = "d:\\python\\projects\\migrate_APs\\show_ap_summary.txt"
newfile = "d:\\python\\projects\\migrate_APs\\assign_to_AP_group.txt"

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

AP_group_name = 'GB-AP-Group'

with open(newfile, "a") as file2:
    counter = 0
    for name in apnamelist:
        file2.write("config ap group-name {0} {1}\n".format(AP_group_name, name))
        file2.write('y\n')
        counter += 1
        if counter == 20:
            file2.write("\n")
            counter = 0
