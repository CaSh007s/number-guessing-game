import random

class GameState:
    def __init__(self, level):
        self.level = level
        self.min_num, self.max_num = {
            "easy": (1, 50),
            "medium": (1, 100),
            "hard": (1, 500)
        }[level]
        self.secret = random.randint(self.min_num, self.max_num)
        self.attempts = 0

def start_game(level="medium"):
    return GameState(level)

def get_hint(diff):
    if diff == 0:
        return "CORRECT!"
    elif diff <= 5:
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