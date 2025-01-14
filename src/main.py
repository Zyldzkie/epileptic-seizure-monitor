from GUI import SeizureMonitorApp
import threading
import time
import cv2
import numpy as np
import mss


class SeizureMonitorLogic:
    def __init__(self, detector):
        self.detector = detector
        self.prev_gray = None
        self.sct = mss.mss()
        self.running = False

    def grab_screen(self):
        try:
            with mss.mss() as sct:
                monitor = sct.monitors[0]  # Grab the primary monitor
                screen = sct.grab(monitor)
                screen_np = np.array(screen)  # Convert raw pixels to a NumPy array
                return cv2.cvtColor(screen_np, cv2.COLOR_BGRA2BGR)  # Convert BGRA to BGR
        except Exception as e:
            print(f"Error capturing screen: {e}")
            return None


    def run_detection(self):
        while self.running:
            try:
                screen = self.grab_screen()
                if screen is None:
                    time.sleep(self.detector.read_frequency)
                    continue

                gray = cv2.cvtColor(screen, cv2.COLOR_BGR2GRAY)

                if self.prev_gray is not None:
                    if self.detector.calculate_risk_factors(self.prev_gray, gray):
                        current_time = time.time()
                        if current_time - self.detector.last_alert >= self.detector.alert_cooldown:
                            self.detector.last_alert = current_time
                            self.alert_callback()

                self.prev_gray = gray.copy()
                time.sleep(self.detector.read_frequency)
            except Exception as e:
                print(f"Error during detection: {e}")

    def start(self, alert_callback):
        self.running = True
        self.alert_callback = alert_callback
        threading.Thread(target=self.run_detection, daemon=True).start()

    def stop(self):
        self.running = False


if __name__ == "__main__":
    from seizure_detector import SeizureDetector

    detector = SeizureDetector()
    logic = SeizureMonitorLogic(detector)

    app = SeizureMonitorApp(detector, logic)
    logic.start(app.show_alert)
    app.run()
    logic.stop()