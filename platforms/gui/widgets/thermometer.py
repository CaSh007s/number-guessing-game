import customtkinter as ctk
import tkinter as tk

class Thermometer(ctk.CTkCanvas):
    def __init__(self, parent):
        super().__init__(parent, width=60, height=300, highlightthickness=0, bg="#1e1e1e")
        self.pack_propagate(False)
        self.configure(width=60, height=300)
        
        self.level = 0  # 0 = cold, 100 = hot
        self.create_thermometer()
        
    def create_thermometer(self):
        # Outline
        self.create_rectangle(20, 20, 40, 280, outline="#555", width=3)
        # Bulb
        self.create_oval(10, 270, 50, 310, outline="#555", width=3, fill="#333")
        
        # Fill
        self.fill_id = self.create_rectangle(22, 278, 38, 278, fill="#1e90ff", outline="")
        
    def update_level(self, diff: int):
        # diff: 0 = correct, >50 = cold
        if diff == 0:
            self.level = 100
        else:
            self.level = max(0, 100 - (diff * 2))
            self.level = min(100, self.level)
        
        y = 278 - (258 * self.level / 100)
        self.coords(self.fill_id, 22, y, 38, 278)
        
        # Color gradient
        if self.level > 80:
            color = "#ff4500"  # Red hot
        elif self.level > 50:
            color = "#ff8c00"  # Orange
        elif self.level > 20:
            color = "#ffd700"  # Yellow
        else:
            color = "#1e90ff"  # Blue cold
        self.itemconfig(self.fill_id, fill=color)