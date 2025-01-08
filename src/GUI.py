import tkinter as tk
from tkinter import messagebox

def show_alert():
    root = tk.Tk()
    root.withdraw()
    messagebox.showwarning("Warning", "Potential seizure-inducing content detected!")
    root.destroy()
