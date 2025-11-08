import os
os.environ["CTK_SCALING"] = "1.0" 

import customtkinter as ctk
import tkinter as tk
from .widgets.thermometer import Thermometer
from .widgets.confetti import Confetti
from core.engine import start_game, make_guess
from shared.sounds import play_sound

class GameWindow(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("Number Guessing Game Pro")
        self.geometry("600x500")
        self.minsize(600, 500)
        
        ctk.set_appearance_mode("dark")
        ctk.set_default_color_theme("blue")
        
        self.game_state = None
        self.confetti = None
        
        self.setup_ui()
        self.start_new_game("medium")
        
    def setup_ui(self):
        # Title
        title = ctk.CTkLabel(self, text="NUMBER GUESSING GAME", font=("Arial", 24, "bold"))
        title.pack(pady=20)
        
        # Main frame
        main_frame = ctk.CTkFrame(self)
        main_frame.pack(fill="both", expand=True, padx=40, pady=20)
        
        # Left: Game
        left = ctk.CTkFrame(main_frame)
        left.pack(side="left", fill="both", expand=True, padx=(0, 20))
        
        self.difficulty_var = ctk.StringVar(value="medium")
        diff_menu = ctk.CTkOptionMenu(
            left, values=["easy", "medium", "hard"],
            variable=self.difficulty_var, command=self.on_difficulty_change
        )
        diff_menu.pack(pady=10)
        
        self.range_label = ctk.CTkLabel(left, text="", font=("Arial", 14))
        self.range_label.pack(pady=5)
        
        input_frame = ctk.CTkFrame(left)
        input_frame.pack(pady=20)
        
        self.guess_entry = ctk.CTkEntry(input_frame, width=100, font=("Arial", 18), justify="center")
        self.guess_entry.pack(side="left", padx=5)
        self.guess_entry.bind("<Return>", lambda e: self.submit_guess())
        
        guess_btn = ctk.CTkButton(input_frame, text="GUESS", command=self.submit_guess)
        guess_btn.pack(side="left", padx=5)
        
        self.hint_label = ctk.CTkLabel(left, text="Enter your guess!", font=("Arial", 16), height=40)
        self.hint_label.pack(pady=10)
        
        stats = ctk.CTkFrame(left)
        stats.pack(pady=10, fill="x")
        self.attempts_label = ctk.CTkLabel(stats, text="Attempts: 0", font=("Arial", 14))
        self.attempts_label.pack(side="left", padx=20)
        self.score_label = ctk.CTkLabel(stats, text="Score: -", font=("Arial", 14))
        self.score_label.pack(side="right", padx=20)
        
        # Right: Thermometer
        thermo_frame = ctk.CTkFrame(main_frame, width=100)
        thermo_frame.pack(side="right", fill="y", padx=(20, 0))
        thermo_frame.pack_propagate(False)
        
        self.thermometer = Thermometer(thermo_frame)
        self.thermometer.pack(expand=True)
        
        # Bottom: Replay
        replay_btn = ctk.CTkButton(self, text="NEW GAME", command=self.new_game_prompt)
        replay_btn.pack(pady=10)
        
        # Theme toggle
        self.theme_var = ctk.StringVar(value="dark")
        theme_switch = ctk.CTkSwitch(self, text="Dark Mode", variable=self.theme_var,
                                    onvalue="dark", offvalue="light",
                                    command=self.toggle_theme)
        theme_switch.pack(pady=5)
        theme_switch.select()
        
    def start_new_game(self, level):
        self.game_state = start_game(level)
        self.update_range()
        self.hint_label.configure(text="Guess a number!")
        self.attempts_label.configure(text="Attempts: 0")
        self.score_label.configure(text="Score: -")
        self.thermometer.update_level(100)
        play_sound("beep.wav")
        
    def update_range(self):
        min_n, max_n = self.game_state.min_num, self.game_state.max_num
        self.range_label.configure(text=f"Range: {min_n} – {max_n}")
        
    def on_difficulty_change(self, level):
        self.start_new_game(level)
        
    def submit_guess(self):
        if not self.game_state:
            return
        try:
            guess = int(self.guess_entry.get())
            if not (self.game_state.min_num <= guess <= self.game_state.max_num):
                self.hint_label.configure(text="Out of range!", text_color="red")
                return
        except:
            self.hint_label.configure(text="Enter a number!", text_color="red")
            return
            
        play_sound("beep.wav")
        result = make_guess(self.game_state, guess)  
        
        self.attempts_label.configure(text=f"Attempts: {self.game_state.attempts}")  
        
        if result["correct"]:
            self.score_label.configure(text=f"Score: {result['score']}/1000")
            self.hint_label.configure(text="CORRECT! YOU WIN!", text_color="#00ff00")
            play_sound("win.wav")
            self.thermometer.update_level(0)
            self.after(500, self.show_confetti)
        else:
            self.hint_label.configure(text=result["hint"], text_color="#ffff00")
            diff = abs(guess - self.game_state.secret)  
            self.thermometer.update_level(diff)
            
        self.guess_entry.delete(0, "end")
        
    def show_confetti(self):
        if hasattr(self, "confetti_canvas"):
            self.confetti_canvas.destroy()
        canvas = tk.Canvas(self, width=500, height=400, highlightthickness=0, bg=self.cget("bg"))
        canvas.place(relx=0.5, rely=0.5, anchor="center")
        self.confetti_canvas = canvas
        self.confetti = Confetti(canvas)
        self.after(3000, lambda: canvas.destroy())
        
    def new_game_prompt(self):
        self.start_new_game(self.difficulty_var.get())
        
    def toggle_theme(self):
        mode = self.theme_var.get()
        ctk.set_appearance_mode(mode)