from config import DIFFICULTY_RANGES

def get_range(level: str):
    level = level.lower()
    if level not in DIFFICULTY_RANGES:
        return DIFFICULTY_RANGES["medium"]
    return DIFFICULTY_RANGES[level]