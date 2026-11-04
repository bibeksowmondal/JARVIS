
from automation.system_monitor import (
    get_cpu_usage,
    get_ram_usage,
    get_battery_status,
    get_disk_usage,
    get_system_info,
    get_system_status
)

print("\n========== JARVIS SYSTEM MONITOR ==========\n")

print("1. CPU:", get_cpu_usage())
print("2. RAM:", get_ram_usage())
print("3. BATTERY:", get_battery_status())
print("4. DISK:", get_disk_usage())
print("5. SYSTEM:", get_system_info())

print("\n========== COMPLETE REPORT ==========\n")
print(get_system_status())
