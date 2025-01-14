import tkinter as tk
from tkinter import messagebox

class SeizureMonitorApp:
    def __init__(self, detector, logic):
        self.detector = detector
        self.logic = logic
        self.root = tk.Tk()
        self.root.geometry("850x400")
        self.root.title("Epileptic Seizure Monitor")

        # Default theme is dark mode
        self.is_dark_mode = True
        self.theme = {
            "bg": "#2e2e2e",
            "fg": "#ffffff",
            "button_bg": "#4a4a4a",
            "button_fg": "#ffffff",
            "spinbox_bg": "#e0e0e0",
            "spinbox_fg": "#000000",
            "toggle_bg": "#2e2e2e"
        }
        self.light_theme = {
            "bg": "#ffffff",
            "fg": "#000000",
            "button_bg": "#e0e0e0",
            "button_fg": "#000000",
            "spinbox_bg": "#e0e0e0",
            "spinbox_fg": "#000000",
            "toggle_bg": "#ffffff"
        }

        self.setup_frontpage()

    def create_toggle_bar(self):
        """Toggle bar for theme switching."""
        toggle_frame = tk.Frame(self.root, bg=self.theme["bg"])
        toggle_frame.place(relx=0.85, rely=0.02, relwidth=0.12, relheight=0.08)

        self.toggle_canvas = tk.Canvas(
            toggle_frame,
            width=60,
            height=30,
            bg=self.theme["toggle_bg"],
            highlightthickness=0
        )
        self.toggle_canvas.pack()

        # Toggle bar components
        self.toggle_rect = self.toggle_canvas.create_rectangle(5, 5, 55, 25, fill=self.theme["button_bg"], outline=self.theme["fg"])
        self.toggle_knob = self.toggle_canvas.create_oval(5, 5, 25, 25, fill=self.theme["fg"], outline=self.theme["fg"])

        # Bind toggle click event
        self.toggle_canvas.bind("<Button-1>", self.switch_theme)

    def switch_theme(self, event=None):
        """Switch the theme using the toggle bar."""
        self.is_dark_mode = not self.is_dark_mode
        self.theme = self.light_theme if not self.is_dark_mode else {
            "bg": "#2e2e2e",
            "fg": "#ffffff",
            "button_bg": "#4a4a4a",
            "button_fg": "#ffffff",
            "spinbox_bg": "#e0e0e0",
            "spinbox_fg": "#000000",
            "toggle_bg": "#2e2e2e"
        }
        self.apply_theme()

        # Update the toggle knob position
        if self.is_dark_mode:
            self.toggle_canvas.coords(self.toggle_knob, 5, 5, 25, 25)
        else:
            self.toggle_canvas.coords(self.toggle_knob, 35, 5, 55, 25)

    def apply_theme(self):
        """Apply the current theme to all widgets."""
        self.root.configure(bg=self.theme["bg"])
        for widget in self.root.winfo_children():
            widget_type = widget.winfo_class()
            if widget_type == "Label":
                widget.configure(bg=self.theme["bg"], fg=self.theme["fg"])
            elif widget_type == "Frame":
                widget.configure(bg=self.theme["bg"])
                for child in widget.winfo_children():
                    child_type = child.winfo_class()
                    if child_type in ("Label", "Button"):
                        child.configure(bg=self.theme["bg"], fg=self.theme["fg"])
                    elif child_type == "Spinbox":
                        child.configure(bg=self.theme["spinbox_bg"], fg=self.theme["spinbox_fg"])
            elif widget_type == "Button":
                widget.configure(
                    bg=self.theme["button_bg"], fg=self.theme["button_fg"]
                )
        self.toggle_canvas.configure(bg=self.theme["toggle_bg"])
        self.toggle_canvas.itemconfig(self.toggle_rect, fill=self.theme["button_bg"], outline=self.theme["fg"])
        self.toggle_canvas.itemconfig(self.toggle_knob, fill=self.theme["fg"], outline=self.theme["fg"])

    def setup_frontpage(self):
        self.root.configure(bg=self.theme["bg"])  # Background color

        title = "Welcome to EpilepSafe"
        description = (
            "Empowering individuals with epilepsy with a tool designed to enhance safety, "
            "promote awareness, and foster a better quality of life. Experience peace of "
            "mind through innovative features tailored to meet your unique needs."
        )

        # Create the toggle bar for theme
        self.create_toggle_bar()

        title_label = tk.Label(
            self.root,
            text=title,
            wraplength=400,
            justify="left",
            bg=self.theme["bg"],
            font=("Arial", 24, "bold"),
            fg=self.theme["fg"]
        )
        title_label.place(relx=0.02, rely=0.20, relwidth=0.5, relheight=0.1)

        description_label = tk.Label(
            self.root,
            text=description,
            wraplength=400,
            justify="left",
            bg=self.theme["bg"],
            font=("Arial", 16),
            fg=self.theme["fg"]
        )
        description_label.place(relx=0.01, rely=0.30, relwidth=0.55, relheight=0.5)

        self.setup_settings()

    def setup_settings(self):
        settings_frame = tk.Frame(self.root, bg=self.theme["bg"])
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

        tk.Label(settings_frame, text="Refresh Rate:", bg=self.theme["bg"], fg=self.theme["fg"]).pack()
        refresh_rate_spinbox = tk.Spinbox(settings_frame, from_=1, to=120, increment=1)
        refresh_rate_spinbox.delete(0, "end")
        refresh_rate_spinbox.insert(0, str(self.detector.refresh_rate))
        refresh_rate_spinbox.configure(bg=self.theme["spinbox_bg"], fg=self.theme["spinbox_fg"])
        refresh_rate_spinbox.pack()

        tk.Label(settings_frame, text="Read Frequency:", bg=self.theme["bg"], fg=self.theme["fg"]).pack()
        read_frequency_spinbox = tk.Spinbox(settings_frame, from_=0.01, to=10, increment=0.01)
        read_frequency_spinbox.delete(0, "end")
        read_frequency_spinbox.insert(0, str(self.detector.read_frequency))
        read_frequency_spinbox.configure(bg=self.theme["spinbox_bg"], fg=self.theme["spinbox_fg"])
        read_frequency_spinbox.pack()

        tk.Label(settings_frame, text="Dangerous Frequency Min:", bg=self.theme["bg"], fg=self.theme["fg"]).pack()
        dangerous_freq_min_spinbox = tk.Spinbox(settings_frame, from_=0, to=100, increment=0.1)
        dangerous_freq_min_spinbox.delete(0, "end")
        dangerous_freq_min_spinbox.insert(0, str(self.detector.dangerous_freq_min))
        dangerous_freq_min_spinbox.configure(bg=self.theme["spinbox_bg"], fg=self.theme["spinbox_fg"])
        dangerous_freq_min_spinbox.pack()

        tk.Label(settings_frame, text="Dangerous Frequency Max:", bg=self.theme["bg"], fg=self.theme["fg"]).pack()
        dangerous_freq_max_spinbox = tk.Spinbox(settings_frame, from_=0, to=100, increment=0.1)
        dangerous_freq_max_spinbox.delete(0, "end")
        dangerous_freq_max_spinbox.insert(0, str(self.detector.dangerous_freq_max))
        dangerous_freq_max_spinbox.configure(bg=self.theme["spinbox_bg"], fg=self.theme["spinbox_fg"])
        dangerous_freq_max_spinbox.pack()

        tk.Label(settings_frame, text="Intensity Change Threshold:", bg=self.theme["bg"], fg=self.theme["fg"]).pack()
        intensity_change_thresh_spinbox = tk.Spinbox(settings_frame, from_=0, to=1, increment=0.01)
        intensity_change_thresh_spinbox.delete(0, "end")
        intensity_change_thresh_spinbox.insert(0, str(self.detector.intensity_change_thresh))
        intensity_change_thresh_spinbox.configure(bg=self.theme["spinbox_bg"], fg=self.theme["spinbox_fg"])
        intensity_change_thresh_spinbox.pack()

        tk.Label(settings_frame, text="Alert Cooldown:", bg=self.theme["bg"], fg=self.theme["fg"]).pack()
        alert_cooldown_spinbox = tk.Spinbox(settings_frame, from_=1, to=60, increment=1)
        alert_cooldown_spinbox.delete(0, "end")
        alert_cooldown_spinbox.insert(0, str(self.detector.alert_cooldown))
        alert_cooldown_spinbox.configure(bg=self.theme["spinbox_bg"], fg=self.theme["spinbox_fg"])
        alert_cooldown_spinbox.pack()

        save_button = tk.Button(
            settings_frame,
            text="Save",
            command=save_settings,
            bg=self.theme["button_bg"],
            fg=self.theme["button_fg"],
            font=("Arial", 12, "bold")
        )
        save_button.pack(pady=10)

    def show_alert(self):
        self.root.after(0, lambda: messagebox.showwarning(
            "Warning", "Potential seizure-inducing content detected!"
        ))

    def run(self):
        self.root.mainloop()
