import platform
import ipaddress
import subprocess
import re
import argparse
import socket

parser = argparse.ArgumentParser()
parser.add_argument("-p", "--ports", type=str, default="Unknown")  # Optional argument with default
parser.add_argument("network", type=str)
args = parser.parse_args()


net = args.network
usable_ips = [str(ip) for ip in ipaddress.ip_network(net, strict=False).hosts()] # Makes a list of usable ips

def ping(ip):
    system = platform.system().lower()
    
    if system == "windows": # Command is slightly different on windows and unix based systems so based on the system it uses a different command
        cmd = ["ping", "-n", "1", ip]
        timeout_msg = "Request timed out."
    else:  # By default the device is eached pinged once. Increaseing this number may give more accurate results but will slow down the program
        cmd = ["ping", "-c", "1", ip]
        timeout_msg = "Request timed out." 
    
    try:
        output = subprocess.run(cmd, capture_output=True, text=True).stdout

        # Check for timeout message
        if timeout_msg in output:
            return "Timed Out"

        match = re.search(r"time[=<]([\d.]+) ?ms", output) # Extract ping time

        if match:
            return f"{match.group(1)} ms"  # Return ping time
    except Exception:
        pass

    return "No Response"  # If it doesn't respond return no response

def check_port(host, port):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
        sock.settimeout(.5)  # Set timeout time for each port check, increasing can improve accuracy however decreasing increases speed
        result = sock.connect_ex((host, port))
        return result == 0

def get_port_list(ports):
    if ',' in ports:
        portlist = []
        strlist = ports.split(',')
        for port in strlist:
            portlist.append(int(port))
    elif '-' in ports:
        pmin = int(ports.split('-')[0])
        pmax = int(ports.split('-')[1])+1
        portlist = list(range(pmin, pmax))
    elif ports.isdigit():
        ports = int(ports)
        portlist = [ports]
    else:
        print("Error: Invalid argument")
    return portlist

print(f"Scanning Network {net}") # Marks the beginning of output
for current_ip in usable_ips:
    ping_result = ping(current_ip) # Calls the ping function to ping each network throughout the loop
    
    if ping_result == "No Response": 
        print(f"{current_ip}   - DOWN ({ping_result})")
    if "ms" in ping_result: # If ms is in the result then print out the time it took and UP
        print(f"{current_ip}   - UP ({ping_result})")
        if args.ports is not None:
            for port in get_port_list(args.ports):
                if check_port(current_ip, port):
                    print(f"  - Port {port}   (OPEN - {port})")  
    if ping_result == "Timed Out": # If the connection times out instead of just not returning, gives an error
        print(f"{current_ip}   - ERROR ({ping_result})")
print("Scan Complete")