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
    from scripts import envvars
    from scripts import bus
    from scripts import processes
    from scripts import mountedd
    from scripts import antivirus_state
    from scripts import java
    from scripts import vm_detect
    from scripts import ports
    from scripts import locale_keyboard
    from scripts import wsl
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
    import locale
    import winreg
    import ctypes
except Exception as e:
    print(f"Warning! External dependency import failed! Please check if all dependencies are installed! Error: {e}")
    exit()



def write_head(filename):
    return f"""<!--This file has been automatically created by machineReports, a tk_dev application: 
https://tk-dev-software.com -->
<!DOCTYPE html>
<html lang="en">
  <head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{filename}.html</title>
    <link rel="preconnect" href="https://fonts.googleapis.com">
    <link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;600;700&display=swap" rel="stylesheet">
    <style>{write_styles()}</style>
</head>
"""

def write_styles():
    return """
body {
margin: 0;
padding: 0;
background-color: #E7ECFF;
font-family: 'Inter', sans-serif;
color: #333;
}

.main-container {
background-color: #ffffff;
max-width: 800px;
margin: 40px auto;
padding: 40px;
border-radius: 16px;
box-shadow: 0 4px 20px rgba(0, 0, 0, 0.1);
}

.title {
text-align: center;
color: #2A2E45;
}

.title .subtitle {
display: block;
font-size: 18px;
font-weight: normal;
color: #5C6B95;
}

h2 {
margin-top: 40px;
font-size: 24px;
color: #3A3F66;
border-bottom: 2px solid #D1D8FF;
padding-bottom: 10px;
}

table {
width: 100%;
border-collapse: collapse;
margin-top: 20px;
background-color: #F8FAFF;
border-radius: 12px;
overflow: hidden;
}

th,
td {
text-align: left;
padding: 12px 16px;
}

th {
background-color: #E2E8FF;
color: #2A2E45;
font-weight: 600;
}

tr:nth-child(even) {
background-color: #F0F3FF;
}

tr:hover {
background-color: #DDE3FF;
}

.expandable {
margin-top: 30px;
}

.expand-button {
display: flex;
align-items: center;
background-color: #DDE3FF;
color: #2A2E45;
font-weight: 600;
padding: 12px 16px;
border: none;
border-radius: 10px;
cursor: pointer;
width: 100%;
font-size: 16px;
font-family: "Inter", sans-serif;
transition: background-color 0.2s;
}

.expand-button:hover {
background-color: #C8D1F5;
}

.expand-content {
display: none;
margin-top: 16px;
padding: 20px;
background-color: #F4F7FF;
border-radius: 10px;
white-space: pre-wrap;
font-family: monospace;
font-size: 14px;
}

.footer {
text-align: center;
margin-top: 10%;
}
"""

def write_script():
    return """
    // Very, very lazy solution, ever heard about arguments?
    // Yes, but it's 1AM, gonna fix this later!
    function toggleExpandFirewall() {
        const content = document.getElementById("firewallContent");
        if (content.style.display === "block") {
          content.style.display = "none";
        } else {
          content.style.display = "block";
        }
      }

      function toggleExpandEnvVars() {
        const content = document.getElementById("envVarContent");
        if (content.style.display === "block") {
          content.style.display = "none";
        } else {
          content.style.display = "block";
        }
      }

      function toggleExpandSoftware() {
        const content = document.getElementById("softwareContent");
        if (content.style.display === "block") {
          content.style.display = "none";
        } else {
          content.style.display = "block";
        }
      }

      function toggleExpandpip() {
        const content = document.getElementById("pipContent");
        if (content.style.display === "block") {
          content.style.display = "none";
        } else {
          content.style.display = "block";
        }
      }
      
      function toggleExpandProcesses() {
        const content = document.getElementById("processesContent");
        if (content.style.display === "block") {
          content.style.display = "none";
        } else {
          content.style.display = "block";
        }
      }

      function toggleExpandPorts() {
        const content = document.getElementById("portsContent");
        if (content.style.display === "block") {
          content.style.display = "none";
        } else {
          content.style.display = "block";
        }
      }
      """

def write_pypath():
    return sys.path


def write_config_files():
    return configfiles.find_config_files()

