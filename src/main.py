import random

from .board import (
    O_STONE,
    init_board,
    print_board,
    get_enemy_stone,
    has_finished,
    do_move,
)
from .cpu import cpu_player
from .human import human_player
from . import peek


def print_turn(player):
    if player == O_STONE:
        print("O turn")
    else:
        print("X  turn")


def do_game():
    board = init_board()
    player = O_STONE
    while not has_finished(board):
        print_turn(player)
        print_board(board)

        #move = human_player(player, board)
        move = cpu_player(player, board)
        print(peek.count_evaled_moves)
        peek.count_evaled_moves = 0
        do_move(move, player, board)
        player = get_enemy_stone(player)

    # Show result
    print_board(board)
    if player == O_STONE:
        print("X is winner")
    else:
        print("O is winner")


def main():
    do_game()


if __name__ == "__main__":
    main()
