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


def print_turn(player: int):
    if player == O_STONE:
        print("O turn")
    else:
        print("X  turn")


def do_game():
    board = init_board()
    player = O_STONE
    player_routine = human_player
    while not has_finished(board):
        print_turn(player)
        print_board(board)

        # move = human_player(player, board)
        move = player_routine(player, board)
        print(f"Evaluated Moves: {peek.count_evaluated_moves}")
        print(f"ALPHA CUT: {peek.count_alpha_cut}")
        print(f"BETA CUT: {peek.count_beta_cut}")
        peek.count_evaluated_moves = 0
        peek.count_alpha_cut = 0
        peek.count_beta_cut = 0

        do_move(move, player, board)
        player = get_enemy_stone(player)

        if player_routine is human_player:
            player_routine = cpu_player
        else:
            player_routine = human_player

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
