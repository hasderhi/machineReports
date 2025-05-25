import shutil
import subprocess

def get_package_managers():
    package_managers = {
        "apt": ["apt", "--version"],
        "dnf": ["dnf", "--version"],
        "yum": ["yum", "--version"],
        "pacman": ["pacman", "--version"],
        "zypper": ["zypper", "--version"],
        "brew": ["brew", "--version"],
        "choco": ["choco", "--version"],
        "winget": ["winget", "--version"],
        "scoop": ["scoop", "--version"],
        "snap": ["snap", "--version"],
        "flatpak": ["flatpak", "--version"],
        "port": ["port", "version"],  # MacPorts
    }

    lines = []
    for name, cmd in package_managers.items():
        if shutil.which(cmd[0]):
            try:
                version = subprocess.check_output(cmd, stderr=subprocess.DEVNULL, text=True).splitlines()[0].strip()
                lines.append(f"{name}: Installed > {version}")
            except Exception:
                lines.append(f"{name}: Installed > Version info not found")
        else:
            lines.append(f"{name}: Not installed/available")

    return "\n    ".join(lines)