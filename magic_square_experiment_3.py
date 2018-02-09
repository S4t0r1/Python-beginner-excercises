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
    prompt_action = input("[C]reate [E]dit [I]nspect: ").lower()
    if prompt_action in "cei":
        prompt_method = input("[F]ile [S]eq [M]anually: ").lower()
        if prompt_method in "fsm":
            return prompt_action, prompt_method


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
    board = [[0 for e in range(4)] for i in range(4)]
    value = 1
    for x in range(4):
        for y in range(4):
            board[x][y] += value
            value += 1
    print_board(board)
    return board


def process_lists(*args, items_lsts=[]):
    remove_chars = {c for c in string.punctuation + string.whitespace + "\ufeff"}
    for lst in args:
        if not lst:
            return
        lst = [str(c) for c in lst if str(c) not in remove_chars]
        try:
            for element in lst:
                if element not in string.digits:
                    raise ValueError("\nERROR: Has to be integers (0-9)! ")
            if not len(lst) % 2 == 0:
                raise IndexError("\nERROR: Must be coordinate pair/s (x,y)!")
            items_lst = [(lst[n], lst[n + 1]) for n in range(len(lst)) if n % 2 == 0]
        except (ValueError, IndexError) as err:
            print(err, "\nList {0}: not processed".format(lst))
        else:
            print("List {0}: OK{1}".format(lst, "\n" if len(lst) > 4 else ""))
            if len(args) > 1:
                items_lsts.append(items_lst)
    return items_lsts if items_lsts else items_lst


def in_line_coordinate_pairs():
    prompt = input("Create coordinate pairs for swapping on each line?"
                       "\n[default = coordinate pairs with mixed lines]: ")
    return 0 if prompt.lower() not in {"y", "yes"} else 1


def swap_values_manually():
    in_line = in_line_coordinate_pairs()
    user_friendly = user_friendly_coordinates()
    coordinates_a, coordinates_b = [], []
    a = True
    while True:
        msg = ("\nChoose x,y for {0}: ".format("A" if a else "B") 
                if not in_line else "\nChoose (x_A, y_A), (x_B, y_B) "
                                    "coordinate pairs for swapping: ")
        try:
            prompt = process_lists(input(msg))
            if not prompt:
                break
            if in_line:
                coordinates_a, coordinates_b = prompt[::2], prompt[1::2]
            coordinates = coordinates_a if a else coordinates_b
            coordinates += prompt
            a = False if a else True
        except ValueError as err:
            print(err)
        else:
            print(("\nSuccessfully queued coordinates for "
                   "swapping values to [B|A]\n") if a else "")
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
        in_line = in_line_coordinate_pairs()
        fh = open(filename, encoding="utf-8")
        for lino, line in enumerate(fh, start=1):
            line_items = process_lists(list(line.strip()))
            if not in_line:
                if lino % 2 != 0:
                    coordinates_a += line_items
                else:
                    coordinates_b += line_items
            else:
                for n in range(len(line_items) - 1):
                    if n % 2 == 0:
                        coordinates_a.append(line_items[n])
                        coordinates_b.append(line_items[n + 1])
        if not (len(coordinates_a) == len(coordinates_b)):
            raise IndexError("Must be even number of lines if pairs from mixed lines")
    except (EnvironmentError, IndexError) as err:
        print(err)
    else:
        print("\nSuccessfully queued coordinates for swapping values\n")
        return coordinates_a, coordinates_b, 0
    finally:
        if fh is not None:
            fh.close()


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
            print("Exiting...")
            return [], [], 0
        else:
            if not coordinates_a_lst:
                coordinates_a_lst = list(input("\nInput for sequence A: "))
            elif not coordinates_b_lst:
                coordinates_b_lst = list(input("\nInput for sequence B: "))
            if not coordinates_a_lst or not coordinates_b_lst:
                print("\nERROR: Empty List/s. Exiting...")
                return [], [], 0
    try:
        coordinates_a, coordinates_b = process_lists(coordinates_a_lst, coordinates_b_lst)
        if (len(coordinates_a) % 2 != 0 or len(coordinates_b) % 2 != 0 or
            len(coordinates_a) != len(coordinates_b)):
            raise ValueError("\nList A and List B must have the same number of "
                             "integers and it should be an even number. ")
    except ValueError as err:
        print(err)
        return [], [], 0
    else:
        print("\nSuccessfully queued coordinates "
              "for swapping values to [B|A]\n")
    return coordinates_a, coordinates_b, 0


def user_friendly_coordinates():
    prompt = input("User-friendly coordinates (without zeros)?: ")
    return 1 if prompt.lower() in {"y", "yes"} else 0


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
            print("Swapped values {0} and {1} successfully"
                  .format(board[x_b][y_b], board[x_a][y_a]))
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
