import pygetwindow as gw
import os
import sys

def minimize_windows():
    if sys.platform == "darwin":  # macOS
        os.system("osascript -e 'tell application \"System Events\" to set minimize of every window of every process to true'")
    else:  # Windows
        for window in gw.getAllWindows():
            try:
                window.minimize()
            except:
                pass