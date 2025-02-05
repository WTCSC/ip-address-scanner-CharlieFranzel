import argparse
import socket

host = '10.103.0.70'

parser = argparse.ArgumentParser()
parser.add_argument("-p", "--ports", type=str, default="Unknown")  # Optional argument with default
args = parser.parse_args()

def check_port(host, port):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
        sock.settimeout(1)  # Set timeout to 1 second
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

for port in get_port_list(args.ports):
    if check_port(host, port):
        print(f"  - Port {port}   (OPEN - {port})")    