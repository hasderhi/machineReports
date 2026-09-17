import psutil

def get_disk_partitions_info() -> str:
    partitions = psutil.disk_partitions()
    output = []
    for part in partitions:
        output.append(
            # Lazy
            f"Device: {part.device}\n"
            f"        Mountpoint: {part.mountpoint}\n"
            f"        Filesystem type: {part.fstype}\n"
            f"        Options: {part.opts}\n"
        )
    return "\n".join(output)