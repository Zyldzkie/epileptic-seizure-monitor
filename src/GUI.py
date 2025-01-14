import tkinter as tk
from tkinter import messagebox


class SeizureMonitorApp:
    def __init__(self, detector, logic):
        self.detector = detector
        self.logic = logic
        self.root = tk.Tk()
        self.root.geometry("850x400")
        self.root.title("Epileptic Seizure Monitor")

        self.setup_frontpage()

    def setup_frontpage(self):
        self.root.configure(bg="#2e2e2e")  # Dark background

        title = "Welcome to EpilepSafe"
        description = (
            "Empowering individuals with epilepsy with a tool designed to enhance safety, "
            "promote awareness, and foster a better quality of life. Experience peace of "
            "mind through innovative features tailored to meet your unique needs."
        )

        title_label = tk.Label(
            self.root, text=title, wraplength=400, justify="left",
            bg="#2e2e2e", font=("Arial", 24, "bold"), fg="#ffffff"
        )
        title_label.place(relx=0.02, rely=0.20, relwidth=0.5, relheight=0.1)

        description_label = tk.Label(
            self.root, text=description, wraplength=400, justify="left",
            bg="#2e2e2e", font=("Arial", 16), fg="#ffffff"
        )
        description_label.place(relx=0.01, rely=0.30, relwidth=0.55, relheight=0.5)

        self.setup_settings()

    def setup_settings(self):
        settings_frame = tk.Frame(self.root, bg="#2e2e2e")
        settings_frame.place(relx=0.55, rely=0.17, relwidth=0.4, relheight=1)

        def save_settings():
            try:
                self.detector.refresh_rate = int(refresh_rate_spinbox.get())
                self.detector.read_frequency = float(read_frequency_spinbox.get())
                self.detector.dangerous_freq_min = float(dangerous_freq_min_spinbox.get())
                self.detector.dangerous_freq_max = float(dangerous_freq_max_spinbox.get())
                self.detector.intensity_change_thresh = float(intensity_change_thresh_spinbox.get())
                self.detector.alert_cooldown = int(alert_cooldown_spinbox.get())
                messagebox.showinfo("Settings Saved", "Settings have been successfully updated.")
            except ValueError:
                messagebox.showerror("Invalid Input", "Please enter valid numbers for all settings.")

        tk.Label(settings_frame, text="Refresh Rate:", bg="#2e2e2e", fg="#ffffff").pack()
        refresh_rate_spinbox = tk.Spinbox(settings_frame, from_=1, to=120, increment=1)
        refresh_rate_spinbox.delete(0, "end")
        refresh_rate_spinbox.insert(0, str(self.detector.refresh_rate))
        refresh_rate_spinbox.pack()

        tk.Label(settings_frame, text="Read Frequency:", bg="#2e2e2e", fg="#ffffff").pack()
        read_frequency_spinbox = tk.Spinbox(settings_frame, from_=0.01, to=10, increment=0.01)
        read_frequency_spinbox.delete(0, "end")
        read_frequency_spinbox.insert(0, str(self.detector.read_frequency))
        read_frequency_spinbox.pack()

        tk.Label(settings_frame, text="Dangerous Frequency Min:", bg="#2e2e2e", fg="#ffffff").pack()
        dangerous_freq_min_spinbox = tk.Spinbox(settings_frame, from_=0, to=100, increment=0.1)
        dangerous_freq_min_spinbox.delete(0, "end")
        dangerous_freq_min_spinbox.insert(0, str(self.detector.dangerous_freq_min))
        dangerous_freq_min_spinbox.pack()

        tk.Label(settings_frame, text="Dangerous Frequency Max:", bg="#2e2e2e", fg="#ffffff").pack()
        dangerous_freq_max_spinbox = tk.Spinbox(settings_frame, from_=0, to=100, increment=0.1)
        dangerous_freq_max_spinbox.delete(0, "end")
        dangerous_freq_max_spinbox.insert(0, str(self.detector.dangerous_freq_max))
        dangerous_freq_max_spinbox.pack()

        tk.Label(settings_frame, text="Intensity Change Threshold:", bg="#2e2e2e", fg="#ffffff").pack()
        intensity_change_thresh_spinbox = tk.Spinbox(settings_frame, from_=0, to=1, increment=0.01)
        intensity_change_thresh_spinbox.delete(0, "end")
        intensity_change_thresh_spinbox.insert(0, str(self.detector.intensity_change_thresh))
        intensity_change_thresh_spinbox.pack()

        tk.Label(settings_frame, text="Alert Cooldown:", bg="#2e2e2e", fg="#ffffff").pack()
        alert_cooldown_spinbox = tk.Spinbox(settings_frame, from_=1, to=60, increment=1)
        alert_cooldown_spinbox.delete(0, "end")
        alert_cooldown_spinbox.insert(0, str(self.detector.alert_cooldown))
        alert_cooldown_spinbox.pack()

        save_button = tk.Button(
            settings_frame, text="Save", command=save_settings,
            bg="#4a4a4a", fg="#ffffff", font=("Arial", 12, "bold")
        )
        save_button.pack(pady=10)  # Add padding to ensure visibility

    def show_alert(self):
        self.root.after(0, lambda: messagebox.showwarning(
            "Warning", "Potential seizure-inducing content detected!"
        ))

    def run(self):
        self.root.mainloop()
