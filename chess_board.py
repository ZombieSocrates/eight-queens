import random
import ipdb

from pprint import pprint
from collections import Counter

def make_chess_board(dim = 8, queen_loc_seed = None):
    '''Sets up a chessboard by randomly placing a single 
    queen in each row of the board
    '''
    chess_board = []
    random.seed(queen_loc_seed)
    for r in range(dim):
        chess_row = [0 for c in range(dim)]
        queen_loc = random.randint(a = 0, b = dim - 1)
        chess_row[queen_loc] = 1
        chess_board.append(chess_row)
    return chess_board


def display_chess_board(chess_board):
    '''Prints all the rows in a given chessboard, with 1's
    representing where queens are. Could also just pprint this'''
    for chess_row in chess_board:
        print(chess_row)


def search_across_row(chess_row, from_column = 0):
    '''Given a row and a column from which to start searching, will look 
    for a queen in that row. Returns the column location of a queen, or
    None if no queen is found
    '''
    try:
        q_col =  chess_row[from_column:].index(1)
        return from_column + q_col
    except ValueError:
        return None


def locate_the_queens(chess_board, verbose = True):
    '''Calls search_across_row for every row in the chess_board, continuing 
    only when no more queens are found in the row. Will print the location 
    of any queen it finds. Also returns the positions of each queen in a
    dictionary of format int : location tuple
    '''
    queen_locations = {}
    queen_count = 0
    for i, chess_row in enumerate(chess_board):
        j = search_across_row(chess_row)
        if j is None:
            if verbose:
                print(f"No queens in row {i}")
            continue
        else:
            while j is not None:
                if verbose:
                    print(f"Queen found at row {i}, column {j}")
                queen_locations[queen_count] = (i , j)
                queen_count += 1 
                j = search_across_row(chess_row, from_column = j + 1)
    return queen_locations


def count_row_conflicts(queen_locations):
    row_counts = Counter([q[0] for q in queen_locations.values()])
    return sum([v - 1 for v in row_counts.values()])


def count_col_conflicts(queen_locations):
    col_counts = Counter([q[1] for q in queen_locations.values()])
    return sum([v - 1 for v in col_counts.values()])


def move_up_and_left(queen_location):
    new_location = queen_location[0] - 1, queen_location[1] - 1
    if (new_location[0] >= 0) and (new_location[1] >= 0):
        return new_location
    return None


def move_up_and_right(queen_location):
    '''get rid of hard-coded n-queens minus 1
    '''
    new_location = queen_location[0] - 1, queen_location[1] + 1
    if (new_location[0] >= 0) and (new_location[1] <= 7):
        return new_location
    return None


def move_down_and_right(queen_location):
    '''get rid of hard-coded n-queens minus 1
    '''
    new_location = queen_location[0] + 1, queen_location[1] + 1
    if (new_location[0] <= 7) and (new_location[1] <= 7):
        return new_location
    return None


def move_down_and_left(queen_location):
    '''get rid of hard-coded n-queens minus 1
    '''
    new_location = queen_location[0] + 1, queen_location[1] - 1
    if (new_location[0] <= 7) and (new_location[1] >= 0):
        return new_location
    return None


def get_diagonals(q_position):
    '''This is probably going to be ugly
    '''
    diags = []
    diag_checker = {"up_left":move_up_and_left, 
        "up_right":move_up_and_right,
        "down_right":move_down_and_right,
        "down_left":move_down_and_left,
        }
    for d in diag_checker.keys():
        print(f"MOVING {d.replace('_',' ')}")
        new_pos = diag_checker[d](q_position)
        if new_pos is None:
            continue
        else:
            while new_pos is not None:
                diags.append(new_pos)
                new_pos = diag_checker[d](new_pos)
    return diags


def check_if_solved(queen_locations):
    '''TODO: implement diagonal checks
    '''
    row_conf = count_row_conflicts(queen_locations)
    col_conf = count_col_conflicts(queen_locations)
    if (row_conf + col_conf) == 0:
        print("WE SOLVED IT, BRO!!!")
    else:
        print("Not solved...")
        print(f"We still have {row_conf} row conflicts")
        print(f"and {col_conf} column conflicts")


if __name__ == "__main__":
    dat_board = make_chess_board(queen_loc_seed = 42)
    display_chess_board(dat_board)
    q_locs = locate_the_queens(dat_board)
    check_if_solved(q_locs)
    ipdb.set_trace()