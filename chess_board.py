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


def move_up_and_left(coord):
    new_coord = coord[0] - 1, coord[1] - 1
    if (new_coord[0] >= 0) and (new_coord[1] >= 0):
        return new_coord
    return None


def move_up_and_right(coord):
    '''get rid of hard-coded n-queens minus 1
    '''
    new_coord = coord[0] - 1, coord[1] + 1
    if (new_coord[0] >= 0) and (new_coord[1] <= 7):
        return new_coord
    return None


def move_down_and_right(coord):
    '''get rid of hard-coded n-queens minus 1
    '''
    new_coord = coord[0] + 1, coord[1] + 1
    if (new_coord[0] <= 7) and (new_coord[1] <= 7):
        return new_coord
    return None


def move_down_and_left(coord):
    '''get rid of hard-coded n-queens minus 1
    '''
    new_coord = coord[0] + 1, coord[1] - 1
    if (new_coord[0] <= 7) and (new_coord[1] >= 0):
        return new_coord
    return None


def get_diagonals(q_position):
    '''This is probably going to be ugly
    '''
    diags = []
    diag_checker = {"up_left":move_up_and_left, 
        "up_right":move_up_and_right,
        "down_right":move_down_and_right,
        "down_left":move_down_and_left
        }
    for d in diag_checker.keys():
        new_pos = diag_checker[d](q_position)
        if new_pos is None:
            continue
        else:
            while new_pos is not None:
                diags.append(new_pos)
                new_pos = diag_checker[d](new_pos)
    return diags


def count_diagonal_conflicts(queen_locations, verbose = False):
    '''Right now, this probably doesn't handle double counting properly, but
    I don't care too much
    '''
    in_diag_queens = []
    locs = [v for v in queen_locations.values()]
    for i, q in enumerate(locs):
        diags = set(get_diagonals(q))
        other_queens = set(locs[0:i] + locs[i+1:])
        conflict = list(diags.intersection(other_queens))
        if not conflict:
            if verbose:
                print(f"\tNo diagonal conflicts for queen at {q}")
            continue
        else:
            if verbose:
                print(f"\tQueen at {q} conflicts with these: {conflict}")
            in_diag_queens.extend(conflict)
    return len(in_diag_queens)


def check_if_solved(queen_locations, verbose = False):
    '''TODO: implement diagonal checks
    '''
    row_conf = count_row_conflicts(queen_locations)
    col_conf = count_col_conflicts(queen_locations)
    diag_conf = count_diagonal_conflicts(queen_locations)
    if (row_conf + col_conf + diag_conf) == 0:
        if verbose:
            print("WE SOLVED IT, BRO!!!")
        return True
    else:
        if verbose:
            print("Not solved...")
            print(f"We have {row_conf} row conflicts, ")
            print(f"{col_conf} column conflicts, ")
            print(f"and {diag_conf} conflicts along diagonals.")
        return False


# GETTING WHICH QUEENS ARE CONFLICTED IS A STEP WE SHOULD DO TO 
# HELP US CHOOSE 


def row_conflicts_by_queen(queen_locations):
    row_conf_dict = {}
    for k in queen_locations.keys():
        this_row = queen_locations[k][0]
        row_count = [1 for v in queen_locations.values() if v[0] == this_row]
        row_conf_dict[k] = sum(row_count) - 1
    return row_conf_dict


def column_conflicts_by_queen(queen_locations):
    '''AARGH IT'S THE SAME AS THE ABOVE JUST WITH A NEW DIMENSION'''
    col_conf_dict = {}
    for k in queen_locations.keys():
        this_col = queen_locations[k][1]
        col_count = [1 for v in queen_locations.values() if v[1] == this_col]
        col_conf_dict[k] = sum(col_count) - 1
    return col_conf_dict


def diag_conflicts_by_queen(queen_locations):
    '''
    '''
    diag_conf_dict = {}
    for k in queen_locations.keys():
        this_qn = queen_locations[k]
        diag_sqrs = get_diagonals(this_qn)
        othr_qns = [q for q in queen_locations.values() if q != this_qn]
        diag_conf_dict[k] = len(set(diag_sqrs).intersection(set(othr_qns)))
    return diag_conf_dict


def combine_conflict_dicts(conflict_dicts):
    all_confs = None
    for conf in conflict_dicts:
        if all_confs is None:
            all_confs = conf.copy()
        for k in conf.keys():
            all_confs[k] += conf[k]
    return all_confs


