import random
from .board import scan_all_moves
from .search import min_max_search


def cpu_player(stone, board):
    move = min_max_search(stone, board, 3)
    return move
