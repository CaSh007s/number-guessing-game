import customtkinter as ctk
import tkinter as tk
import random
import math

class Confetti:
    def __init__(self, canvas: tk.Canvas):
        self.canvas = canvas
        self.particles = []
        self.create_confetti()
        
    def create_confetti(self):
        colors = ["#ff0000", "#00ff00", "#0000ff", "#ffff00", "#ff00ff", "#00ffff"]
        for _ in range(100):
            x = random.randint(0, 500)
            y = random.randint(-100, 0)
            size = random.randint(4, 8)
            color = random.choice(colors)
            speed = random.uniform(2, 6)
            angle = random.uniform(-45, 45)
            particle = {
                "id": self.canvas.create_oval(x, y, x+size, y+size, fill=color, outline=""),
                "x": x, "y": y,
                "vx": math.cos(math.radians(angle)) * speed,
                "vy": -speed,
                "size": size,
                "color": color
            }
            self.particles.append(particle)
        self.animate()
        
    def animate(self):
        for p in self.particles[:]:
            p["x"] += p["vx"]
            p["y"] += p["vy"]
            p["vy"] += 0.3  # gravity
            p["vx"] *= 0.99  # air resistance
            
            self.canvas.coords(p["id"], p["x"], p["y"], p["x"]+p["size"], p["y"]+p["size"])
            
            if p["y"] > 400:
                self.canvas.delete(p["id"])
                self.particles.remove(p)
        
        if self.particles:
            self.canvas.after(30, self.animate)