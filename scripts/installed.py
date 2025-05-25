import os
if os.name == "nt":
    import winreg

def list_software():
    if os.name == "nt":
        software = []
        reg = winreg.ConnectRegistry(None, winreg.HKEY_LOCAL_MACHINE)
        key = winreg.OpenKey(reg, r"SOFTWARE\Microsoft\Windows\CurrentVersion\Uninstall")

        for i in range(winreg.QueryInfoKey(key)[0]):
            software_key_name = winreg.EnumKey(key, i)
            software_key = winreg.OpenKey(key, software_key_name)
            try:
                software_name = winreg.QueryValueEx(software_key, "DisplayName")[0]
                software.append(f"{software_name}")
            except Exception as e:
                pass
        return '\n    '.join(map(str, sorted(software)))
    else:
        return "This option is only available under Windows."