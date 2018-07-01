Text = "d:\\python\\projects\\migrate_APs\\show_ap_summary.txt"
newfile = "d:\\python\\projects\\migrate_APs\\assign_to_flex_group.txt"

ignore = ('(Cisco Controller)',
          'Number of APs',
          'Global AP username',
          'Global AP User Name',
          'Global AP Dot1x username',
          'Global AP Dot1x User Name',
          'AP Name',
          '----------')

apmaclist = []
with open(Text, 'r') as fh:
    for line in fh:
        if line.startswith(ignore) or len(line) <= 1:
            continue
        templist = line.split()
        apmaclist.append(templist[3])

AP_group_name = 'MT_Flex'

with open(newfile, "a") as file2:
    counter = 0
    for mac in apmaclist:
        file2.write("config flexconnect group {0} ap add {1}\n".format(AP_group_name, mac))
        counter += 1
        if counter == 20:
            file2.write("\n")
            counter = 0
