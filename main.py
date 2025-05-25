try:
    from colors import bcolors
    from scripts import disk
    from scripts import admin
    from scripts import installed
    from scripts import packages
    from scripts import gitinfo
    from scripts import shell
    from scripts import internet
    from scripts import hardware
    from scripts import configfiles
    from scripts import pmanagers
    from scripts import nodenpm
except ImportError:
    print("Warning! Internal imports could not be resolved! Please reinstall the repository!")
    exit(1)

try:
    import platform
    import psutil
    import socket
    import re
    import uuid
    import os
    import sys
    import time
    import datetime
    import shutil
    import subprocess
    import pkg_resources
    import shellingham
except Exception as e:
    print(f"Warning! External dependency import failed! Please check if all dependencies are installed! Error: {e}")
    exit()

print(bcolors.OKCYAN + """machineReports by tk_dev
    
Developer: https://tk-dev-software.com
Support: https://tk-dev-software.com/appsupport
""" + bcolors.ENDC)

input(bcolors.OKBLUE + "Press any key to create a report..." + bcolors.ENDC)
date = datetime.datetime.now()

filename = f"mReport_{date.strftime("%d")}_{date.strftime("%m")}_{date.strftime("%Y")}"

print(bcolors.WARNING + f"Creating report {filename}..." + bcolors.ENDC)



with open(f"{filename}.txt", "w") as w:
    w.write(f"""--- machineReports by tk_dev---
    
Report created on {datetime.datetime.now()}

Developer: https://tk-dev-software.com
Support: https://tk-dev-software.com/appsupport
            
-- System overview --
    Machine: {platform.machine()}
    Version: {platform.version()}
    Platform: {platform.platform()}
    Hostname: {socket.gethostname()}
    System: {platform.system()}
    Processor: {platform.processor()}
    RAM: {str(round(psutil.virtual_memory().total / (1024.0 **3)))+" GB"}
    {disk.get_diskinfo()}
    System timezone: {time.tzname}
    System time: {datetime.datetime.now()}
    Uptime: {time.time() - psutil.boot_time()} seconds

-- Battery --
    {hardware.get_battery_status()}

-- Connectivity --
    Online: {internet.internet()}
    IP Address: {socket.gethostbyname(socket.gethostname())}
    MAC Address: {':'.join(re.findall('..', '%012x' % uuid.getnode()))}
    Firewall: \n{internet.get_firewall_status()}

-- User Information --
    Username: {os.getlogin()}
    User directory: {os.path.expanduser('~')}
    Program ran by administrator: {admin.check()}

-- Default shell --
    {shell.get_shell()}

-- Environment variables --
    {os.environ}

-- Config files --
    {configfiles.find_config_files()}

-- Installed Software --
    {installed.list_software()}

-- Python --
    Version: {sys.version}
    Path: {sys.path}

-- Package managers --
    {pmanagers.get_package_managers()}

-- Node/NPM -- 
    Node.js version: {nodenpm.get_node_and_npm_versions()["node_version"] or "Not installed"}
    npm version: {nodenpm.get_node_and_npm_versions()["npm_version"] or "Not installed"}

-- Installed pip packages --
    {packages.list_packages()}

-- Git --
    {gitinfo.get_git_info()}
""")
print(bcolors.OKGREEN + "Report created successfully!" + bcolors.ENDC)
input(bcolors.OKBLUE + "Press any key to exit..." + bcolors.ENDC)