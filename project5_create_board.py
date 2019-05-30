

def create_board(row:int, column: int) -> [[]]:
    '''creates the board with the given number of rows and columns'''
    board = []
    for num in range(row):
        row_list = []
        for item in range(column):
            row_list.append('.')
        board.append(row_list)

    return board

def print_board(board: [[]]):
    '''prints the board with the given board list'''
    for row in board:
        row_print = ""
        for column in row:
            row_print += column + " "
        print(row_print)


def middle_four(board:[[]], top_left:str, row:int, column:int) -> [[]]:
    '''updates the board to have the miiddle four black and white discs'''
    new_board = board
    middle_row = row/2

    middle_column = column/2

    if top_left == 'B':
        new_board[int(middle_row-1)][int(middle_column-1)] = 'B'
        new_board[int(middle_row-1)][int(middle_column)] = 'W'
        new_board[int(middle_row)][int(middle_column-1)] = 'W'
        new_board[int(middle_row)][int(middle_column)] = 'B'
    elif top_left == 'W':
        new_board[int(middle_row-1)][int(middle_column-1)] = 'W'
        new_board[int(middle_row-1)][int(middle_column)] = 'B'
        new_board[int(middle_row)][int(middle_column-1)] = 'B'
        new_board[int(middle_row)][int(middle_column)] = 'W'

    return new_board
