import timeit
from typing import List

from .board import Move
from .search import min_max_search, alpha_beta_search, iterative_deepning_search


def cpu_player(stone: int, board: List[List[int]]) -> Move:
    # move = min_max_search(stone, board, 2)
    # res = timeit.timeit(lambda: alpha_beta_search(stone, board, 3),  number=1)
    # print(res)
    # move = alpha_beta_search(stone, board, 2)
    move = iterative_deepning_search(stone, board, max_depth=10, timelimit_in_seconds=3)
    return move
