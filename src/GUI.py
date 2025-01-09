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
        self.root.geometry("1100x570")
        self.root.title("Epileptic Seizure Monitor")
        self.detector = SeizureDetector()

        # Screen capture variables
        self.prev_gray = None
        self.sct = mss.mss()

        self.setup_frontpage()

    def setup_frontpage(self):
        
        try:
            bg_image = Image.open("src/static/bg.png")
            bg_photo = ImageTk.PhotoImage(bg_image)
        except Exception as e:
            messagebox.showerror("Error", f"Failed to load background image: {e}")
            bg_photo = None

        if bg_photo:
            bg_label = tk.Label(self.root, image=bg_photo)
            bg_label.place(relwidth=1, relheight=1)
            # Keep a reference to avoid garbage collection
            bg_label.image = bg_photo

        title = "Welcome to VisualEase"
        description = ("The ultimate companion for individuals with epilepsy and their caregivers, "
                       "designed to promote safety, awareness, and a better quality of life.")

        title_label = tk.Label(self.root, text=title, wraplength=400, justify="left", bg="#f8d4fc", font=("Arial", 24, "bold"), fg="#c700ff")
        title_label.place(relx=0.07, rely=0.17, relwidth=0.4, relheight=0.1)

        description_label = tk.Label(self.root, text=description, wraplength=400, justify="left", bg="#f8d4fc", font=("Arial", 16), fg="#c700ff")
        description_label.place(relx=0.07, rely=0.27, relwidth=0.4, relheight=0.3)

        next_button = tk.Button(self.root, text="Get Started", command=self.go_to_next_page, bg="#c700ff", fg="white", font=("Arial", 16, "bold"))
        next_button.place(relx=0.20, relwidth=0.13, relheight=0.07, rely=0.65)

    def go_to_next_page(self):
        
        self.root.withdraw()  # Hide the first page

        settings_window = tk.Toplevel(self.root)
        settings_window.geometry("800x400")
        settings_window.title("Seizure Detector Settings")

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

        def go_back():
            settings_window.destroy()
            self.root.deiconify()  # Show the first page again

        back_button = tk.Button(settings_window, text="Back", command=go_back, bg="#c700ff", fg="white", font=("Arial", 12, "bold"))
        back_button.pack(anchor="nw", padx=10, pady=10)

        tk.Label(settings_window, text="Refresh Rate:").pack()
        refresh_rate_entry = tk.Entry(settings_window)
        refresh_rate_entry.insert(0, str(self.detector.refresh_rate))
        refresh_rate_entry.pack()

        tk.Label(settings_window, text="Read Frequency:").pack()
        read_frequency_entry = tk.Entry(settings_window)
        read_frequency_entry.insert(0, str(self.detector.read_frequency))
        read_frequency_entry.pack()

        tk.Label(settings_window, text="Dangerous Frequency Min:").pack()
        dangerous_freq_min_entry = tk.Entry(settings_window)
        dangerous_freq_min_entry.insert(0, str(self.detector.dangerous_freq_min))
        dangerous_freq_min_entry.pack()

        tk.Label(settings_window, text="Dangerous Frequency Max:").pack()
        dangerous_freq_max_entry = tk.Entry(settings_window)
        dangerous_freq_max_entry.insert(0, str(self.detector.dangerous_freq_max))
        dangerous_freq_max_entry.pack()

        tk.Label(settings_window, text="Intensity Change Threshold:").pack()
        intensity_change_thresh_entry = tk.Entry(settings_window)
        intensity_change_thresh_entry.insert(0, str(self.detector.intensity_change_thresh))
        intensity_change_thresh_entry.pack()

        tk.Label(settings_window, text="Alert Cooldown:").pack()
        alert_cooldown_entry = tk.Entry(settings_window)
        alert_cooldown_entry.insert(0, str(self.detector.alert_cooldown))
        alert_cooldown_entry.pack()

        save_button = tk.Button(settings_window, text="Save", command=save_settings, bg="#c700ff", fg="white", font=("Arial", 12, "bold"))
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
