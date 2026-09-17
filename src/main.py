"""
machineReports by tk_dev
https://tk-dev-software.com

Collects a snapshot of the current machine (hardware, network, software,
environment, processes, etc.) and writes it out as either an HTML report
or a plain-text report.
"""

from __future__ import annotations

import argparse
import datetime as dt
import getpass
import logging
import platform
import re
import socket
import sys
import time
import uuid
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any

try:
    import psutil
except ImportError as exc: # pragma: no cover
    print(f"Warning! External dependency import failed: {exc}")
    sys.exit(1)

try:
    from colors import bcolors
    from scripts import (
        admin,
        antivirus_state,
        bus,
        configfiles,
        disk,
        envvars,
        gitinfo,
        hardware,
        installed,
        internet,
        java,
        locale_keyboard,
        mountedd,
        nodenpm,
        packages,
        pmanagers,
        ports,
        processes,
        shell,
        vm_detect,
        wsl,
    )
except ImportError as exc:
    print(f"Warning! Internal imports could not be resolved: {exc}")
    print("Please reinstall the repository!")
    sys.exit(1)


log = logging.getLogger("machineReports")

APP_NAME = "machineReports"
APP_URL = "https://tk-dev-software.com"
SUPPORT_URL = "https://tk-dev-software.com/appsupport"
GITHUB_URL = "https://github.com/hasderhi/machineReports"

OUTPUT_DIR = Path("output")





@dataclass
class ReportData:
    generated_at: dt.datetime = field(default_factory=dt.datetime.now)

    # System overview
    machine: str = field(default_factory=platform.machine)
    version: str = field(default_factory=platform.version)
    platform_str: str = field(default_factory=platform.platform)
    hostname: str = field(default_factory=socket.gethostname)
    system: str = field(default_factory=platform.system)
    processor: str = field(default_factory=platform.processor)
    ram_gb: int = 0
    disk_info: str = ""
    timezone: tuple = field(default_factory=lambda: time.tzname)
    uptime_seconds: float = 0.0
    vm_detected: str = ""
    locale_info: str = ""
    keyboard_layout: str = ""

    # Battery
    battery_status: str = ""

    # Connectivity
    online: bool = False
    ip_address: str = ""
    mac_address: str = ""
    firewall_status: str = ""
    open_connections: str = ""

    # Disks / USB
    mounted_disks: str = ""
    usb_devices: str = ""

    # User
    username: str = ""
    home_dir: str = ""
    is_admin: bool = False

    # Software / processes
    antivirus: str = ""
    processes_info: str = ""
    default_shell: str = ""
    wsl_info: str = ""
    env_vars: str = ""
    config_files: Any = None
    installed_software: Any = None

    # Python / package managers / runtimes
    python_version: str = field(default_factory=lambda: sys.version)
    python_path: list[str] = field(default_factory=lambda: list(sys.path))
    package_managers: Any = None
    node_version: str = "Not installed"
    npm_version: str = "Not installed"
    java_status: str = ""
    pip_packages: Any = None
    git_info: str = ""

    @classmethod
    def gather(cls) -> "ReportData":
        log.info("Gathering system information...")
        data = cls()

        data.ram_gb = round(psutil.virtual_memory().total / (1024.0 ** 3))
        data.disk_info = disk.get_diskinfo()
        data.uptime_seconds = time.time() - psutil.boot_time()
        data.vm_detected = vm_detect.detect_vm()
        data.locale_info = locale_keyboard.get_system_locale()
        data.keyboard_layout = locale_keyboard.get_keyboard_layout()

        data.battery_status = hardware.get_battery_status()

        data.online = internet.internet()
        data.ip_address = socket.gethostbyname(socket.gethostname())
        data.mac_address = ":".join(re.findall("..", "%012x" % uuid.getnode()))
        data.firewall_status = internet.get_firewall_status()
        data.open_connections = ports.get_net_connections()

        data.mounted_disks = mountedd.get_disk_partitions_info()
        data.usb_devices = bus.list_usb_devices()

        data.username = getpass.getuser()
        data.home_dir = str(Path.home())
        data.is_admin = admin.check()

        data.antivirus = antivirus_state.get_antivirus_status()
        data.processes_info = processes.get_process_info()
        data.default_shell = shell.get_shell()
        data.wsl_info = wsl.get_wsl_info()
        data.env_vars = envvars.get_envvars()
        data.config_files = configfiles.find_config_files()
        data.installed_software = installed.list_software()

        data.package_managers = pmanagers.get_package_managers()

        node_npm = nodenpm.get_node_and_npm_versions()
        data.node_version = node_npm.get("node_version") or "Not installed"
        data.npm_version = node_npm.get("npm_version") or "Not installed"

        data.java_status = java.get_java_status()
        data.pip_packages = packages.list_packages()
        data.git_info = gitinfo.get_git_info()

        log.info("Done gathering system information.")
        return data



