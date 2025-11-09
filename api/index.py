from flask import Flask, render_template, request, session
import os
import random

app = Flask(__name__, template_folder='templates', static_folder='static')
app.secret_key = os.getenv("SECRET_KEY", "fallback-secret-123")

# Game Logic (All Here — No External Imports)
class GameState:
    def __init__(self, level):
        self.level = level
        self.min_num, self.max_num = {"easy": (1, 50), "medium": (1, 100), "hard": (1, 200)}[level]
        self.secret = random.randint(self.min_num, self.max_num)
        self.attempts = 0

def start_game(level="medium"):
    return GameState(level)

def get_hint(diff):
    if diff <= 5:
        return "Very hot!"
    elif diff <= 10:
        return "Hot"
    elif diff <= 20:
        return "Warm"
    elif diff <= 50:
        return "Cold"
    else:
        return "Very cold"

def make_guess(state, guess):
    state.attempts += 1
    diff = abs(guess - state.secret)
    if guess == state.secret:
        score = max(100, 1000 - (state.attempts - 1) * 100)
        return {"correct": True, "score": score, "state": state}
    else:
        hint = get_hint(diff)
        return {"correct": False, "hint": hint, "state": state}

def get_state():
    if 'state' not in session:
        session['state'] = vars(start_game('medium'))
    return session['state']

# Routes
@app.route("/")
def index():
    return render_template("index.html")

@app.route("/game")
def game():
    state = get_state()
    diff = abs(state.get('secret', 50) - 50)
    thermo = max(0, 100 - diff * 2)
    color = "#1e90ff" if thermo < 30 else "#ffd700" if thermo < 60 else "#ff4500"
    return render_template("_game.html",
        level=state.get('level', 'medium'),
        min_num=state['min_num'], max_num=state['max_num'],
        feedback="Guess a number!", attempts=state['attempts'],
        score=0, won=False, thermo=thermo, thermo_color=color
    )

@app.route("/new", methods=["POST"])
def new_game():
    level = request.form.get("level", "medium")
    new_state = start_game(level)
    session['state'] = vars(new_state)
    return render_template("_game.html",
        level=level, min_num=new_state.min_num, max_num=new_state.max_num,
        feedback="Guess a number!", attempts=0, score=0, won=False,
        thermo=100, thermo_color="#1e90ff"
    )

@app.route("/guess", methods=["POST"])
def guess():
    state = get_state()
    try:
        guess = int(request.form["guess"])
    except:
        return render_template("_game.html", **state, feedback="Invalid number!", won=False, thermo=10, thermo_color="#ff0000")

    game_obj = type('obj', (), {})()
    for k, v in state.items():
        setattr(game_obj, k, v)

    result = make_guess(game_obj, guess)
    session['state'] = vars(result['state'])

    diff = abs(guess - result['state'].secret)
    thermo = 100 if result['correct'] else max(0, 100 - diff * 2)
    color = "#00ff00" if result['correct'] else "#1e90ff" if thermo < 30 else "#ffd700" if thermo < 60 else "#ff4500"

    return render_template("_game.html",
        level=result['state'].level,
        min_num=result['state'].min_num, max_num=result['state'].max_num,
        feedback="CORRECT! YOU WIN!" if result['correct'] else result['hint'],
        attempts=result['state'].attempts,
        score=result['score'] if result['correct'] else 0,
        won=result['correct'], thermo=thermo, thermo_color=color
    )

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)