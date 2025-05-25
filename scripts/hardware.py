import psutil

def get_battery_status():
    battery = psutil.sensors_battery()
    if battery is None:
        return "Battery info not available"
    if battery.power_plugged:
        time_left = "/"
    else:
        time_left = battery.secsleft

    return f"""Percent: {battery.percent}
    Plugged in: {battery.power_plugged}
    Time left: {time_left}"""
    