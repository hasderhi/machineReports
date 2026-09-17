import locale
import platform
import ctypes
import winreg
import subprocess
import os



def get_keyboard_layout():
    system = platform.system()
    if system == "Windows":
        return get_keyboard_layout_windows()
    elif system == "Darwin":
        return get_keyboard_layout_macos()
    elif system == "Linux":
        return get_keyboard_layout_linux()
    else:
        return "Unsupported platform for keyboard layout detection"


def get_system_locale():
    lang, encoding = locale.getlocale()
    return f"{lang or 'Unknown'} / {encoding or 'Unknown'}"



def get_keyboard_layout_windows():
    try:
        user32 = ctypes.WinDLL('user32', use_last_error=True)
        layout_id = user32.GetKeyboardLayout(0) & (2**16 - 1)
        with winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE,
                            r"SYSTEM\CurrentControlSet\Control\Keyboard Layouts") as layouts_key:
            index = 0
            while True:
                try:
                    subkey_name = winreg.EnumKey(layouts_key, index)
                    if int(subkey_name, 16) == layout_id:
                        with winreg.OpenKey(layouts_key, subkey_name) as layout_key:
                            layout_text = winreg.QueryValueEx(layout_key, "Layout Text")[0]
                            return f"{layout_text} ({subkey_name})"
                    index += 1
                except OSError:
                    break
        return f"Unknown ({hex(layout_id)})"
    except Exception as e:
        return f"Failed to get keyboard layout: {e}"




def get_keyboard_layout_macos():
    try:
        result = subprocess.run(
            ["defaults", "read", "~/Library/Preferences/com.apple.HIToolbox.plist", "AppleSelectedInputSources"],
            capture_output=True, text=True, shell=True
        )
        return f"{result.stdout.strip() or 'Unknown'}"
    except Exception as e:
        return f"Failed to get keyboard layout on macOS: {e}"




def get_keyboard_layout_linux():
    try:
        result = subprocess.run(["localectl", "status"], capture_output=True, text=True)
        for line in result.stdout.splitlines():
            if "Layout" in line:
                return f"        {line.strip()}"
        return "Unknown"
    except Exception:
        # Fallback to /etc/default/keyboard because some distros are weird
        try:
            if os.path.exists("/etc/default/keyboard"):
                with open("/etc/default/keyboard") as f:
                    for line in f:
                        if line.startswith("XKBLAYOUT"):
                            layout = line.strip().split("=")[1].strip('"')
                            return f"{layout}"
        except Exception as e:
            return f"        Failed to get keyboard layout on Linux: {e}"
    return "Unknown"


