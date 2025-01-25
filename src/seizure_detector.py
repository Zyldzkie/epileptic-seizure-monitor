import cv2
import numpy as np
import time
import os

class SeizureDetector:

    def __init__(self, 
                 refresh_rate=60, 
                 dangerous_freq_min=3,
                 dangerous_freq_max=30, 
                 intensity_change_thresh=0.2, 
                 alert_cooldown=5,
                 consecutive_threshold=3,
                 window_trigger_behavior="minimize",
                 play_sound_path=None  # Default to None
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

        self.window_trigger_behavior = window_trigger_behavior
        
        # Load sound path from file if not provided
        if play_sound_path is None:
            try:
                with open('sound_path.txt', 'r') as f:
                    self.play_sound_path = f.read().strip()
            except FileNotFoundError:
                self.play_sound_path = os.path.join(os.path.dirname(__file__), '..', 'assets', 'alert.mp3')  # Default path
        else:
            self.play_sound_path = play_sound_path

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
    
    