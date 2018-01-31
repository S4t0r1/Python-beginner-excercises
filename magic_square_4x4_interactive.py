# User can choose which values to switch according to coordinates (x,y)/(xy)
import string

def build_gameboard():
    board = []
    for i in range(4):
        board_row = [0 for e in range(4)]
        board.append(board_row)
    return board


def swap_values():
    prompt = input("Do you wish to switch some values? (y,Y,yes,Yes)?")
    if prompt.lower() not in {"y", "yes"}:
        return [], []
    coordinates_a, coordinates_b = [], []
    while True:
        try:
            a = tuple(input("\nChoose x,y for left: ").replace(",", ""))
            b = tuple(input("\nChoose x,y for right: ").replace(",", ""))
            if not a or not b:
                break
            else:
                if len(a) != 2 or len(b) != 2:
                    raise ValueError("Can have only 2 numbers for [x,y /or xy]!")
                for value_a, value_b in zip(a, b):
                    if (value_a not in string.digits or 
                        value_b not in string.digits):
                        raise ValueError("Has to be integers (0-9)!")
                coordinates_a.append(a) 
                coordinates_b.append(b)
        except ValueError as err:
            print(err)
        else:
            print("Successfully swapped values to [right/left]")
    return coordinates_a, coordinates_b


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
    
    a, b = swap_values()
    for left, right in zip(a, b):
        x_a, y_a = int(left[0]), int(left[1])
        x_b, y_b = int(right[0]), int(right[1])
        board[x_a][y_a], board[x_b][y_b] = board[x_b][y_b], board[x_a][y_a]
    return board


def print_board(board):
    print("\n")
    for row in board:
        for element in row:
            print("{0:2d}".format(element), end="  ")
        print("\n")
    

def print_sums(board):
    sums = {}
    print("\n")
    for n in range(4):
        name = "row_{0}".format(n + 1)
        sums.update({name: [board[n][i] for i in range(4)]})
    for n in range(4):
        name = "col_{0}".format(n + 1)
        sums.update({name: [board[i][n] for i in range(4)]})
    sums.update({"diag_1": [board[i][i] for i in range(4)],
                 "diag_2": [board[3 - i][i] for i in range(4)]})
    
    for key, value in sums.items():
        summed_numbers = 0
        for number in sums[key]:
            summed_numbers += number
        print("{key}: {summed_numbers}".format(**locals()))


def main():
    board = build_gameboard()
    coordinate_algorithm(board)
    print_board(board)
    print_sums(board)


main()
