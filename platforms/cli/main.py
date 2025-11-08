from core.engine import start_game, make_guess
from .display import *

def run_cli():
    print_welcome()
    while True:
        level = choose_difficulty()
        state = start_game(level)
        print(Fore.CYAN + f"\n{level.title()} Mode: {state.min_num}–{state.max_num}")
        
        while True:
            guess = get_guess(state.min_num, state.max_num)
            result = make_guess(state, guess)
            
            if result["correct"]:
                show_victory(result["attempts"], result["score"])
                if not ask_replay():
                    return
                break
            else:
                show_hint(result["hint"])