HTML_STYLES = """
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

HTML_JS = """
function toggleExpand(id) {
  const content = document.getElementById(id);
  content.style.display = content.style.display === "block" ? "none" : "block";
}
"""


def render_html_head(filename: str) -> str:
    return f"""<!--This file has been automatically created by {APP_NAME}, a tk_dev application:
{APP_URL} -->
<!DOCTYPE html>
<html lang="en">
  <head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{filename}.html</title>
    <link rel="preconnect" href="https://fonts.googleapis.com">
    <link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;600;700&display=swap" rel="stylesheet">
    <style>{HTML_STYLES}</style>
</head>
"""

def _expandable(title: str, content_id: str, content: Any) -> str:
    return f"""
      <h2>{title}</h2>
      <div class="expandable">
        <button class="expand-button" onclick="toggleExpand('{content_id}')">Expand</button>
        <div class="expand-content" id="{content_id}">{content}</div>
      </div>
"""

def render_html_body(data: ReportData) -> str:
    return f"""<body>
    <div class="main-container">
      <h1 class="title">
        {APP_NAME} <span class="subtitle">by tk_dev</span>
      </h1>

      <h2>Report details</h2>
      <table>
        <tr><th>Generated on <i>{data.generated_at}</i></th></tr>
        <tr><th><a href="{APP_URL}">Developer</a></th></tr>
        <tr><th><a href="{SUPPORT_URL}">Support</a></th></tr>
      </table>

      <h2>System Overview</h2>
      <table>
        <tr><th>Property</th><th>Value</th></tr>
        <tr><td>Machine</td><td>{data.machine}</td></tr>
        <tr><td>Version</td><td>{data.version}</td></tr>
        <tr><td>Platform</td><td>{data.platform_str}</td></tr>
        <tr><td>Hostname</td><td>{data.hostname}</td></tr>
        <tr><td>System</td><td>{data.system}</td></tr>
        <tr><td>Processor</td><td>{data.processor}</td></tr>
        <tr><td>RAM</td><td>{data.ram_gb} GB</td></tr>
        <tr><td>Drive Status</td><td>{data.disk_info}</td></tr>
        <tr><td>Timezone</td><td>{data.timezone}</td></tr>
        <tr><td>Uptime</td><td>{data.uptime_seconds} seconds</td></tr>
        <tr><td>VM Detected</td><td>{data.vm_detected}</td></tr>
        <tr><td>Language/Encoding</td><td>{data.locale_info}</td></tr>
        <tr><td>Keyboard layout</td><td>{data.keyboard_layout}</td></tr>
      </table>

      <h2>Battery</h2>
      <table>
        <tr><th>Property</th><th>Value</th></tr>
        <tr><td>Battery Status</td><td>{data.battery_status}</td></tr>
      </table>

      <h2>Connectivity</h2>
      <table>
        <tr><th>Property</th><th>Value</th></tr>
        <tr><td>Online</td><td>{data.online}</td></tr>
        <tr><td>IP Address</td><td>{data.ip_address}</td></tr>
        <tr><td>MAC Address</td><td>{data.mac_address}</td></tr>
      </table>

      {_expandable("Open connections", "portsContent", data.open_connections)}

      <h2>Mounted disks</h2>
      <table><tr><th>Value</th></tr><tr><td>{data.mounted_disks}</td></tr></table>

      <h2>USB devices</h2>
      <table><tr><th>Value</th></tr><tr><td>{data.usb_devices}</td></tr></table>

      {_expandable("Firewall", "firewallContent", data.firewall_status)}

      <h2>User Information</h2>
      <table>
        <tr><th>Property</th><th>Value</th></tr>
        <tr><td>Username</td><td>{data.username}</td></tr>
        <tr><td>User directory</td><td>{data.home_dir}</td></tr>
        <tr><td>Program ran by administrator</td><td>{data.is_admin}</td></tr>
      </table>

      <h2>Antivirus state</h2>
      <table><tr><th>Value</th></tr><tr><td>{data.antivirus}</td></tr></table>

      {_expandable("Running processes", "processesContent", data.processes_info)}

      <h2>Default shell</h2>
      <table><tr><th>Value</th></tr><tr><td>{data.default_shell}</td></tr></table>

      <h2>WSL (Windows Subsystem for Linux)</h2>
      <table><tr><th>Value</th></tr><tr><td>{data.wsl_info}</td></tr></table>

      {_expandable("Environment variables", "envVarContent", data.env_vars)}

      <h2>Config files</h2>
      <table><tr><th>Value</th></tr><tr><td>{data.config_files}</td></tr></table>

      {_expandable("Installed Software", "softwareContent", data.installed_software)}

      <h2>Python</h2>
      <table>
        <tr><th>Property</th><th>Value</th></tr>
        <tr><td>Version</td><td>{data.python_version}</td></tr>
        <tr><td>Path</td><td>{data.python_path}</td></tr>
      </table>

      <h2>Package managers</h2>
      <table><tr><th>Value</th></tr><tr><td>{data.package_managers}</td></tr></table>

      <h2>Node.js / NPM</h2>
      <table>
        <tr><th>Property</th><th>Value</th></tr>
        <tr><td>Node.js version</td><td>{data.node_version}</td></tr>
        <tr><td>npm version</td><td>{data.npm_version}</td></tr>
      </table>

      <h2>Java</h2>
      <table><tr><th>Value</th></tr><tr><td>{data.java_status}</td></tr></table>

      {_expandable("Installed pip packages", "pipContent", data.pip_packages)}

      <h2>Git</h2>
      <table><tr><th>Value</th></tr><tr><td>{data.git_info}</td></tr></table>

      <p class="footer">
        Auto-generated by {APP_NAME}, a <a href="{APP_URL}">tk_dev</a> application.
        <a href="{GITHUB_URL}">GitHub page</a>
      </p>
    </div>
    <script>{HTML_JS}</script>
  </body>
