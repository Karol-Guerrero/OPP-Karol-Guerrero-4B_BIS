import tkinter as tk
from tkinter import ttk

root = tk.Tk()
root.title("Tkinter Library Test")
root.geometry("640x480")
root.minsize(320, 240)

ttk.Label(root, text="Student: Guerrero Quintero Karol Emmanuel").pack(padx=20, pady=20)

root.mainloop()