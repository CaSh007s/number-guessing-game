from dataclasses import dataclass
from typing import Optional

@dataclass
class GameState:
    secret: int
    min_num: int
    max_num: int
    attempts: int = 0
    prev_diff: Optional[int] = None
    score: Optional[int] = None