def build_gameboard():
    board = []
    for i in range(3):
        board_row = [0 for e in range(3)]
        board.append(board_row)
    return board


def coordinate_algorithm(board):
    x, y = 1, 2
    minimum, maximum = 0, (3 - 1)
    for value in range(1, 10):
        board[x][y] = value
        x, y = x - 1, y + 1
        if (x < minimum) and (y > maximum):
            x, y = maximum, minimum
        if (x < minimum) and (y <= maximum):
            x, y = maximum, y
        if (x >= minimum) and (y > maximum):
            x, y = x, minimum
        
        if board[x][y] != 0:
            if (minimum <= x < maximum):
                x = x + 1
            elif x == maximum:
                x = minimum
            
            if (2 <= y <= maximum):
                y = y - 2
            elif y == 1:
                y = maximum
            elif y == 0:
                y = maximum - 1
        
    print('\n',*board, sep='\n')
    return board


def print_sums(board):
    sums = {"row_1": [board[0][i] for i in range(3)],
            "row_2": [board[1][i] for i in range(3)],
            "row_3": [board[2][i] for i in range(3)],
            "col_1": [board[i][0] for i in range(3)],
            "col_2": [board[i][1] for i in range(3)],
            "col_3": [board[i][2] for i in range(3)],
            "diag_1": [board[i][i] for i in range(3)],
            "diag_2": [board[2 - i][i] for i in range(3)]}
    print("\n")
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
