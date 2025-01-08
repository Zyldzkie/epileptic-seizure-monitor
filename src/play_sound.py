import playsound
import os
import sys



def play_alert():
    if sys.platform == "darwin":  # macOS
        os.system("afplay alert.wav")
    else:  # Windows
        playsound.playsound("alert.wav")