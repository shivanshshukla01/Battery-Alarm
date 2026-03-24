import psutil
import time
import os

LOWEST_BATTERY_POINT = 30
HIGHEST_BATTERY_POINT = 97
CHECK_INTERVAL = 2               # seconds

VOLUME_INCREASE = 4

alert_active = False
stop_alert = False

scenario = ""
sound_file = None


while true:
    battery = psutil.sensors_battery()
    if battery is none:
        time.sleep(check_interval)
        continue

    percent = battery.percent
    charging = battery.power_plugged

    if pecent <= LOWEST_BATTERY_POINT and not charging:
        os.system(f"aplay low-battery.wav")
    elif percent >= HIGHEST_BATTERY_POINT and charging:
        os.system(f"aplay full-battery.wav")
    
    time.sleep(CHECK_INTERVAL)
