import platform
import psutil
import shutil


def get_cpu_usage():
    usage = psutil.cpu_percent(interval=1)
    return f"CPU usage is {usage} percent."


def get_ram_usage():
    memory = psutil.virtual_memory()

    total = memory.total / (1024 ** 3)
    used = memory.used / (1024 ** 3)
    available = memory.available / (1024 ** 3)

    return (
        f"RAM usage is {memory.percent} percent. "
        f"{used:.2f} GB used out of {total:.2f} GB. "
        f"{available:.2f} GB available."
    )


def get_battery_status():
    battery = psutil.sensors_battery()

    if battery is None:
        return "Battery information is not available on this computer."

    percentage = battery.percent
    charging = battery.power_plugged

    status = "charging" if charging else "not charging"

    return f"Battery is at {percentage} percent and is {status}."


def get_disk_usage():
    disk = shutil.disk_usage("C:\\")

    total = disk.total / (1024 ** 3)
    used = disk.used / (1024 ** 3)
    free = disk.free / (1024 ** 3)

    return (
        f"Drive C has {free:.2f} GB free space. "
        f"{used:.2f} GB used out of {total:.2f} GB."
    )


def get_system_info():
    return (
        f"Operating system: {platform.system()}. "
        f"Version: {platform.version()}. "
        f"Processor: {platform.processor()}."
    )


def get_system_status():
    return "\n".join([
        "Here is your system status.",
        get_cpu_usage(),
        get_ram_usage(),
        get_battery_status(),
        get_disk_usage(),
        get_system_info()
    ])