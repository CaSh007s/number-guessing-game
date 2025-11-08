import random
from .state import GameState
from .scorer import calculate_score
from .difficulty import get_range

def start_game(level: str = "medium") -> GameState:
    min_num, max_num = get_range(level)
    secret = random.randint(min_num, max_num)
    return GameState(secret=secret, min_num=min_num, max_num=max_num)

def make_guess(state: GameState, guess: int) -> dict:
    state.attempts += 1
    diff = abs(guess - state.secret)
    
    if guess == state.secret:
        state.score = calculate_score(state.attempts, state.max_num)
        return {"correct": True, "score": state.score, "attempts": state.attempts}
    
    hint = "Too high!" if guess > state.secret else "Too low!"
    warmth = (
        "SCORCHING!" if diff <= 5 else
        "Warm!" if diff <= 10 else
        "Getting closer..." if diff <= 20 else
        "Cold!"
    )
    if state.prev_diff is not None:
        warmth += " (Warmer!)" if diff < state.prev_diff else " (Colder)"
    
    state.prev_diff = diff
    return {"correct": False, "hint": f"{hint} {warmth}"}