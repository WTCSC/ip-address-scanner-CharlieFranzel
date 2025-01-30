import platform
import ipaddress
import subprocess
import re

net = "192.168.1.0/24"

usable_ips = [str(ip) for ip in ipaddress.ip_network(net, strict=False).hosts()]

def ping(ip):
    system = platform.system().lower()
    
    # Use appropriate ping command based on OS
    if system == "windows":
        cmd = ["ping", "-n", "1", ip]
        timeout_msg = "Request timed out."
    else:
        cmd = ["ping", "-c", "1", ip]
        timeout_msg = "100% packet loss" 
    
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

print(f"Scanning Network {net}")
for current_ip in usable_ips:
    ping_result = ping(current_ip)
    
    if ping_result == "No Response":
        print(f"{current_ip}   - DOWN ({ping_result})")
    if "ms" in ping_result:
        print(f"{current_ip}   - UP ({ping_result})")
    if ping_result == "Timed Out":
        print(f"{current_ip}   - ERROR ({ping_result})")
