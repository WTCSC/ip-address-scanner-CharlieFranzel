import os
import os
import platform
import ipaddress

net = "192.168.1.0/24"

usable_ips = [str(ip) for ip in ipaddress.ip_network(net, strict=False).hosts()]


def ping(ip):
    if platform.system().lower() == "windows":
        response = os.system(f"ping -n 1 {ip} >nul 2>&1")
    else:
        response = os.system(f"ping -c 1 {ip} >/dev/null 2>&1")
    return response

for current_ip in usable_ips:
    if ping(current_ip) == 0:
        print(f"{current_ip}   - UP   ()")
    else:
        print(f"{current_ip}   - DOWN   (No Response)")
