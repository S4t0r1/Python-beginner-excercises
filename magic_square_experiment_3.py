import sys, string, argparse


lst1 = [0,0,0,3,1,1,1,2]


def main():
    option = None
    action, method = input_actions_methods()
    board = build_gameboard()
    if "c" in action:
        board = build_gameboard()
    if "e" in action:
        filename = "swaptest.txt" if "f" in method else None
        lst = lst1 if "s" in method else None
        option = (swap_coordinates_from_file(filename) if "f" in method
                 else swap_coordinates_from_lists(lst) if "s" in method
                 else swap_values_manually() if "m" in method
                 else None)
    check_if_magic_square = True if "i" in action else False
    coordinate_algorithm(board, option)
    print_sums(board, check_if_magic_square)


def input_actions_methods():
    prompt_action = input("[C]reate [E]dit [I]nspect: ")
    if prompt_action in "CEI".lower():
        prompt_method = input("[F]ile [S]eq [M]anually: ")
        if prompt_method in "FSM".lower():
            return prompt_action.lower(), prompt_method.lower()


def cmd_options():
    usage = """%prog [options] [filename]
Filename is optional"""
    parser = argparse.ArgumentParser(usage=usage)
    parser.add_argument("-f", "--file", dest="file",
                        action="store_true",
                        help=("Uses file for creating/editing/inspecting magic-square"
                              "\n[default: off]"))
    parser.add_argument("-seq", "--sequence", dest="sequence",
                        action="store_true",
                        help=("Uses sequence(s) for creating/editing/inspecting magic-square"
                              "\n[default: off]"))
    parser.add_argument("-m", "--manually", dest="manually",
                        action="store_true",
                        help=("Uses manual input for creating/editing/inspecting magic-square"
                              "\n[default: off]"))
    parser.add_argument("-ins", "--inspect", dest="inspect",
                        action="store_true",
                        help=("Inspects the if it's a magic-square"
                              "\n[default: off]"))
    parser.add_argument("-e", "--edit", dest="edit",
                        action="store_true",
                        help=("Specialises to edit a magic-square (combined with -f, -seq or -int)"
                              "\n[default: off]"))
    parser.add_argument("-c", "--create", dest="create",
                        action="store_true",
                        help=("Specialises to create a magic-square"
                              "\n[default: off]"))
    args = parser.parse_args()
    return args


def build_gameboard():
    board = []
    for i in range(4):
        board_row = [0 for e in range(4)]
        board.append(board_row)
    value = 1
    for x in range(4):
        for y in range(4):
            board[x][y] += value
            value += 1
    print_board(board)
    return board


def process_lists(lst):
    remove_chars = {c for c in string.punctuation + string.whitespace + "\ufeff"}
    lst = [str(c) for c in lst if str(c) not in remove_chars]
    try:
        for element in lst:
            if element not in string.digits:
                raise ValueError("\nERROR: Has to be integers (0-9)! "
                                 "\nList {0}: not processed".format(lst))
        items_lst = []
        for n in range(len(lst)):
            if n % 2 == 0:
                tuple_data = (lst[n], lst[n + 1])
                items_lst.append(tuple_data)
    except ValueError as err:
        print(err)
    else:
        print("List {0}: OK".format(lst))
    del lst
    return items_lst


def swap_values_manually():
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


def swap_coordinates_from_file(filename=None):
    if filename is None:
        if len(sys.argv) > 1:
            filename = sys.argv[1]
        print("No filename input given. Exiting...")
        sys.exit(2)
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
        print("\nSuccessfully swapped values")
    finally:
        if fh is not None:
            fh.close()
    return coordinates_a, coordinates_b, 0


def swap_coordinates_from_lists(coordinates_a_lst=None, 
                                coordinates_b_lst=None):
    if coordinates_a_lst is None or coordinates_b_lst is None:
        prompt = input("No lists given (or missing list).\n"
                       "Present list {0}\n"
                       "Do you want to submit the sequences manually?: "
                       .format(coordinates_a_lst if coordinates_a_lst 
                          else coordinates_b_lst if coordinates_b_lst
                          else "'None'"))
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


def coordinate_algorithm(board, option=None):
    x, y = 0, 0
    minimum, maximum = 0, (4 - 1)
    if (x < minimum) and (y > maximum):
        x, y = maximum, minimum
    if (x < minimum) and (y <= maximum):
        x, y = maximum, y
    if (x >= minimum) and (y > maximum):
        x, y = x, minimum
    if option:
        a, b, user_friendly = option
        for left, right in zip(a, b):
            x_a, y_a = (int(left[0]) - user_friendly), (int(left[1]) - user_friendly)
            x_b, y_b = (int(right[0]) - user_friendly), (int(right[1]) - user_friendly)
            board[x_a][y_a], board[x_b][y_b] = board[x_b][y_b], board[x_a][y_a]
    print_board(board)
    return board


def print_board(board):
    print("\n")
    for row in board:
        for element in row:
            print("{0:2d}".format(element), end="  ")
        print("\n")
    

def print_sums(board, check_if_magic_square=False):
    sums = {}
    print("\n")
    for n in range(4):
        name = "row_{0}".format(n + 1)
        sums.update({name: {board[n][i] for i in range(4)}})
    for n in range(4):
        name = "col_{0}".format(n + 1)
        sums.update({name: {board[i][n] for i in range(4)}})
    sums.update({"diag_1": {board[i][i] for i in range(4)},
                 "diag_2": {board[3 - i][i] for i in range(4)}})
    for key in sums.keys():
        summed_numbers = sum(sums[key])
        print("{key}: {summed_numbers}".format(**locals()))
    if check_if_magic_square:
        next_value_sum = sum(next(iter(sums.values())))
        check_magic = all(sum(value) == next_value_sum for value in sums.values())
        return (print("\nMagic square!") if check_magic is True
                                         else print("\nNot a magic square!"))


main()
