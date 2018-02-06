import sys, string


lst1 = [0,0,0,3,1,1,1,2]

def build_gameboard():
    board = []
    for i in range(4):
        board_row = [0 for e in range(4)]
        board.append(board_row)
    return board


def swap_values_interactively():
    prompt = input("Do you wish to switch some values interactively? (y,Y,yes,Yes) ")
    if prompt.lower() not in {"y", "yes"}:
        return [], [], None
    user_friendly = user_friendly_coordinates()
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
                        raise ValueError("ERROR: Has to be integers (0-9)!")
                coordinates_a.append(a) 
                coordinates_b.append(b)
        except ValueError as err:
            print(err)
        else:
            print("\nSuccessfully swapped values to [right/left].")
    return coordinates_a, coordinates_b, user_friendly


def process_lists(lst):
    remove_strings = [",", "(", ")", " ", "\"", "\'"]
    new_lst, items_lst = [], []
    try:
        for stringy in remove_strings:
            for n in range(len(lst)):    
                lst[n] = str(lst[n]).replace(stringy, "")
        for item in lst:
            if len(item) == 1:
                new_lst.append(item)
            if len(item) >= 2:
                for n in range(len(item)):
                    new_lst.append(item[n])
        for element in new_lst:
            if element not in string.digits:
                raise ValueError("\nERROR: Has to be integers (0-9)! "
                                 "\nList {0}: not processed".format(new_lst))
        for n in range(len(new_lst)):
            if n % 2 == 0:
                tuple_data = (new_lst[n], new_lst[n + 1])
                items_lst.append(tuple_data)
    except ValueError as err:
        print(err)
    else:
        print("List {0}: OK".format(new_lst))
    del lst, new_lst
    return items_lst


def swap_coordinates_from_file(filename=None):
    if filename is None:
        if len(sys.argv) > 1:
            filename = sys.argv[1]
        print("No filename input given. Exiting...")
    fh = None
    coordinates_a, coordinates_b = [], []
    try:
        fh = open(filename, encoding="utf-8")
        prompt = input("Create coordinate pairs for swapping on each line?"
                       "\n[default = coordinate pairs with mixed lines]: ")
        for lino, line in enumerate(fh, start=1):
            line_items = process_lists(list(line.strip()))
            if prompt.lower() not in {"y", "yes"}:
                if lino % 2 != 0:
                    coordinates_a += line_items
                else:
                    coordinates_b += line_items
            else:
                for n in range(len(line_items) - 1):
                    if n % 2 == 0:
                        coordinates_a.append(line_items[n])
                        coordinates_b.append(line_items[n + 1])
    except EnvironmentError as err:
        print(err)
    else:
        print("\nSuccessfully swapped values of the coordinates "
              "from one line with the other.\n")
    finally:
        if fh is not None:
            fh.close()
    return coordinates_a, coordinates_b, 0


def swap_coordinates_from_lists(coordinates_a_lst=None, 
                                coordinates_b_lst=None):
    if coordinates_a_lst is None or coordinates_b_lst is None:
        prompt = input("No lists given (or missing list).\n"
                       "Do you want to submit the sequences manually?: ")
        if prompt.lower() not in {"y", "yes"}:
            print("\nExiting...")
            return [], [], 0
        else:
            if not coordinates_a_lst:
                coordinates_a_lst = list(input("\nInput for sequence A: "))
            if not coordinates_b_lst:
                coordinates_b_lst = list(input("\nInput for sequence B: "))
            if not coordinates_a_lst or not coordinates_b_lst:
                print("\nERROR: Empty List/s. Exiting...")
                return [], [], 0
    try:
        coordinates_a = process_lists(coordinates_a_lst)
        coordinates_b = process_lists(coordinates_b_lst)
        if (len(coordinates_a) % 2 != 0 or len(coordinates_b) % 2 != 0 or
            len(coordinates_a) != len(coordinates_b)):
            raise ValueError("\nList A and List B must have the same number of "
                             "integers and it should be an even number. ")
    except ValueError as err:
        print(err)
        return [], [], 0
    else:
        print("\nSuccessfully swapped values on coordinates from "
              "'coordinates_a_lst' and 'coordinates_b_lst'.")
    return coordinates_a, coordinates_b, 0


def user_friendly_coordinates():
    prompt = input("User-friendly coordinates (without zeros)?")
    if prompt.lower() in {"y", "yes"}:
        return 1
    else:
        return 0


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
    print_board(board)
    a, b, user_friendly = swap_coordinates_from_file("swaptest.txt")
    for left, right in zip(a, b):
        x_a, y_a = (int(left[0]) - user_friendly), (int(left[1]) - user_friendly)
        x_b, y_b = (int(right[0]) - user_friendly), (int(right[1]) - user_friendly)
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
