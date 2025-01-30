import os
import os
import platform

input = "192.168.56.0/24"
range = 2**(32-(int(input.split('/')[1])))-2



def ping(ip):
    if platform.system().lower() == "windows":
        response = os.system(f"ping -n 4 {ip} >nul 2>&1")
    else:
        response = os.system(f"ping -c 4 {ip} >/dev/null 2>&1")
    return response
while range > 0:
    if ping(current_ip) == 0:
        print(range)
    else:
        print("not reachable")