import psutil
import socket

def get_net_connections():
    connections = psutil.net_connections()
    lines = []
    for conn in connections:
        laddr = f"{conn.laddr.ip}:{conn.laddr.port}" if conn.laddr else "N/A"
        raddr = f"{conn.raddr.ip}:{conn.raddr.port}" if conn.raddr else "N/A"
        status = conn.status
        pid = conn.pid if conn.pid is not None else "N/A"
        try:
            proc = psutil.Process(conn.pid) if conn.pid else None
            pname = proc.name() if proc else "N/A"
        except (psutil.NoSuchProcess, psutil.AccessDenied):
            pname = "N/A"
        lines.append(
            f"        Process: {pname} (PID: {pid})\n"
            f"            Local Address: {laddr}\n"
            f"            Remote Address: {raddr}\n"
            f"            Status: {status}"
        )
    return "\n".join(lines) if lines else "        No active network connections found."