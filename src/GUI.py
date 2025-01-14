import tkinter as tk
from tkinter import messagebox
from PIL import Image, ImageTk
import cv2
import time
import mss
import threading
from seizure_detector import SeizureDetector
import numpy as np

class SeizureMonitorApp:
    def __init__(self):
        
        self.root = tk.Tk()
        self.root.geometry("850x400")
        self.root.title("Epileptic Seizure Monitor")
        self.detector = SeizureDetector()

        # Screen capture variables
        self.prev_gray = None
        self.sct = mss.mss()

        self.setup_frontpage()

    def setup_frontpage(self):
        self.root.configure(bg="#2e2e2e")  # Set background color to dark

        title = "Welcome to EpilepSafe"
        description = ("Empowering individuals with epilepsy with a tool designed to enhance safety, promote awareness, and foster a better quality of life. Experience peace of mind through innovative features tailored to meet your unique needs.")

        title_label = tk.Label(self.root, text=title, wraplength=400, justify="left", bg="#2e2e2e", font=("Arial", 24, "bold"), fg="#ffffff")
        title_label.place(relx=0.02, rely=0.20, relwidth=0.5, relheight=0.1)

        description_label = tk.Label(self.root, text=description, wraplength=400, justify="left", bg="#2e2e2e", font=("Arial", 16), fg="#ffffff")
        description_label.place(relx=0.01, rely=0.30, relwidth=0.55, relheight=0.5)

        self.setup_settings()

    def setup_settings(self):
        settings_frame = tk.Frame(self.root, bg="#2e2e2e")
        settings_frame.place(relx=0.55, rely=0.17, relwidth=0.4, relheight=0.6)

        def save_settings():
            try:
                self.detector.refresh_rate = int(refresh_rate_entry.get())
                self.detector.read_frequency = float(read_frequency_entry.get())
                self.detector.dangerous_freq_min = float(dangerous_freq_min_entry.get())
                self.detector.dangerous_freq_max = float(dangerous_freq_max_entry.get())
                self.detector.intensity_change_thresh = float(intensity_change_thresh_entry.get())
                self.detector.alert_cooldown = int(alert_cooldown_entry.get())
                messagebox.showinfo("Settings Saved", "Settings have been successfully updated.")
            except ValueError:
                messagebox.showerror("Invalid Input", "Please enter valid numbers for all settings.")

        tk.Label(settings_frame, text="Refresh Rate:", bg="#2e2e2e", fg="#ffffff").pack()
        refresh_rate_entry = tk.Entry(settings_frame)
        refresh_rate_entry.insert(0, str(self.detector.refresh_rate))
        refresh_rate_entry.pack()

        tk.Label(settings_frame, text="Read Frequency:", bg="#2e2e2e", fg="#ffffff").pack()
        read_frequency_entry = tk.Entry(settings_frame)
        read_frequency_entry.insert(0, str(self.detector.read_frequency))
        read_frequency_entry.pack()

        tk.Label(settings_frame, text="Dangerous Frequency Min:", bg="#2e2e2e", fg="#ffffff").pack()
        dangerous_freq_min_entry = tk.Entry(settings_frame)
        dangerous_freq_min_entry.insert(0, str(self.detector.dangerous_freq_min))
        dangerous_freq_min_entry.pack()

        tk.Label(settings_frame, text="Dangerous Frequency Max:", bg="#2e2e2e", fg="#ffffff").pack()
        dangerous_freq_max_entry = tk.Entry(settings_frame)
        dangerous_freq_max_entry.insert(0, str(self.detector.dangerous_freq_max))
        dangerous_freq_max_entry.pack()

        tk.Label(settings_frame, text="Intensity Change Threshold:", bg="#2e2e2e", fg="#ffffff").pack()
        intensity_change_thresh_entry = tk.Entry(settings_frame)
        intensity_change_thresh_entry.insert(0, str(self.detector.intensity_change_thresh))
        intensity_change_thresh_entry.pack()

        tk.Label(settings_frame, text="Alert Cooldown:", bg="#2e2e2e", fg="#ffffff").pack()
        alert_cooldown_entry = tk.Entry(settings_frame)
        alert_cooldown_entry.insert(0, str(self.detector.alert_cooldown))
        alert_cooldown_entry.pack()

        save_button = tk.Button(settings_frame, text="Save", command=save_settings, bg="#4a4a4a", fg="#ffffff", font=("Arial", 12, "bold"))
        save_button.pack()

    def run_detection(self):
        
        try:
            screen = self.grab_screen()
            if screen is None:
                # Schedule the next check
                self.root.after(int(self.detector.read_frequency * 1000), self.run_detection)
                return

            gray = cv2.cvtColor(screen, cv2.COLOR_BGR2GRAY)

            if self.prev_gray is not None:
                if self.detector.calculate_risk_factors(self.prev_gray, gray):
                    current_time = time.time()
                    if current_time - self.detector.last_alert >= self.detector.alert_cooldown:
                        self.detector.last_alert = current_time
                        threading.Thread(target=self.show_alert, daemon=True).start()

            self.prev_gray = gray.copy()
        except Exception as e:
            print(f"Error during detection: {e}")

        finally:
            # Schedule the next check
            self.root.after(int(self.detector.read_frequency * 1000), self.run_detection)


    # def grab_screen(self):
    #     try:
    #         monitor = self.sct.monitors[0]
    #         screen = self.sct.grab(monitor)
    #         return cv2.cvtColor(cv2.cvtColor(cv2.array(screen), cv2.COLOR_BGRA2BGR), cv2.COLOR_BGR2RGB)
    #     except Exception as e:
    #         print(f"Error capturing screen: {e}")
    #         return None

    def grab_screen(self):

        try:
            monitor = self.sct.monitors[0]  # Grab the primary monitor
            screen = self.sct.grab(monitor)
            # Convert the raw pixels to a NumPy array
            screen_np = np.array(screen)
            # Convert BGRA to BGR format (cv2 expects this format)
            return cv2.cvtColor(screen_np, cv2.COLOR_BGRA2BGR)
        except Exception as e:
            print(f"Error capturing screen: {e}")
            return None
        

    def show_alert(self):
        self.root.after(0, lambda: messagebox.showwarning(
            "Warning", "Potential seizure-inducing content detected!"
        ))

    def run(self):
        # Start the detection loop
        self.root.after(100, self.run_detection)
        self.root.mainloop()
        print("WORKING APP")
