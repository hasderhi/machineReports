import psutil


def get_diskinfo():
    disk = psutil.disk_usage('/')

    output = f"""Total drive capacity: {round(disk.total / (2**30), 3)} GiB
    Used drive space: {round(disk.used / (2**30), 3)} GiB
    Free drive space: {round(disk.free / (2**30), 3)} GiB"""
    return output