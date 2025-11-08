def calculate_score(attempts: int, max_range: int) -> int:
    base = 1000
    penalty = attempts * 12
    bonus = max(0, (max_range - attempts * 2) // 3)
    return max(100, base - penalty + bonus)