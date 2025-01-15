import cv2
import numpy as np
import time

class SeizureDetector:

    def __init__(self, 
                 refresh_rate=60, 
                 dangerous_freq_min=3,
                 dangerous_freq_max=30, 
                 intensity_change_thresh=0.2, 
                 alert_cooldown=5,
                 consecutive_threshold=3,
                 ):

        self.refresh_rate = refresh_rate
        self.read_frequency = 1/self.refresh_rate
        self.dangerous_freq_min = dangerous_freq_min  # Hz
        self.dangerous_freq_max = dangerous_freq_max  # Hz
        self.frame_buffer = []
        self.buffer_size = self.refresh_rate
        self.intensity_change_thresh = intensity_change_thresh
        self.alert_cooldown = alert_cooldown
        self.last_alert = 0
        self.frame_timestamps = []
        self.last_frame_size = None
        self.consecutive_threshold = consecutive_threshold
        self.consecutive_danger_count = 0  
        

    def analyze_frequency(self):
        if len(self.frame_timestamps) < 2:
            return 0
            
        time_diffs = []
        for i in range(len(self.frame_timestamps) - 1):
            diff = self.frame_timestamps[i + 1] - self.frame_timestamps[i]
            if diff > 0:  # Avoid division by zero
                time_diffs.append(1.0 / diff)  # Convert to frequency (Hz)
        
        return np.mean(time_diffs) if time_diffs else 0
        

    def is_seizure_probable(self, frame1, frame2):
        if frame1 is None or frame2 is None:
            return False
            
        # Check if frames have different sizes
        if frame1.shape != frame2.shape:
            return False
            
        current_time = time.time()
        
        intensity_diff = cv2.absdiff(frame1, frame2)
        intensity_change = np.mean(intensity_diff) / 255.0
        
        if intensity_change > self.intensity_change_thresh:
            self.frame_timestamps = [t for t in self.frame_timestamps 
                                   if current_time - t <= 1.0]
            self.frame_timestamps.append(current_time)
            
            frequency = self.analyze_frequency()
            
            is_dangerous_freq = (self.dangerous_freq_min <= frequency <= self.dangerous_freq_max)
            
        
            if is_dangerous_freq:
                self.consecutive_danger_count += 1  
            # Move this out maybe?????
            else:
                self.consecutive_danger_count = 0  
            
            return self.consecutive_danger_count >= self.consecutive_threshold  
            
        return False
    
    