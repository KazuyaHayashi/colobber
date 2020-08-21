import time
from typing import List
from copy import deepcopy
from .board import Move, scan_all_moves, do_move, get_enemy_stone, has_finished
from .evaluate import MIN_SCORE, MAX_SCORE, evaluate
from . import peek


INITIAL_ALPHA_SCORE = MIN_SCORE * 2
INITIAL_BETA_SCORE = MAX_SCORE * 2


class TimeLimitExceededError(Exception):
    pass


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
    stone: int,
    board: List[List[int]],
    depth: int,
    mine_turn=True,
    alpha=INITIAL_ALPHA_SCORE,
    beta=INITIAL_BETA_SCORE,
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
                    peek.count_alpha_cut += 1
                    # print(f"ALPHA Cutting. alpha: {alpha}, beta: {beta}")
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
                    peek.count_beta_cut += 1
                    # print(f"BETA Cutting. alpha: {alpha}, beta: {beta}")
                    break
        return candidate_move


def alpha_beta_search_with_timelimit(
    stone: int,
    board: List[List[int]],
    depth: int,
    timelimit_in_seconds: int,
    start_time: float,
    mine_turn=True,
    alpha=INITIAL_ALPHA_SCORE,
    beta=INITIAL_BETA_SCORE,
) -> Move:
    if time.time() - start_time > timelimit_in_seconds:
        raise TimeLimitExceededError()
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
            evaluated_move = alpha_beta_search_with_timelimit(
                opponent_stone,
                virtual_board,
                depth - 1,
                timelimit_in_seconds,
                start_time,
                not mine_turn,
                alpha,
                beta,
            )
            if evaluated_move.score > alpha:
                alpha = evaluated_move.score
                move.score = evaluated_move.score
                candidate_move = move
                if alpha >= beta:
                    peek.count_alpha_cut += 1
                    # print(f"ALPHA Cutting. alpha: {alpha}, beta: {beta}")
                    break
        return candidate_move
    else:
        for move in all_moves:
            virtual_board = deepcopy(board)
            do_move(move, stone, virtual_board)
            opponent_stone = get_enemy_stone(stone)
            evaluated_move = alpha_beta_search_with_timelimit(
                opponent_stone,
                virtual_board,
                depth - 1,
                timelimit_in_seconds,
                start_time,
                not mine_turn,
                alpha,
                beta,
            )
            if evaluated_move.score < beta:
                beta = evaluated_move.score
                move.score = evaluated_move.score
                candidate_move = move
                if beta <= alpha:
                    peek.count_beta_cut += 1
                    # print(f"BETA Cutting. alpha: {alpha}, beta: {beta}")
                    break
        return candidate_move


def iterative_deepning_search(
    stone: int, board: List[List[int]], max_depth: int, timelimit_in_seconds=10
) -> Move:
    depth = 1
    current_move = Move()
    start_time = time.time()

    while depth < max_depth:
        try:
            print(f"current depth: {depth}")
            current_move = alpha_beta_search_with_timelimit(
                stone,
                board,
                depth,
                timelimit_in_seconds=timelimit_in_seconds,
                start_time=start_time,
            )
            depth += 1
            from_x = chr(current_move.from_position.x + ord("A"))
            to_x = chr(current_move.to_position.x + ord("A"))
            print(
                f"best move: Score={current_move.score}, from=({from_x}, {current_move.from_position.y + 1}), to=({to_x}, {current_move.to_position.y + 1})"
            )
        except TimeLimitExceededError:
            break

    return current_move
