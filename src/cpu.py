from typing import List

from .board import Move
from .search import min_max_search, alpha_beta_search


def cpu_player(stone: int, board: List[List[int]]) -> Move:
    #move = min_max_search(stone, board, 2)
    move = alpha_beta_search(stone, board, 2)
    return move
