from seizure_detector import SeizureDetector
from play_sound import play_alert
from window_manager import minimize_windows, grab_screen
from GUI import show_alert

import cv2
import time
import threading
import mss

def main():
    detector = SeizureDetector(refresh_rate=180)
    prev_gray = None
    sct = None
    
    try:
        sct = mss.mss() 
        while True:
            try:
                screen = grab_screen(sct) 
                if screen is None:
                    time.sleep(detector.read_frequency)
                    continue
                    
                gray = cv2.cvtColor(screen, cv2.COLOR_BGR2GRAY)
                
                if prev_gray is not None:
                    if detector.calculate_risk_factors(prev_gray, gray):
                        current_time = time.time()
                        if current_time - detector.last_alert >= detector.alert_cooldown:
                            detector.last_alert = current_time
                            threading.Thread(target=play_alert, daemon=True).start()
                            threading.Thread(target=show_alert, daemon=True).start()
                            threading.Thread(target=minimize_windows, daemon=True).start()
                
                prev_gray = gray.copy()
                del screen  
                time.sleep(detector.read_frequency)
                
            except KeyboardInterrupt:
                break
                
    finally:
        if sct:
            sct.close() 
        cv2.destroyAllWindows() 

if __name__ == "__main__":
    main()