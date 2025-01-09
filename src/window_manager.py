import numpy as np
import mss
import sys
import os

if sys.platform == "darwin":  # macOS
    from AppKit import NSWorkspace, NSScreen
else:  # Windows
    import pygetwindow as gw

def grab_screen(sct):
    try:
        if sys.platform == "darwin":
            workspace = NSWorkspace.sharedWorkspace()
            active_app = workspace.activeApplication()
            if active_app:
                screen = NSScreen.mainScreen()
                frame = screen.frame()
                monitor = {
                    "top": int(frame.origin.y),
                    "left": int(frame.origin.x),
                    "width": int(frame.size.width),
                    "height": int(frame.size.height),
                    "mon": 1,
                }
                screen = np.array(sct.grab(monitor))
                return screen
        else:
            active_window = gw.getActiveWindow()
            if active_window and active_window.title:
                monitor = {
                    "top": active_window.top,
                    "left": active_window.left,
                    "width": active_window.width,
                    "height": active_window.height,
                    "mon": 1,
                }
                screen = np.array(sct.grab(monitor))
                return screen
        return None
    except Exception as e:
        print(f"Screen capture failed: {e}")
        return None


def minimize_active_window():
    try:
        if sys.platform == "darwin":
            workspace = NSWorkspace.sharedWorkspace()
            active_app = workspace.activeApplication()
            if active_app:
                app_name = active_app['NSApplicationName']
                os.system(f'osascript -e \'tell application "{app_name}" to set miniaturized of window 1 to true\'')
        else:
            active_window = gw.getActiveWindow()
            if active_window:
                active_window.minimize()
    except Exception as e:
        print(f"Failed to minimize window: {e}")


def close_active_window():
    try:
        if sys.platform == "darwin":
            workspace = NSWorkspace.sharedWorkspace()
            active_app = workspace.activeApplication()
            if active_app:
                app_name = active_app['NSApplicationName']
                os.system(f'osascript -e \'tell application "{app_name}" to close window 1\'')
        else:
            active_window = gw.getActiveWindow()
            if active_window:
                active_window.close()
    except Exception as e:
        print(f"Failed to close window: {e}")