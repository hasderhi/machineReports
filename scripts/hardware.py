import psutil
import time

def get_battery_status():
    battery = psutil.sensors_battery()
    if battery is None:
        return "Battery info not available"
    if battery.power_plugged:
        time_left = "/"
    else:
        if battery.secsleft == psutil.POWER_TIME_UNKNOWN:
            time_left = "Unknown"
        elif battery.secsleft == psutil.POWER_TIME_UNLIMITED:
            time_left = "Unlimited"
        else:
            time_left = time.strftime("%H:%M:%S", time.gmtime(battery.secsleft))


    return f"""Percent: {battery.percent}
        Plugged in: {battery.power_plugged}
        Time left: {time_left}"""
    