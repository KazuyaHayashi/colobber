from .board import (
    Position,
    is_valid_board_index,
    scan_moves_at,
)


def is_player_stone(stone_position, player, board):
    if board[stone_position.y][stone_position.x] == player:
        return True
    return False


def get_X(label: str) -> int:
    while 1:
        value = input(label)
        try:
            index = ord(str(value).upper()) - ord("A")
            if is_valid_board_index(index):
                return index
            continue
        except ValueError:
            continue


def get_Y(label: str) -> int:
    while 1:
        value = input(label)
        try:
            index = int(value) - 1
            if is_valid_board_index(index):
                return int(value) - 1
            continue
        except ValueError:
            continue


def human_player(stone, board):
    while 1:
        from_x = get_X("FROM X (A to H):")
        from_y = get_Y("FROM Y (1 to 9):")
        from_position = Position(from_x, from_y)
        if not is_player_stone(from_position, stone, board):
            continue
        moves = scan_moves_at(from_position, stone, board)
        if len(moves) > 0:
            break

    while 1:
        for i in range(len(moves)):
            print(
                "%d: Move to %s, %d"
                % (
                    i + 1,
                    chr(moves[i].to_position.y + ord("A")),
                    moves[i].to_position.x + 1,
                )
            )
        selection = int(input("Choose number:")) - 1
        if selection > -1 and selection < len(moves):
            return moves[selection]
