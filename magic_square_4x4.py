
def build_gameboard():
    board = []
    for i in range(4):
        board_row = [0 for e in range(4)]
        board.append(board_row)
    return board


def coordinate_algorithm(board):
    value = 1
    x, y = 0, 0
    minimum, maximum = 0, (4 - 1)
    while value < 17:
        for row in board:
            for element in row:
                board[x][y] = value
                value += 1
                y += 1
            x += 1
            if (x < minimum) and (y > maximum):
                x, y = maximum, minimum
            if (x < minimum) and (y <= maximum):
                x, y = maximum, y
            if (x >= minimum) and (y > maximum):
                x, y = x, minimum
    
    board[0][0], board[3][3] = board[3][3], board[0][0]
    board[0][3], board[3][0] = board[3][0], board[0][3]
    board[1][1], board[2][2] = board[2][2], board[1][1]
    board[1][2], board[2][1] = board[2][1], board[1][2]
    
    print('\n',*board, sep='\n')
    return board


def print_sums(board):
    sums = {"row_1": [board[0][i] for i in range(4)],
            "row_2": [board[1][i] for i in range(4)],
            "row_3": [board[2][i] for i in range(4)],
            "row_4": [board[3][i] for i in range(4)],
            "col_1": [board[i][0] for i in range(4)],
            "col_2": [board[i][1] for i in range(4)],
            "col_3": [board[i][2] for i in range(4)],
            "col_4": [board[i][3] for i in range(4)],
            "diag_1": [board[i][i] for i in range(4)],
            "diag_2": [board[3 - i][i] for i in range(4)]}
    for key, value in sums.items():
        summed_numbers = 0
        for number in sums[key]:
            summed_numbers += number
        print("{key}: {summed_numbers}".format(**locals()))


def main():
    board = build_gameboard()
    coordinate_algorithm(board)
    print_sums(board)


main()
