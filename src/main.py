from seizure_detector import SeizureDetector
from play_sound import play_alert
from window_manager import minimize_windows, grab_screen
from GUI import show_alert

import cv2
import numpy as np
import time
from PIL import ImageGrab
import threading
import sys


def main():
    detector = SeizureDetector(refresh_rate=180)
   
    prev_gray = None
    
    while True:
        try:
            
            gray = cv2.cvtColor(grab_screen(), cv2.COLOR_BGR2GRAY)
            
            if prev_gray is not None:
                if detector.calculate_risk_factors(prev_gray, gray):
                    current_time = time.time()
                    if current_time - detector.last_alert >= detector.alert_cooldown:
                        detector.last_alert = current_time
                        threading.Thread(target=play_alert).start()
                        threading.Thread(target=show_alert).start()
                        threading.Thread(target=minimize_windows).start()
            
            prev_gray = gray.copy()
            time.sleep(detector.read_frequency)  
            
        except KeyboardInterrupt:
            break
        
if __name__ == "__main__":
    main()