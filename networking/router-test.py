# import ipaddress
# import requests
#
#
#
# for ip_addr in ip_addrs:
#     url = f'http://{ip_addr}'
#     try:
#         r = requests.get(url, timeout=1)
#         if r.ok:
#             print(f'{url} is accessible private network')
#         else:
#             pass
#     except:
#         pass

import requests
import ipaddress
from concurrent.futures import ThreadPoolExecutor, as_completed

print('----------------INITIATED------------------')
def get_ip_from_subnet(ip_subnet):
    ips= ipaddress.ip_network(ip_subnet)
    ip_list = [f'http://{str(ip)}' for ip in ips]
    return ip_list


ip_subnet= "192.168.0.0/16"
url_list = get_ip_from_subnet(ip_subnet)


def ping_private_ip(url):
    try:
        print('REquest', url)
        r = requests.get(url, timeout=2)
        if r.ok:
            print(f'{url} is getting connected to private net')
    except:
        pass

processes = []
with ThreadPoolExecutor(max_workers=10000) as executor:
    for url in url_list:
        processes.append(executor.submit(ping_private_ip, url))

print('----------ENDED---------------')
# for task in as_completed(processes):
#     pass