</html>
"""

def render_html(filename: str, data: ReportData) -> str:
    return render_html_head(filename) + render_html_body(data)

def render_text(data: ReportData) -> str:
    return f"""--- {APP_NAME} by tk_dev ---

Report created on {data.generated_at}

Developer: {APP_URL}
Support: {SUPPORT_URL}

-- System overview --
    Machine: {data.machine}
    Version: {data.version}
    Platform: {data.platform_str}
    Hostname: {data.hostname}
    System: {data.system}
    Processor: {data.processor}
    RAM: {data.ram_gb} GB
    {data.disk_info}
    System timezone: {data.timezone}
    System time: {data.generated_at}
    Language/Encoding: {data.locale_info}
    Keyboard layout: {data.keyboard_layout}
    Uptime: {data.uptime_seconds} seconds
    VM detected: {data.vm_detected}

-- Mounted disks --
    {data.mounted_disks}

-- Battery --
    {data.battery_status}

-- Connectivity --
    Online: {data.online}
    IP Address: {data.ip_address}
    MAC Address: {data.mac_address}
    Firewall:
{data.firewall_status}

-- Open connections --
{data.open_connections}

-- USB Devices --
    {data.usb_devices}

-- User Information --
    Username: {data.username}
    User directory: {data.home_dir}
    Program ran by administrator: {data.is_admin}

