import os
import sys
from pygame import mixer

def play_alert():
    try:
        mixer.init()
        alert_file = os.path.join(os.path.dirname(__file__), '..', 'assets', 'alert.mp3')
        alert_file = os.path.abspath(alert_file)
        mixer.music.load(alert_file)
        mixer.music.play()
    except Exception as e:
        print(f"Error playing sound: {e}")

