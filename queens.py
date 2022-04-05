from os import system, name

NO_COL = 8
NO_ROW = 8

ROW_POSITION = 0
COL_POSITION = 1
QUEEN_MARK = 1
QUEEN_EMOJI = 'Q '


def get_row_text(row):
    row_str = ""
    for cell in row:
        row_str += "║"
        if cell == 1:
            row_str += f" {QUEEN_EMOJI} "
        else:
            row_str += "    "
    row_str += "║"
    return row_str


def print_chess_borad(board):
    CELL_WIDTH = 4

    header = f"╔{(CELL_WIDTH * '═' + '╦') * NO_COL}"[:-1] + "╗"
    separa = f"╠{(CELL_WIDTH * '═' + '╬') * NO_COL}"[:-1] + "╣"
    footer = f"╚{(CELL_WIDTH * '═' + '╩') * NO_COL}"[:-1] + "╝"

    print(header)
    for row in range(NO_ROW):
        print(get_row_text(board[row]))
        if row != NO_ROW - 1:
            print(separa)
    print(footer)


def generate_empty_board():
    board = [[0 for _ in range(NO_COL)] for _ in range(NO_ROW)]
    return board


def is_in_same_row(position_reference, position):
    if get_row_position(position_reference) == get_row_position(position):
        return True
    else:
        return False


def is_in_same_diagonal(reference_position, position):
    if(abs(get_row_position(reference_position) - get_row_position(position))) == \
      (abs(get_col_position(reference_position) - get_col_position(position))):
        return True
    else:
        return False


def get_row_position(position):
    return position[ROW_POSITION]


def get_col_position(position):
    return position[COL_POSITION]


def is_valid_position(queens_row, position):
    for col in range(0, 8):
        if queens_row[col] == 0:
            break
        reference_position = (queens_row[col], col + 1)
        if is_in_same_row(reference_position, position):
            return False
        if is_in_same_diagonal(reference_position, position):
            return False
    return True


def place_queen(board, position):
    board[get_row_position(position)][get_col_position(position)] = QUEEN_MARK


def transform_row_to_board(row, board):
    for col in range(0, 8):
        position = row[col] - 1, col
        place_queen(board, position)


def get_next_possible_pos(queens_row, row, col):
    row = queens_row[col - 2] + 1
    queens_row[col - 2] = 0
    col -= 1
    return row, col


def place_queens_generator(queens_row, row, col):
    while 8 >= col >= 0:
        valid_position = False
        while row <= 8:
            position = row, col
            valid_position = is_valid_position(queens_row, position)
            if valid_position:
                break
            row += 1
        if valid_position:
            queens_row[col - 1] = row
            row = 1
            col += 1
        else:
            row, col = get_next_possible_pos(queens_row, row, col)
            while row > 8:
                row, col = get_next_possible_pos(queens_row, row, col)
        if col == 9:
            col = 8
            row = queens_row[7] + 1
            yield queens_row


def clear_screen():
    system('cls' if name == 'nt' else 'clear') 


def get_user_input():
    return input("Press Enter to generate the next solution!")


def main():
    queens_row = [0 for _ in range(8)]
    queens_row[0] = 1

    queen_place_gen = place_queens_generator(queens_row, 1, 2)

    while get_user_input() == "":
        solution = next(queen_place_gen)
        clear_screen()
        
        board = generate_empty_board()
        transform_row_to_board(solution, board)
        print_chess_borad(board)


if __name__ == "__main__":
    main()