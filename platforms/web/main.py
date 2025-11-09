from flask import Flask, render_template, request, session
from core.engine import start_game, make_guess
import random

app = Flask(__name__)
app.secret_key = "supersecret123"

def get_state():
    if 'state' not in session:
        session['state'] = vars(start_game('medium'))
    return session['state']

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

    # Rebuild object from dict
    game_obj = type('obj', (), {})()
    for k, v in state.items():
        setattr(game_obj, k, v)

    result = make_guess(game_obj, guess)
    session['state'] = vars(result['state'])  # ← CRITICAL: vars() = real dict

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

def run_web():
    app.run(host="0.0.0.0", port=5001, debug=False)