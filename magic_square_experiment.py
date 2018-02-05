import sys, string

lst1 = [0,0,"0,3",1,1,12]
lst2 = [3330,(2,2),(2,1)]


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
                        raise ValueError("Has to be integers (0-9)!")
                coordinates_a.append(a) 
                coordinates_b.append(b)
        except ValueError as err:
            print(err)
        else:
            print("\nSuccessfully swapped values to [right/left].")
    return coordinates_a, coordinates_b, user_friendly


def process_list(lst):
    n, n_range = 0, len(lst)
    item_lst = []
    while n < n_range:
        lst_item = str(lst[n])
        if len(lst_item) >= 2:
            for index, element in enumerate(lst_item[:]):
                if index % 2 == 0:
                    print(index)
                    tuple_data = (lst_item[index], lst_item[index + 1])
                    print(tuple_data)
                    
                    lst.insert(n, tuple_data[0])
                    lst.insert(n + 1, tuple_data[1])
                    if index == (len(lst_item) - 2):
                        lst.remove(lst_item)
                        item_lst.append(tuple_data)
                    
                    print(lst)
                    n_range += 1 if index == 0 else ((index / 2) + 1)
                    
                    
        else:
            if n % 2 == 0:
                tuple_data = (lst[n], lst[n + 1])
                print(tuple_data)
                item_lst.append(tuple_data)
        n += 1
    return item_lst


def swap_coordinates_from_lists(coordinates_a_lst=None, 
                                coordinates_b_lst=None):
    if coordinates_a_lst is None or coordinates_b_lst is None:
        return [], [], 0
    else:
        try:
            remove_strings = [",", "(", ")", " "]
            for stringy in remove_strings:
                for n in range(len(coordinates_a_lst)):    
                    coordinates_a_lst[n] = str(coordinates_a_lst[n]).replace(stringy, "")
                for n in range(len(coordinates_b_lst)):    
                    coordinates_b_lst[n] = str(coordinates_b_lst[n]).replace(stringy, "")
            
            coordinates_a = process_list(coordinates_a_lst)
            coordinates_b = process_list(coordinates_b_lst)
            print(coordinates_a)
            print(coordinates_b)
            if (len(coordinates_a) % 2 != 0 or len(coordinates_b) % 2 != 0 or
                len(coordinates_a) != len(coordinates_b)):
                raise ValueError("List A and List B must have the same length "
                                 "and the lenth has to be an even number. ")
                
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
        return 
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
    a, b, user_friendly = swap_coordinates_from_lists(lst1, lst2)
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
