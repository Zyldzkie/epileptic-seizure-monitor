import os
import sys
from pygame import mixer

def play_alert(play_sound_path):
    try:
        mixer.init()
        alert_file = play_sound_path
        alert_file = os.path.abspath(alert_file)
        mixer.music.load(alert_file)
        mixer.music.play()
    except Exception as e:
        print(f"Error playing sound: {e}")

