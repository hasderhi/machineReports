import psutil

def get_process_info() -> str:
    output = []
    for proc in psutil.process_iter(['pid', 'name', 'username']):
        try:
            info = proc.info
            name = info.get('name', 'Unknown')
            pid = info.get('pid', 'N/A')
            username = info.get('username', 'N/A')
            output.append(f"Name: {name} > PID: {pid} > Username: {username}")
        except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
            continue
    return '\n        '.join(output)