def conflicts_by_queen(queen_locations):
    '''Combine the results of the above three functions, breh'''
    conf_dicts = [row_conflicts_by_queen(queen_locations), 
        column_conflicts_by_queen(queen_locations),
        diag_conflicts_by_queen(queen_locations)]
    conf_by_qn = combine_conflict_dicts(conf_dicts)
    for k, v in conf_by_qn.items():
        if v == 0:
            del(conf_by_qn[k])
    return conf_by_qn


def find_best_column_for_queen(focus_queen_index, current_queen_locations, 
    unconflicted_queens, verbose = False):
    '''Assumes that we could only move a queen within the row it's already in, 
    this puts a queen in all columns in that row, sums up the column and 
    diagonal conflicts at each column, and returns the column that results in
    the lowest number of conflicts.

    TODO: Checking rows isn't necessary becasue of how I set up the
    problem right now...might be good to include for due diligence?
    '''
    focus_queen_pos = current_queen_locations[focus_queen_index]
    queen_coords = [v for v in current_queen_locations.values()]
    conflicts_by_col = {k:0 for k in current_queen_locations.keys()}
    # Check columns
    curr_queens_by_col = Counter(v[1] for v in queen_coords)
    for col, q_count in curr_queens_by_col.items():
        if col == focus_queen_pos[1]:
            conflicts_by_col[col] += q_count - 1
        else:
            conflicts_by_col[col] += q_count
    # Check diagonals
    other_queens = [x for x in queen_coords if x != focus_queen_pos]
    for k in conflicts_by_col.keys():
        diags = get_diagonals((focus_queen_pos[0],k))
        diag_conf = set(diags).intersection(set(other_queens))
        conflicts_by_col[k] += len(diag_conf)
    #TODO: Prevent the current queen location from being considered here?
    min_conflict = sorted(conflicts_by_col.items(), key = lambda v: v[1])[0]
    curr_conflict = conflicts_by_col[focus_queen_pos[1]]
    if (min_conflict[1] == 0) or (curr_conflict == 0):
        unconflicted_queens.append(focus_queen_index)
    if verbose:
        print(f"Queen {focus_queen_index} is now at {focus_queen_pos} ")
        print(f"where it is causing {curr_conflict} conflicts.")
        print(f"Moving it to column {min_conflict[0]} ")
        print(f"creates {min_conflict[1]} conflicts.")
    return min_conflict[0] if curr_conflict > 0 else None

    
def move_queen_to_column(move_queen_index, current_queen_locations,
    dest_column, chess_board):
    queen_start_pos = current_queen_locations[move_queen_index]
    chess_board[queen_start_pos[0]][queen_start_pos[1]] = 0
    chess_board[queen_start_pos[0]][dest_column] = 1
    current_queen_locations[move_queen_index] = (queen_start_pos[0], dest_column)


def choose_a_queen_to_move(queens_to_avoid, dim = 8):
    '''I think this is the only missing piece of the solver...
    '''
    poss_queens = [q for q in range(dim) if q not in queens_to_avoid]
    return random.choice(poss_queens)


if __name__ == "__main__":
    # At this point, all of this is starting to look like a class
    # The number of unconflicted queens, the queen locations are all
    # pieces of data about that class
    dat_board = make_chess_board(queen_loc_seed = 42)
    unconf_queens = []
    steps_taken = 0
    print("Here's what we're starting with ...")
    display_chess_board(dat_board)
    q_locs = locate_the_queens(dat_board)
    is_solved = check_if_solved(q_locs, verbose = True)
    ipdb.set_trace()
    while not is_solved:
        mv_queen = choose_a_queen_to_move(queens_to_avoid = unconf_queens)
        print(f"Finding min conflict column for queen {mv_queen}")
        new_col = find_best_column_for_queen(focus_queen_index = mv_queen, 
            current_queen_locations = q_locs, 
            unconflicted_queens = unconf_queens, 
            verbose = True)
        # The function above returns None if the chosen queen is already in 
        # a zero conflict position. Right now this continue syntax is 
        # janky shorthand for: just pick another queen.
        if new_col is None:
            continue
        move_queen_to_column(move_queen_index = mv_queen, 
            current_queen_locations = q_locs, dest_column = new_col, 
            chess_board = dat_board)
        steps_taken += 1
        display_chess_board(dat_board)
        is_solved = check_if_solved(q_locs, verbose = True)
        ipdb.set_trace()
    print(f"We solved the eight queens problem in {steps_taken} steps")



    # TODO: Other odd behaviors we're not actually accounting for
    #    - I think it's possible to "move" a queen to the same spot it's already in
    #    - I have also seen this thing get caught in an infinite loop at least once XD