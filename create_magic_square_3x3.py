def build_gameboard():
    board = []
    for i in range(3):
        board_row = [0 for e in range(3)]
        board.append(board_row)
    return board


def coordinate_algorithm(board):
    x, y = 1, 2
    for value in range(1, 10):
        board[x][y] = value
        x, y = x - 1, y + 1
        if (x < 0) and (y > 2):
            x, y = 2, 0
        if (x < 0) and (y <= 2):
            x, y = 2, y
        if (x >= 0) and (y > 2):
            x, y = x, 0
        
        if board[x][y] != 0:
            if (0 <= x < 2) and (y == 2):
                x, y = x + 1, y - 2
            elif (x == 2) and (y == 2):
                x, y = 0, y - 2
            elif (x == 2) and (y < 2):
                if y == 1:
                    x, y = 0, 2
                elif y == 0:
                    x, y = 0, 1
        
    print('\n',*board, sep='\n')
    return board


def main():
    board = build_gameboard()
    coordinate_algorithm(board)


main()
