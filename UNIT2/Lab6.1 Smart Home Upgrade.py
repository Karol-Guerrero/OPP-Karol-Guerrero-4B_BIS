import tkinter as tk
from tkinter import ttk, scrolledtext
from abc import ABC, abstractmethod
from datetime import datetime


# ==================== MODEL ====================

class SmartDevice(ABC):
    def __init__(self, name: str, room: str):
        self.name = name
        self.room = room
        self.is_on = False

    @abstractmethod
    def turn_on(self) -> str:
        pass

    @abstractmethod
    def turn_off(self) -> str:
        pass

    def __str__(self):
        estado = "ON" if self.is_on else "OFF"
        return f"[{estado}] {self.name}"


class SmartLight(SmartDevice):
    def turn_on(self):
        self.is_on = True
        return f"{self.name} is ON"

    def turn_off(self):
        self.is_on = False
        return f"{self.name} is OFF"


class SmartThermostat(SmartDevice):
    def turn_on(self):
        self.is_on = True
        return f"{self.name} activated"

    def turn_off(self):
        self.is_on = False
        return f"{self.name} in standby"


class SmartSpeaker(SmartDevice):
    def turn_on(self):
        self.is_on = True
        return f"{self.name} is playing music"

    def turn_off(self):
        self.is_on = False
        return f"{self.name} is muted"


class SmartCamera(SmartDevice):
    def turn_on(self):
        self.is_on = True
        return f"{self.name} is recording"

    def turn_off(self):
        self.is_on = False
        return f"{self.name} stopped (privacy mode)"


# ==================== VIEW (GUI) ====================

class SmartHomeGUI:
    def __init__(self, root, devices):
        self.root = root
        self.devices = devices

        root.title("Lab 6: Polymorphism GUI")
        root.geometry("460x480")
        root.configure(bg="#e6e6e6")

        # Main Header
        tk.Label(
            root, text="Smart Home Center", 
            font=("Segoe UI", 20, "bold"), bg="#e6e6e6", fg="#2c3e50"
        ).pack(pady=(15, 10))

        # Device Selection Frame
        frame_list = tk.LabelFrame(
            root, text="Select an Option", 
            font=("Segoe UI", 12, "bold"), bg="#e6e6e6", fg="#000000", padx=10, pady=10
        )
        frame_list.pack(fill="x", padx=20, pady=5)

        self.listbox = tk.Listbox(frame_list, height=5, font=("Consolas", 10), bd=1, relief="solid")
        self.listbox.pack(fill="x", padx=5, pady=5)
        self.refresh_list()

    #Buttons
        frame_btn = tk.Frame(root, bg="#e6e6e6")
        frame_btn.pack(pady=12)

        tk.Button(
            frame_btn, text="Turn On Device", command=self.turn_on,
            bg="#2b78e4", fg="white", font=("Segoe UI", 11, "bold"),
            activebackground="#1d5b8f", activeforeground="white",
            bd=0, padx=14, pady=6, cursor="hand2"
        ).grid(row=0, column=0, padx=6)

        tk.Button(
            frame_btn, text="Turn Off Device", command=self.turn_off,
            bg="#2b78e4", fg="white", font=("Segoe UI", 11, "bold"),
            activebackground="#1d5b8f", activeforeground="white",
            bd=0, padx=14, pady=6, cursor="hand2"
        ).grid(row=0, column=1, padx=6)

        # Log Panel
        self.log = scrolledtext.ScrolledText(
            root, height=7, font=("Consolas", 9), bg="#f8f9fa", fg="#333333", bd=1, relief="solid"
        )
        self.log.pack(fill="both", expand=True, padx=20, pady=(5, 15))

        self.write_log("Select an option above and click 'Turn On Device' or 'Turn Off Device'.")

    def write_log(self, msg: str):
        ts = datetime.now().strftime("%H:%M:%S")
        self.log.insert(tk.END, f"[{ts}] {msg}\n")
        self.log.see(tk.END)

    def refresh_list(self):
        self.listbox.delete(0, tk.END)
        for device in self.devices:
            self.listbox.insert(tk.END, str(device))

    def get_selected(self):
        sel = self.listbox.curselection()
        if sel:
            return self.devices[sel[0]]
        return None

    def turn_on(self):
        device = self.get_selected()
        if device:
            self.write_log(device.turn_on())
            self.refresh_list()

    def turn_off(self):
        device = self.get_selected()
        if device:
            self.write_log(device.turn_off())
            self.refresh_list()


# ==================== MAIN ====================

if __name__ == "__main__":
    devices = [
        SmartLight("Living Room Light", "Living Room"),
        SmartThermostat("Thermostat", "Hallway"),
        SmartSpeaker("Speaker", "Kitchen"),
        SmartCamera("Camera", "Entrance"),
    ]

    root = tk.Tk()
    app = SmartHomeGUI(root, devices)
    root.mainloop()