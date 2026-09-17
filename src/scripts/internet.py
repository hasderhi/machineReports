import socket
import subprocess
import os

def internet(host="8.8.8.8", port=53, timeout=3):
    """
    Host: 8.8.8.8 (google-public-dns-a.google.com)
    OpenPort: 53/tcp
    Service: domain (DNS/TCP)
    """
    try:
        socket.setdefaulttimeout(timeout)
        socket.socket(socket.AF_INET, socket.SOCK_STREAM).connect((host, port))
        return True
    except socket.error as ex:
        return f"Connection failed: {ex}"
    
def get_firewall_status():
    if os.name == "nt":
        try:
            result = subprocess.run(
                ["netsh", "advfirewall", "show", "allprofiles"],
                check=True,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True
            )
            # Add 4 spaces before each line
            indented_output = '\n'.join('        ' + line for line in result.stdout.strip().splitlines())
            return indented_output
        except subprocess.CalledProcessError as e:
            return f"Error: {e.stderr.strip()}"
    else:
        return "This option is only available under Windows."