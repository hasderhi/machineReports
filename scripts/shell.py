import shellingham
import platform

def get_shell():
    try:
        return shellingham.detect_shell()
    except Exception:
        if platform.system().lower() == "windows":
            return ("cmd", "C:\\Windows\\System32\\cmd.exe")
        return ("unknown", None)