def write_body():
    return f"""<body>
    <div class="main-container">
      <h1 class="title">
        machineReports <span class="subtitle">by tk_dev</span>
      </h1>
      <h2>Report details</h2>
      <table>
        <tr>
          <th>Generated by machineReports on <i>{datetime.datetime.now()}</i>
          </th>
        </tr>
        <tr>
          <th>
            <a href="https://tk-dev-software.com">Developer</a>
          </th>
        </tr>
        <tr>
          <th>
            <a href="https://tk-dev-software.com/appsupport">Support</a>
          </th>
        </tr>
      </table>
      <h2>System Overview</h2>
      <table>
        <tr>
          <th>Property</th>
          <th>Value</th>
        </tr>
        <tr>
          <td>Machine</td>
          <td>{platform.machine()}</td>
        </tr>
        <tr>
          <td>Version</td>
          <td>{platform.version()}</td>
        </tr>
        <tr>
          <td>Platform</td>
          <td>{platform.platform()}</td>
        </tr>
        <tr>
          <td>Hostname</td>
          <td>{socket.gethostname()}</td>
        </tr>
        <tr>
          <td>System</td>
          <td>{platform.system()}</td>
        </tr>
        <tr>
          <td>Processor</td>
          <td>{platform.processor()}</td>
        </tr>
        <tr>
          <td>RAM</td>
          <td>{str(round(psutil.virtual_memory().total / (1024.0 **3)))+" GB"}</td>
        </tr>
        <tr>
          <td>Drive Status</td>
          <td>{disk.get_diskinfo()}</td>
        </tr>
        <tr>
          <td>Timezone</td>
          <td>{time.tzname}</td>
        </tr>
        <tr>
          <td>System Time</td>
          <td>{datetime.datetime.now()}</td>
        </tr>
        <tr>
          <td>Uptime</td>
          <td>{time.time() - psutil.boot_time()} seconds</td>
        </tr>
        <tr>
          <td>VM Detected</td>
          <td>{vm_detect.detect_vm()}</td>
        </tr>
      </table>

      <h2>Battery</h2>
      <table>
        <tr>
          <th>Property</th>
          <th>Value</th>
        </tr>
        <tr>
          <td>Battery Status</td>
          <td>{hardware.get_battery_status()}</td>
        </tr>
      </table>

      <h2>Connectivity</h2>
      <table>
        <tr>
          <th>Property</th>
          <th>Value</th>
        </tr>
        <tr>
          <td>Online</td>
          <td>{internet.internet()}</td>
        </tr>
        <tr>
          <td>IP Address</td>
          <td>{socket.gethostbyname(socket.gethostname())}</td>
        </tr>
        <tr>
          <td>MAC Address</td>
          <td>{':'.join(re.findall('..', '%012x' % uuid.getnode()))}</td>
        </tr>
      </table>

      <h2>Open connections</h2>
      <div class="expandable">
        <button class="expand-button" onclick="toggleExpandPorts()">Expand</button>
            <div class="expand-content" id="portsContent">
                {ports.get_net_connections()}
            </div>
      </div>

      <h2>Mounted disks</h2>
      <table>
        <tr>
          <th>Value</th>
        </tr>
        <tr>
          <td>{mountedd.get_disk_partitions_info()}</td>
        </tr>
      </table>

      <h2>USB devices</h2>
      <table>
        <tr>
          <th>Value</th>
        </tr>
        <tr>
          <td>{bus.list_usb_devices()}</td>
        </tr>
      </table>

      <h2>Firewall</h2>
      <div class="expandable">
        <button class="expand-button" onclick="toggleExpandFirewall()">Expand</button>
            <div class="expand-content" id="firewallContent">
                {internet.get_firewall_status()}
            </div>
      </div>

      <h2>User Information</h2>
      <table>
        <tr>
          <th>Property</th>
          <th>Value</th>
        </tr>
        <tr>
          <td>Username</td>
          <td>{os.getlogin()}</td>
        </tr>
        <tr>
          <td>User directory</td>
          <td>{os.path.expanduser('~')}</td>
        </tr>
        <tr>
          <td>Program ran by administrator</td>
          <td>{admin.check()}</td>
        </tr>
      </table>

      <h2>Antivirus state</h2>
      <table>
        <tr>
          <th>Value</th>
        </tr>
        <tr>
          <td>{antivirus_state.get_antivirus_status()}</td>
        </tr>
      </table>

      <h2>Running processes</h2>
      <div class="expandable">
        <button class="expand-button" onclick="toggleExpandProcesses()">Expand</button>
        <div class="expand-content" id="processesContent">{processes.get_process_info()}</div>
      </div>

      <h2>Default shell</h2>
      <table>
        <tr>
          <th>Value</th>
        </tr>
        <tr>
          <td>{shell.get_shell()}</td>
        </tr>
      </table>

      <h2>WSL (Windows Subsystem for Linux)</h2>
      <table>
        <tr>
          <th>Value</th>
        </tr>
        <tr>
          <td>{wsl.get_wsl_info()}</td>
        </tr>
      </table>

      <h2>Environment variables</h2>
      <div class="expandable">
        <button class="expand-button" onclick="toggleExpandEnvVars()">Expand</button>
        <div class="expand-content" id="envVarContent">{envvars.get_envvars()}</div>
      </div>

      <h2>Config files</h2>
      <table>
        <tr>
          <th>Value</th>
        </tr>
        <tr>
          <td>{write_config_files()}</td>
        </tr>
      </table>

      <h2>Installed Software</h2>
      <div class="expandable">
        <button class="expand-button" onclick="toggleExpandSoftware()">Expand</button>
        <div class="expand-content" id="softwareContent">{installed.list_software()}</div>
      </div>

      <h2>Python</h2>
      <table>
        <tr>
          <th>Property</th>
          <th>Value</th>
        </tr>
        <tr>
          <td>Version</td>
          <td>{sys.version}</td>
        </tr>
        <tr>
          <td>Path</td>
          <td>{write_pypath()}</td>
        </tr>
      </table>

      <h2>Package managers</h2>
      <table>
        <tr>
          <th>Value</th>
        </tr>
        <tr>
          <td>{pmanagers.get_package_managers()}</td>
        </tr>
      </table>

      <h2>Node.js / NPM</h2>
      <table>
        <tr>
          <th>Property</th>
          <th>Value</th>
        </tr>
        <tr>
          <td>Node.js version</td>
          <td>{nodenpm.get_node_and_npm_versions()["node_version"] or "Not installed"}</td>
        </tr>
        <tr>
          <td>npm version</td>
          <td>{nodenpm.get_node_and_npm_versions()["npm_version"] or "Not installed"}</td>
        </tr>
      </table>

      <h2>Java</h2>
      <table>
        <tr>
          <th>Value</th>
        </tr>
        <tr>
          <td>{java.get_java_status()}</td>
        </tr>
      </table>

      <h2>Installed pip packages</h2>
      <div class="expandable">
        <button class="expand-button" onclick="toggleExpandpip()">Expand</button>
        <div class="expand-content" id="pipContent">{packages.list_packages()}</div>
      </div>
      <h2>Git</h2>
      <table>
        <tr>
          <th>Value</th>
        </tr>
        <tr>
          <td>{gitinfo.get_git_info()}</td>
        </tr>
      </table>

      <p class="footer">Auto-generated by machineReports, a <a href="https://tk-dev-software.com">tk_dev</a> application. <a href="https://github.com/hasderhi/machineReports">GitHub page</a></p>

    </div>
    <script>
      {write_script()}
    </script>
    </div>
  </body>
</html>
"""







