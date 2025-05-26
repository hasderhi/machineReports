import subprocess

def get_java_status():
    try:
        result = subprocess.run(
            ["java", "-version"],
            capture_output=True, text=True, check=True
        )
        output = result.stderr.strip()  # Go home, Java, you're drunk - Why do you use stderr, not stdout?
        return "        " + output.replace('\n', '\n        ')
    except subprocess.CalledProcessError as e:
        return f"        Error checking Java status: {e}"
    except FileNotFoundError:
        return "        Java is not installed or not in PATH."
    except Exception as e:
        return f"        Unexpected error: {e}"