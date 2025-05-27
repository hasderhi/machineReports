import subprocess
import platform
import re

def get_wsl_info():
    if platform.system() != "Windows":
        return "        WSL is only available on Windows."

    try:
        result = subprocess.run(
            ["wsl", "--list", "--verbose"],
            capture_output=True,
            text=True,
            check=True
        )
        # Remove any ANSI escape sequences or problematic characters
        raw_output = result.stdout
        cleaned_output = re.sub(r'[^\x20-\x7E\n\r\t]', '', raw_output)  # Keep printable ASCII + control chars

        lines = cleaned_output.strip().splitlines()
        if len(lines) <= 1:
            return "        No WSL distros found."

        output = "        Installed WSL Distros:\n"
        for line in lines[1:]:
            output += f"        > {line.strip()}\n"
        return output.strip()

    except subprocess.CalledProcessError as e:
        return f"        Failed to list WSL distros: {e}"
    except FileNotFoundError:
        return "        WSL not found (is it installed?)"
