import shellingham

def get_shell():
    try:
        return shellingham.detect_shell()
    except shellingham.ShellDetectionFailure:
        return "Could not detect shell"