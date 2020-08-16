EMPTY = 0
O_STONE = 1
X_STONE = -1
MAX_BOARD_SIZE = 8


class MoveError(Exception):
    pass


class Position:
    def __init__(self, x, y):
        self.x = x
        self.y = y


class Move:
    def __init__(
        self, score=0, from_position=Position(0, 0), to_position=Position(0, 0)
    ):
        self.score = score
        self.from_position = from_position
        self.to_position = to_position


def init_board():
    return [
        [O_STONE, X_STONE, O_STONE, X_STONE, O_STONE, X_STONE, O_STONE, X_STONE],
        [X_STONE, O_STONE, X_STONE, O_STONE, X_STONE, O_STONE, X_STONE, O_STONE],
        [O_STONE, X_STONE, O_STONE, X_STONE, O_STONE, X_STONE, O_STONE, X_STONE],
        [X_STONE, O_STONE, X_STONE, O_STONE, X_STONE, O_STONE, X_STONE, O_STONE],
        [O_STONE, X_STONE, O_STONE, X_STONE, O_STONE, X_STONE, O_STONE, X_STONE],
        [X_STONE, O_STONE, X_STONE, O_STONE, X_STONE, O_STONE, X_STONE, O_STONE],
        [O_STONE, X_STONE, O_STONE, X_STONE, O_STONE, X_STONE, O_STONE, X_STONE],
        [X_STONE, O_STONE, X_STONE, O_STONE, X_STONE, O_STONE, X_STONE, O_STONE],
    ]


def print_board(board):
    print("  A B C D E F G H (X)")
    for y in range(MAX_BOARD_SIZE):
        print(y + 1, end=" ")
        for x in range(MAX_BOARD_SIZE):
            if board[y][x] == O_STONE:
                print("O", end=" ")
            elif board[y][x] == X_STONE:
                print("X", end=" ")
            else:
                print("*", end=" ")
        print("\n")
    print("Y")


def is_valid_board_index(index):
    if index < 0:
        return False
    if index >= MAX_BOARD_SIZE:
        return False

    return True


def get_enemy_stone(player_stone):
    return player_stone * -1


def scan_all_moves(player, board):
    moves = []
    enemy = get_enemy_stone(player)
    for y in range(MAX_BOARD_SIZE):
        for x in range(MAX_BOARD_SIZE):
            if board[y][x] != player:
                continue

            if is_valid_board_index(y - 1):
                if board[y - 1][x] == enemy:
                    moves.append(
                        Move(
                            from_position=Position(x, y), to_position=Position(x, y - 1)
                        )
                    )
            if is_valid_board_index(y + 1):
                if board[y + 1][x] == enemy:
                    moves.append(
                        Move(
                            from_position=Position(x, y), to_position=Position(x, y + 1)
                        )
                    )
            if is_valid_board_index(x - 1):
                if board[y][x - 1] == enemy:
                    moves.append(
                        Move(
                            from_position=Position(x, y), to_position=Position(x - 1, y)
                        )
                    )
            if is_valid_board_index(x + 1):
                if board[y][x + 1] == enemy:
                    moves.append(
                        Move(
                            from_position=Position(x, y), to_position=Position(x + 1, y)
                        )
                    )

    return moves


def scan_moves_at(stone_from, player, board):
    moves = []
    enemy = get_enemy_stone(player)
    y = stone_from.y
    x = stone_from.x
    if is_valid_board_index(y - 1):
        if board[y - 1][x] == enemy:
            moves.append(Move(from_position=stone_from, to_position=Position(x, y - 1)))
    if is_valid_board_index(y + 1):
        if board[y + 1][x] == enemy:
            moves.append(Move(from_position=stone_from, to_position=Position(x, y + 1)))
    if is_valid_board_index(x - 1):
        if board[y][x - 1] == enemy:
            moves.append(Move(from_position=stone_from, to_position=Position(x - 1, y)))
    if is_valid_board_index(x + 1):
        if board[y][x + 1] == enemy:
            moves.append(Move(from_position=stone_from, to_position=Position(x + 1, y)))
    return moves


def has_finished(board):
    O_moves = scan_all_moves(O_STONE, board)
    if len(O_moves) > 0:
        return False

    X_moves = scan_all_moves(X_STONE, board)
    if len(X_moves) > 0:
        return False

    return True


def is_valid_move(move, player_stone, board):
    # check board index range
    if not is_valid_board_index(move.from_position.x):
        return False
    if not is_valid_board_index(move.from_position.y):
        return False
    if not is_valid_board_index(move.to_position.x):
        return False
    if not is_valid_board_index(move.to_position.y):
        return False

    # check stone stone
    enemy_stone = get_enemy_stone(player_stone)
    if board[move.from_position.y][move.from_position.x] != player_stone:
        return False
    if board[move.to_position.y][move.to_position.x] != enemy_stone:
        return False

    return True


def do_move(move, player_stone, board):
    if not is_valid_move(move, player_stone, board):
        raise MoveError("Invalid Move")

    board[move.from_position.y][move.from_position.x] = EMPTY
    board[move.to_position.y][move.to_position.x] = player_stone
    return board
