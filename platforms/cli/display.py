from colorama import Fore, Style, init
init(autoreset=True)

def print_welcome():
    print(Fore.CYAN + Style.BRIGHT + """
    ╔════════════════════════════════════╗
    ║      NUMBER GUESSING GAME PRO      ║
    ╚════════════════════════════════════╝
    """)

def choose_difficulty() -> str:
    print(Fore.YELLOW + "Choose difficulty:")
    print("1. Easy (1–50)")
    print("2. Medium (1–100)")
    print("3. Hard (1–200)")
    while True:
        c = input(Fore.WHITE + "> ").strip()
        if c == "1": return "easy"
        if c == "2": return "medium"
        if c == "3": return "hard"
        print(Fore.RED + "Pick 1, 2, or 3.")

def get_guess(min_num: int, max_num: int) -> int:
    while True:
        try:
            g = input(Fore.WHITE + f"Guess ({min_num}–{max_num}): ")
            num = int(g)
            if min_num <= num <= max_num:
                return num
            print(Fore.RED + f"Must be {min_num}–{max_num}")
        except:
            print(Fore.RED + "Enter a number!")

def show_hint(hint: str):
    print(Fore.MAGENTA + hint)

def show_victory(attempts: int, score: int):
    print(Fore.GREEN + Style.BRIGHT + f"\nCORRECT! Attempts: {attempts}")
    print(Fore.YELLOW + f"Score: {score}/1000")
    print(Fore.CYAN + "Thanks for playing!")

def ask_replay() -> bool:
    while True:
        r = input(Fore.WHITE + "\nPlay again? (y/n): ").lower()
        if r in ["y", "yes"]: return True
        if r in ["n", "no"]: return False
        print(Fore.RED + "y or n?")