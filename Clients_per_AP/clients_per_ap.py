import re
from collections import defaultdict

client_sum = "d:\\python\\projects\\Clients_per_AP\\show_client_summary.txt"
per_AP = "d:\\python\\projects\\Clients_per_AP\\Clients_per_AP.txt"

d = defaultdict(int)

with open(per_AP, 'w') as pap:
    with open(client_sum, 'r') as cs:
        for line in cs:
            regex = re.compile(r'([0-9a-f]{2}[:-]){5}([0-9a-f]{2})(\s)(.+?)(\s)')
            mo = regex.search(line)
            ap_name = mo.group(4)

            d[ap_name] += 1

        for k, v in d.items():
            if v > 5:
                print(k, ":", v, "  <-----  Client count greater than 5.")
            else:
                print(k, ":", v)
