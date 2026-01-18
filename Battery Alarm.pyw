import psutil
import time
import os
from pystray import Icon, Menu, MenuItem
from threading import Thread
from pydub import AudioSegment
from pydub.playback import play
from PIL import Image


LOWEST_BATTERY_POINT = 40
HIGHEST_BATTERY_POINT = 97
CHECK_INTERVAL = 2               # seconds

GAP_BETWEEN_ALERTS = 1           # seconds between alert sound
VOLUME_INCREASE = 4              # increase the volumne of the wav file by X db

alert_active = False
stop_alert = False

scenario = ""

def alert_sound():
    if scenario == "low-battery":
        sound_file = "low-battery.wav"
    elif scenario == "full-battery":
        sound_file = "full-battery.wav"

    sound = AudioSegment.from_file(sound_file)
    
    while not stop_alert:
        play(sound + VOLUME_INCREASE)
        time.sleep(GAP_BETWEEN_ALERTS)

# Function for tray icon
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

def maintain_posture():
    posture_reminder_audio = AudioSegment.from_file("Posture Reminder.wav")
    play(posture_reminder_audio + VOLUME_INCREASE)
    while True:
        time.sleep(20*60)
        play(posture_reminder_audio + VOLUME_INCREASE - 2)

Thread(target=setup_tray, daemon=True).start()
# Thread(target=maintain_posture, daemon=True).start()

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
            scenario = "low-battery"
            Thread(target=alert_sound, daemon=True).start()
    elif percent >= HIGHEST_BATTERY_POINT and charging:
        if not alert_active:
            alert_active = True
            stop_alert = False
            scenario = "full-battery"
            Thread(target=alert_sound, daemon=True).start()
    else:
        # Battery status safe → stop alert if active
        if alert_active:
            stop_alert = True
            alert_active = False

    time.sleep(CHECK_INTERVAL)

