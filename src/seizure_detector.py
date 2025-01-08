import cv2
import numpy as np
import time

class SeizureDetector:
    def __init__(self):
        self.read_frequency = 1/60
        self.dangerous_freq_min = 3   # Hz
        self.dangerous_freq_max = 30  # Hz
        self.frame_buffer = []
        self.buffer_size = 30
        self.intensity_change_thresh = 0.2,
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
        
        if intensity_change > self.intensity_change_thresh:
            self.frame_timestamps = [t for t in self.frame_timestamps 
                                   if current_time - t <= 1.0]
            self.frame_timestamps.append(current_time)
            
            frequency = self.analyze_frequency()
            
            is_dangerous_freq = (self.dangerous_freq_min <= frequency <= self.dangerous_freq_max)
            
            return is_dangerous_freq and intensity_change > self.intensity_change_thresh
            
        return False