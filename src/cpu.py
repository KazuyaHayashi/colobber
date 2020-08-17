from typing import List

from .board import Move
from .search import min_max_search


def cpu_player(stone: int, board: List[List[int]]) -> Move:
    move = min_max_search(stone, board, 1)
    return move
