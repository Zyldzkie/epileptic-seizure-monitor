import tkinter as tk
from tkinter import messagebox
from PIL import Image, ImageTk
from seizure_detector import SeizureDetector

def show_alert():
    root = tk.Tk()
    root.withdraw()
    messagebox.showwarning("Warning", "Potential seizure-inducing content detected!")
    root.destroy()

def go_to_next_page():
    root.withdraw()  # Hide the first page

    settings_window = tk.Toplevel(root)
    settings_window.geometry("800x400")
    settings_window.title("Seizure Detector Settings")

    detector = SeizureDetector()

    def save_settings():
        detector.refresh_rate = int(refresh_rate_entry.get())
        detector.read_frequency = float(read_frequency_entry.get())
        detector.dangerous_freq_min = float(dangerous_freq_min_entry.get())
        detector.dangerous_freq_max = float(dangerous_freq_max_entry.get())
        detector.intensity_change_thresh = float(intensity_change_thresh_entry.get())
        detector.alert_cooldown = int(alert_cooldown_entry.get())
    
        

    def go_back():
        settings_window.destroy()
        root.deiconify()  # Show the first page again

    back_button = tk.Button(settings_window, text="Back", command=go_back, bg="#c700ff", fg="white", font=("Arial", 12, "bold"))
    back_button.pack(anchor="nw", padx=10, pady=10)

    tk.Label(settings_window, text="Refresh Rate:").pack()
    refresh_rate_entry = tk.Entry(settings_window)
    refresh_rate_entry.insert(0, str(detector.refresh_rate))
    refresh_rate_entry.pack()

    tk.Label(settings_window, text="Read Frequency:").pack()
    read_frequency_entry = tk.Entry(settings_window)
    read_frequency_entry.insert(0, str(detector.read_frequency))
    read_frequency_entry.pack()

    tk.Label(settings_window, text="Dangerous Frequency Min:").pack()
    dangerous_freq_min_entry = tk.Entry(settings_window)
    dangerous_freq_min_entry.insert(0, str(detector.dangerous_freq_min))
    dangerous_freq_min_entry.pack()

    tk.Label(settings_window, text="Dangerous Frequency Max:").pack()
    dangerous_freq_max_entry = tk.Entry(settings_window)
    dangerous_freq_max_entry.insert(0, str(detector.dangerous_freq_max))
    dangerous_freq_max_entry.pack()

    tk.Label(settings_window, text="Intensity Change Threshold:").pack()
    intensity_change_thresh_entry = tk.Entry(settings_window)
    intensity_change_thresh_entry.insert(0, str(detector.intensity_change_thresh))
    intensity_change_thresh_entry.pack()

    tk.Label(settings_window, text="Alert Cooldown:").pack()
    alert_cooldown_entry = tk.Entry(settings_window)
    alert_cooldown_entry.insert(0, str(detector.alert_cooldown))
    alert_cooldown_entry.pack()

    save_button = tk.Button(settings_window, text="Save", command=save_settings)
    save_button.pack()

def frontpage():
    global root
    root = tk.Tk()
    root.geometry("1100x570")
    root.title("Epileptic Seizure Monitor")

    bg_image = Image.open("src/static/bg.png")
    bg_photo = ImageTk.PhotoImage(bg_image)
    bg_label = tk.Label(root, image=bg_photo)
    bg_label.place(relwidth=1, relheight=1)

    title = "Welcome to VisualEase"
    description = ("the ultimate companion for individuals with epilepsy and their caregivers, "
                   "designed to promote safety, awareness, and a better quality of life. Manage seizures, track triggers, "
                   "send alerts, and take control of epilepsy with ease.")
    
    title_label = tk.Label(root, text=title, wraplength=400, justify="left", bg="#f8d4fc", font=("Arial", 24, "bold"), fg="#c700ff")
    title_label.place(relx=0.07, rely=0.17, relwidth=0.4, relheight=0.1)
    
    description_label = tk.Label(root, text=description, wraplength=400, justify="left", bg="#f8d4fc", font=("Arial", 16), fg="#c700ff")
    description_label.place(relx=0.07, rely=0.27, relwidth=0.4, relheight=0.3)

    next_button = tk.Button(root, text="Get Started", command=go_to_next_page, bg="#c700ff", fg="white", font=("Arial", 16, "bold"))
    next_button.place(relx=0.20, rely=0.65, relwidth=0.13, relheight=0.07)

    root.mainloop()






