def board_size():
    return int(input("Choose 'N' size for magic_square [NxN]: "))


def build_gameboard(size):
    board = []
    for i in range(size):
        board_row = [0 for e in range(size)]
        board.append(board_row)
    return board


def coordinate_algorithm(board, size):
    x, y = 2, 3
    minimum, maximum = 0, size - 1
    for value in range(1, ((size ** 2) + 1)):
        board[x][y] = value
        x, y = x - 1, y + 1
        if (x < minimum) and (y > maximum):
            x, y = maximum, minimum
        if (x < minimum) and (y <= maximum):
            x, y = maximum, y
        if (x >= minimum) and (y > maximum):
            x, y = x, minimum
        
        if board[x][y] != 0:
            if (minimum <= x < (maximum - 1)):
                x = x + 2
            elif x == (maximum - 1):
                x = minimum
            elif x == maximum:
                x = minimum + 1
            
            if (1 <= y <= maximum):
                y = y - 1
            elif y == 1:
                y = minimum
            elif y == 0:
                y = maximum
                
        
    print('\n',*board, sep='\n')
    return board


def main():
    size = board_size()
    board = build_gameboard(size)
    coordinate_algorithm(board, size)


main()