-- Running processes --
    {data.processes_info}

-- Default shell --
    {data.default_shell}

-- WSL (Windows Subsystem for Linux) --
    {data.wsl_info}

-- Antivirus status --
    {data.antivirus}

-- Environment variables --
    {data.env_vars}

-- Config files --
    {data.config_files}

-- Installed Software --
    {data.installed_software}

-- Python --
    Version: {data.python_version}
    Path: {data.python_path}

-- Package managers --
    {data.package_managers}

-- Node/NPM --
    Node.js version: {data.node_version}
    npm version: {data.npm_version}

-- Java Status --
{data.java_status}

-- Installed pip packages --
    {data.pip_packages}

-- Git --
    {data.git_info}
"""

def make_filename(now: dt.datetime | None = None) -> str:
    now = now or dt.datetime.now()
    return f"mReport_{now:%d_%m_%Y}"

def write_report(fmt: str, output_dir: Path = OUTPUT_DIR) -> Path:
    output_dir.mkdir(parents=True, exist_ok=True)

    data = ReportData.gather()
    filename = make_filename(data.generated_at)

    if fmt == "html":
        out_path = output_dir / f"{filename}.html"
        content = render_html(filename, data)
    else:
        out_path = output_dir / f"{filename}.txt"
        content = render_text(data)

    log.info("Writing report to %s", out_path)
    out_path.write_text(content, encoding="utf-8")
    return out_path


def parse_args(argv: list[str] | None = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        prog=APP_NAME,
        description=f"{APP_NAME} by tk_dev - generates a machine information report.",
    )
    parser.add_argument(
        "-f", "--format",
        choices=["html", "text"],
        default=None,
        help="Report format to generate. If omitted, you will be prompted interactively.",
    )
    parser.add_argument(
        "-o", "--output-dir",
        type=Path,
        default=OUTPUT_DIR,
        help=f"Directory to write the report into (default: {OUTPUT_DIR}).",
    )
    parser.add_argument(
        "-q", "--quiet",
        action="store_true",
        help="Suppress banner/info logging (errors still shown).",
    )
    return parser.parse_args(argv)


def prompt_for_format() -> str:
    print(
        bcolors.OKCYAN
        + f"""{APP_NAME} by tk_dev

Developer: {APP_URL}
Support: {SUPPORT_URL}
"""
        + bcolors.ENDC
    )
    answer = input(
        bcolors.OKBLUE
        + "Press 'H' to create report as HTML, press any other key to create as text..."
        + bcolors.ENDC
    )
    return "html" if answer.strip().lower() == "h" else "text"


def main(argv: list[str] | None = None) -> int:
    args = parse_args(argv)

    logging.basicConfig(
        level=logging.WARNING if args.quiet else logging.INFO,
        format="%(message)s",
    )

    fmt = args.format or prompt_for_format()

    print(bcolors.WARNING + f"Creating {make_filename()}.{ 'html' if fmt == 'html' else 'txt' }" + bcolors.ENDC)
    try:
        out_path = write_report(fmt, args.output_dir)
    except Exception as exc:
        log.error("Failed to generate report: %s", exc)
        return 1

    print(bcolors.OKGREEN + f"Report created successfully at {out_path}!" + bcolors.ENDC)

    if args.format is None:
        input(bcolors.OKBLUE + "Press any key to exit..." + bcolors.ENDC)

    return 0

if __name__ == "__main__":
    sys.exit(main())