import random
from typing import List

MAX_SCORE = 100
MIN_SCORE = -100


def evaluate(board: List[List[int]]) -> int:
    return random.randint(MIN_SCORE, MAX_SCORE)
