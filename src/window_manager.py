import pygetwindow as gw
import os
import sys
import mss
import numpy as np

def minimize_windows():
    if sys.platform == "darwin":  # macOS
        os.system("osascript -e 'tell application \"System Events\" to set minimize of every window of every process to true'")
    else:  # Windows
        for window in gw.getAllWindows():
            try:
                window.minimize()
            except:
                pass

def grab_screen(sct):
    try:
        screen = np.array(sct.grab(sct.monitors[1]))
        return screen
    except Exception as e:
        print(f"Screen capture failed: {e}")
        return None