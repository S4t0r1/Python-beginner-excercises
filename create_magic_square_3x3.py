def build_gameboard():
    board = []
    for i in range(3):
        board_row = [0 for e in range(3)]
        board.append(board_row)
    return board


def coordinate_algorithm(board):
    x, y = 1, 2
    minimum, maximum = 0, 2
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


def main():
    board = build_gameboard()
    coordinate_algorithm(board)


main()