print(bcolors.OKCYAN + """machineReports by tk_dev
    
Developer: https://tk-dev-software.com
Support: https://tk-dev-software.com/appsupport
""" + bcolors.ENDC)

answer = input(bcolors.OKBLUE + "Press 'H' to create report as HTML, press any other key to create as text..." + bcolors.ENDC)
if answer.lower() == "h":
    date = datetime.datetime.now()
    filename = f"mReport_{date.strftime("%d")}_{date.strftime("%m")}_{date.strftime("%Y")}"

    print(bcolors.WARNING + f"Creating report {filename}.html" + bcolors.ENDC)
    with open(f"output/{filename}.html", "w") as w:
        w.write(write_head(filename))
        w.write(write_body())
else:

    date = datetime.datetime.now()

    filename = f"mReport_{date.strftime("%d")}_{date.strftime("%m")}_{date.strftime("%Y")}"

    print(bcolors.WARNING + f"Creating report {filename}.txt" + bcolors.ENDC)



    with open(f"output/{filename}.txt", "w", encoding="utf-8") as w:
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
        Language/Encoding: {locale_keyboard.get_system_locale()}
        Keyboard layout: {locale_keyboard.get_keyboard_layout()}
        Uptime: {time.time() - psutil.boot_time()} seconds
        VM detected: {vm_detect.detect_vm()}

    -- Mounted disks --
       {mountedd.get_disk_partitions_info()}

    -- Battery --
        {hardware.get_battery_status()}

    -- Connectivity --
        Online: {internet.internet()}
        IP Address: {socket.gethostbyname(socket.gethostname())}
        MAC Address: {':'.join(re.findall('..', '%012x' % uuid.getnode()))}
        Firewall: \n{internet.get_firewall_status()}

    -- Open connections --
{ports.get_net_connections()}

    -- USB Devices --
        {bus.list_usb_devices()}

    -- User Information --
        Username: {os.getlogin()}
        User directory: {os.path.expanduser('~')}
        Program ran by administrator: {admin.check()}

    -- Running processes --
        {processes.get_process_info()}    

    -- Default shell --
        {shell.get_shell()}

    -- WSL (Windows Subsystem for Linux) --
        {wsl.get_wsl_info()}

    -- Antivirus status --
        {antivirus_state.get_antivirus_status()}

    -- Environment variables --
        {envvars.get_envvars()}

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

    -- Java Status --
{java.get_java_status()}

    -- Installed pip packages --
        {packages.list_packages()}

    -- Git --
        {gitinfo.get_git_info()}
    """)
print(bcolors.OKGREEN + "Report created successfully!" + bcolors.ENDC)
input(bcolors.OKBLUE + "Press any key to exit..." + bcolors.ENDC)


