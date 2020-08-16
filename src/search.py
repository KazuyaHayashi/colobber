from copy import deepcopy
from .board import Move, scan_all_moves, do_move, get_enemy_stone, has_finished
from .evaluate import MIN_SCORE, MAX_SCORE, evaluate
from . import peek


def min_max_search(stone, board, depth, mine_turn=True):
    if depth <= 0:
        peek.count_evaled_moves += 1
        return Move(score=evaluate(board))

    if has_finished(board):
        if mine_turn:
            return Move(score=MIN_SCORE)
        else:
            return Move(score=MAX_SCORE)

    all_moves = scan_all_moves(stone, board)

    candidate_move = Move(score=0)
    if mine_turn:
        max_score = MIN_SCORE - 1
        for move in all_moves:
            virtual_board = deepcopy(board)
            do_move(move, stone, virtual_board)
            opponent_stone = get_enemy_stone(stone)
            evaluated_move = min_max_search(
                opponent_stone, virtual_board, depth - 1, not mine_turn
            )
            if evaluated_move.score > max_score:
                max_score = evaluated_move.score
                move.score = evaluated_move.score
                candidate_move = move
        return candidate_move
    else:
        min_score = MAX_SCORE + 1
        for move in all_moves:
            virtual_board = deepcopy(board)
            do_move(move, stone, virtual_board)
            opponent_stone = get_enemy_stone(stone)
            evaluated_move = min_max_search(
                opponent_stone, virtual_board, depth - 1, not mine_turn
            )
            if evaluated_move.score < min_score:
                min_score = evaluated_move.score
                move.score = evaluated_move.score
                candidate_move = move
        return candidate_move
