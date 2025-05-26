"""
IMPORTANT

This module is only checking the windows antivirus state and is not harming or interfering with the defending system
IN ANY WAY!

For absolute clarity, I have decided to document this script very exact. If you are still unsure, you can disable
the execution of this part of the program by changing this variable to "False":
"""

EXECUTE = True  #<<< Change this to False to disable this feature

import subprocess # Import module to run PowerShell commands
import os

def get_antivirus_status():
    if EXECUTE == True: # Run this ONLY IF EXECUTE is set to TRUE
        if os.name == "nt": # Run only under Windows (NT), as this won't work under Linux or macOS
            try:
                result = subprocess.run( # Run Powershell command to retrieve antivirus information 
                    ["powershell", "-Command", "Get-MpComputerStatus | Select-Object -Property AMServiceEnabled,AntispywareEnabled,AntivirusEnabled,RealTimeProtectionEnabled"],
                    capture_output=True, text=True, check=True # Retrieve output
                )
                lines = result.stdout.strip().splitlines() # Prepare output for display
                output = "\n        ".join(lines)
                return "        " + output # Return output to the main program
            except subprocess.CalledProcessError as e: # Except something went wrong
                return f"        Error checking Defender status: {e}"
        else:
            return f"        This option is only available under Windows."
    else:
        return f"        Disabled. If you want to check for antivirus status, go to 'scripts/antivirus_state.py' and enable the 'EXECUTE' variable."


