import re
from collections import defaultdict

client_sum = "d:\\python\\projects\\Clients_per_AP\\show_client_summary.txt"
per_AP = "d:\\python\\projects\\Clients_per_AP\\Clients_per_AP.txt"

d = defaultdict(int)
e = defaultdict(list)

with open(per_AP, 'w') as pap:
    with open(client_sum, 'r') as cs:
        for line in cs:
            regex = re.compile(r'([0-9a-f]{2}[:-]){5}([0-9a-f]{2})(\s)(.+?)(\s)')
            mo = regex.search(line)
            ap_name = mo.group(4)

            d[ap_name] += 1

        for k, v in d.items():
            e[k].append(v)

        total = sum(d.values())
        print("The total number of attached clients is: ", total)
        print()

        print('{:25}{:5}'.format('       AP', 'Count'))
        print('-' * 30)

        for k, v in d.items():
            if v > 30:
                print('{:25}{:5}'.format(k, d[k]), "  <-----  Client count greater than 30.")
            else:
                print('{:25}{:5}'.format(k, d[k]))
