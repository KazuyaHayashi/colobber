from typing import List
from copy import deepcopy
from .board import Move, scan_all_moves, do_move, get_enemy_stone, has_finished
from .evaluate import MIN_SCORE, MAX_SCORE, evaluate
from . import peek


INITIAL_ALPHA_SCORE = MIN_SCORE * 2
INITIAL_BETA_SCORE = MAX_SCORE * 2


def min_max_search(
    stone: int, board: List[List[int]], depth: int, mine_turn=True
) -> Move:
    if depth <= 0:
        peek.count_evaluated_moves += 1
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


def alpha_beta_search(
    stone: int, board: List[List[int]], depth: int, mine_turn=True, alpha=INITIAL_ALPHA_SCORE, beta=INITIAL_BETA_SCORE
) -> Move:
    if depth <= 0:
        peek.count_evaluated_moves += 1
        return Move(score=evaluate(board))

    if has_finished(board):
        if mine_turn:
            return Move(score=MIN_SCORE)
        else:
            return Move(score=MAX_SCORE)

    all_moves = scan_all_moves(stone, board)

    candidate_move = Move(score=0)
    if mine_turn:
        for move in all_moves:
            virtual_board = deepcopy(board)
            do_move(move, stone, virtual_board)
            opponent_stone = get_enemy_stone(stone)
            evaluated_move = alpha_beta_search(
                opponent_stone, virtual_board, depth - 1, not mine_turn, alpha, beta
            )
            if evaluated_move.score > alpha:
                alpha = evaluated_move.score
                move.score = evaluated_move.score
                candidate_move = move
                if alpha >= beta:
                    #print(f"ALPHA Cutting. alpha: {alpha}, beta: {beta}")
                    break
        return candidate_move
    else:
        for move in all_moves:
            virtual_board = deepcopy(board)
            do_move(move, stone, virtual_board)
            opponent_stone = get_enemy_stone(stone)
            evaluated_move = alpha_beta_search(
                opponent_stone, virtual_board, depth - 1, not mine_turn, alpha, beta
            )
            if evaluated_move.score < beta:
                beta = evaluated_move.score
                move.score = evaluated_move.score
                candidate_move = move
                if beta <= alpha:
                    #print(f"BETA Cutting. alpha: {alpha}, beta: {beta}")
                    break
        return candidate_move