import cv2
import numpy as np
import mss
import time
from PIL import ImageGrab
import threading
import playsound
import tkinter as tk
from tkinter import messagebox
import pygetwindow as gw
import os
import sys

class SeizureDetector:
    def __init__(self):
        self.dangerous_freq_min = 3   # Hz
        self.dangerous_freq_max = 30  # Hz
        self.frame_buffer = []
        self.buffer_size = 30
        self.threshold = {
            'intensity_change': 0.2,
            'contrast': 0.5
        }
        self.alert_cooldown = 10
        self.last_alert = 0
        self.frame_timestamps = []
        
    def analyze_frequency(self):
        if len(self.frame_timestamps) < 2:
            return 0
            
        time_diffs = []
        for i in range(len(self.frame_timestamps) - 1):
            diff = self.frame_timestamps[i + 1] - self.frame_timestamps[i]
            if diff > 0:  # Avoid division by zero
                time_diffs.append(1.0 / diff)  # Convert to frequency (Hz)
        
        return np.mean(time_diffs) if time_diffs else 0
        
    def calculate_risk_factors(self, frame1, frame2):
        current_time = time.time()
        
        intensity_diff = cv2.absdiff(frame1, frame2)
        intensity_change = np.mean(intensity_diff) / 255.0
        
        if intensity_change > self.threshold['intensity_change']:
            self.frame_timestamps = [t for t in self.frame_timestamps 
                                   if current_time - t <= 1.0]
            self.frame_timestamps.append(current_time)
            
            frequency = self.analyze_frequency()
            
            is_dangerous_freq = (self.dangerous_freq_min <= frequency <= self.dangerous_freq_max)
            
            return is_dangerous_freq and intensity_change > self.threshold['intensity_change']
            
        return False

def play_alert():
    if sys.platform == "darwin":  # macOS
        os.system("afplay alert.wav")
    else:  # Windows
        playsound.playsound("alert.wav")

def show_alert():
    root = tk.Tk()
    root.withdraw()
    messagebox.showwarning("Warning", "Potential seizure-inducing content detected!")
    root.destroy()

def minimize_windows():
    if sys.platform == "darwin":  # macOS
        os.system("osascript -e 'tell application \"System Events\" to set minimize of every window of every process to true'")
    else:  # Windows
        for window in gw.getAllWindows():
            try:
                window.minimize()
            except:
                pass

def main():
    detector = SeizureDetector()
    sct = mss.mss()
    prev_gray = None
    
    while True:
        try:
            if sys.platform == "darwin":  # macOS
                screen = np.array(ImageGrab.grab())
            else:  # Windows
                screen = np.array(sct.grab(sct.monitors[1]))
                
            gray = cv2.cvtColor(screen, cv2.COLOR_BGR2GRAY)
            
            if prev_gray is not None:
                if detector.calculate_risk_factors(prev_gray, gray):
                    current_time = time.time()
                    if current_time - detector.last_alert >= detector.alert_cooldown:
                        detector.last_alert = current_time
                        threading.Thread(target=play_alert).start()
                        threading.Thread(target=show_alert).start()
                        threading.Thread(target=minimize_windows).start()
            
            prev_gray = gray.copy()
            time.sleep(1/60)  
            
        except KeyboardInterrupt:
            break
        
if __name__ == "__main__":
    main()