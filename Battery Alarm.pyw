import psutil
import time
import os
from pystray import Icon, Menu, MenuItem
from threading import Thread
from pydub import AudioSegment
from pydub.playback import play
from PIL import Image

LOWEST_BATTERY_POINT = 30
HIGHEST_BATTERY_POINT = 97
CHECK_INTERVAL = 2               # seconds

VOLUME_INCREASE = 4              # increase the volumne of the wav file by X db

alert_active = False
stop_alert = False

scenario = ""
sound_file = None

def setup_tray():
    
    def quit_action(icon, item):
        global stop_alert
        stop_alert = True
        icon.stop()
        os._exit(0)

    icon_img = Image.open("Battery Alarm.ico")
    icon = Icon("BatteryAlert", icon_img, "Battery Alert", 
                menu=Menu(MenuItem("Quit", quit_action)))
    icon.run()

Thread(target=setup_tray, daemon=True).start()

while True:
    battery = psutil.sensors_battery()
    if battery is None:
        time.sleep(CHECK_INTERVAL)
        continue

    percent = battery.percent
    charging = battery.power_plugged

    if percent <= LOWEST_BATTERY_POINT and not charging:
        if not alert_active:
            alert_active = True
            stop_alert = False
            sound_file = "low-battery.wav"
    elif percent >= HIGHEST_BATTERY_POINT and charging:
        if not alert_active:
            alert_active = True
            stop_alert = False
            sound_file = "full-battery.wav"
    else:
        # Battery status safe - stop alert if active
        if alert_active:
            stop_alert = True
            alert_active = False
            sound_file = None

    if sound_file != None:
        sound = AudioSegment.from_file(sound_file)
        play(sound + VOLUME_INCREASE)

    time.sleep(CHECK_INTERVAL)