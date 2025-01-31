IPFreely

This project is a scanner to check the status of all devices on a given netowork
Pings each device individually and outputs what the result of the ping is

Takes the input and creates a list of all the usable IPs in that range
Uses that list and runs through it using a ping function that checks the OS type for the right command
Prints the result of each ping and the address name
Uses subprocess as well to get the ping time in ms

EXAMPLE USE:
Input: 
10.103.0.70/23
Output:
Scanning Network 10.103.0.70/23
10.103.0.1   - DOWN (No Response)
10.103.0.2   - DOWN (No Response)
...
10.103.0.67   - DOWN (No Response)
10.103.0.68   - UP (1 ms)
10.103.0.69   - DOWN (No Response)
10.103.0.70   - UP (1 ms)
10.103.0.71   - DOWN (No Response)
10.103.0.72   - ERROR (Timed Out)