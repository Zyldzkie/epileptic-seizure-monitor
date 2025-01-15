from seizure_detector import SeizureDetector
from play_sound import play_alert
from window_manager import minimize_active_window, close_active_window, grab_screen
from GUI import GUI
import cv2
import time
import threading
import mss

class ApplicationLogic:
    def __init__(self):
        self.running = True
        self.detector = SeizureDetector()
        self.prev_gray = None
        self.sct = None
        
    def start_monitoring(self):
        self.sct = mss.mss()
        while self.running:
            try:
                screen = grab_screen(self.sct)
                if screen is None:
                    time.sleep(self.detector.read_frequency)
                    continue
                    
                gray = cv2.cvtColor(screen, cv2.COLOR_BGR2GRAY)
                
                if self.prev_gray is not None:
                    if self.detector.is_seizure_probable(self.prev_gray, gray):
                        current_time = time.time()
                        if current_time - self.detector.last_alert >= self.detector.alert_cooldown:
                            self.detector.last_alert = current_time
                            
                            threading.Thread(target=self.gui.show_alert, daemon=True).start()
                            
                            if self.detector.window_trigger_behavior == "minimize":
                                threading.Thread(target=minimize_active_window, daemon=True).start()
                            else:  # close
                                threading.Thread(target=close_active_window, daemon=True).start()

                            threading.Thread(target=play_alert, daemon=True).start()
                
                self.prev_gray = gray.copy()
                del screen
                time.sleep(self.detector.read_frequency)
                
            except KeyboardInterrupt:
                break
                
    def stop_monitoring(self):
        self.running = False
        if self.sct:
            self.sct.close()
        cv2.destroyAllWindows()

def main():
    logic = ApplicationLogic()
    gui = GUI(logic.detector, logic)
    logic.gui = gui
    
    monitor_thread = threading.Thread(target=logic.start_monitoring, daemon=True)
    monitor_thread.start()
    
    gui.run()
    logic.stop_monitoring()

if __name__ == "__main__":
    main()