import ipdb
import random

from collections import Counter

from chess_board import chessBoard


#Any solver should have this particular method, but the solve method 
def check_if_solved(board_object, verbose = False):
    '''Right now, this probably doesn't handle double counting properly, but
    I don't care too much
    '''

    conflicted_queens = board_object.count_conflicts_by_queen()
    if not conflicted_queens:
        return True
    else:
        if verbose:
            print("Not solved yet...")
            print(f"\t{len(conflicted_queens)} queens still conflicted")
            for q, n in conflicted_queens.items():
                print(f"\tQueen {q} has {n} conflicts")
            print("\n")
        return False


# ALL OF THIS STUFF BELOW BELONGS TO A SPECIFIC SOLVER!!!
def choose_max_conflict_queen(board_object):
    '''We always want to move the queen that presents the most conflicts in the 
    current configuration. This filters the conflicted queens down to those 
    presenting the maximum number of conflicts, and then chooses one to move
    from those. The randomness will hopefully prevent us from moving the same 
    queen over and over again
    '''
    conf_by_qn = board_object.count_conflicts_by_queen()
    max_conf = max(conf_by_qn.values())
    qns_at_max = [k for k in conf_by_qn.keys() if conf_by_qn[k] == max_conf]
    return random.choice(qns_at_max)


def find_best_column_for_queen(board_object, focus_queen_index, curr_step, 
    verbose = False):
    '''Assumes that we could only move a queen within the row it's already in, 
    this puts a queen in all columns in that row, sums up the column and 
    diagonal conflicts at each column, and returns the column that results in
    the lowest number of conflicts.

    TODO: Checking rows isn't necessary because of how I set up the
    problem right now...might be good to include for due diligence?
    '''
    this_loc = board_object.q_locs[focus_queen_index]
    all_locs = [v for v in board_object.q_locs.values()]
    conflicts_by_col = {k:0 for k in board_object.q_locs.keys()}
    # Check columns
    curr_queens_by_col = Counter(v[1] for v in all_locs)
    for col, q_count in curr_queens_by_col.items():
        if col == this_loc[1]:
            conflicts_by_col[col] += q_count - 1
        else:
            conflicts_by_col[col] += q_count
    # Check diagonals
    other_locs = [x for x in all_locs if x != this_loc]
    for k in conflicts_by_col.keys():
        diags = board_object.get_diagonals((this_loc[0],k))
        diag_conf = set(diags).intersection(set(other_locs))
        conflicts_by_col[k] += len(diag_conf)
    conf = conflicts_by_col[this_loc[1]]
    del(conflicts_by_col[this_loc[1]])
    min_conf = sorted(conflicts_by_col.items(), key = lambda v: v[1])[0]
    if verbose:
        print(f"{curr_step + 1}. Queen at {this_loc} causes {conf} conflicts.")
        print(f"Moving to column {min_conf[0]} causes {min_conf[1]} conflicts.")
    return min_conf[0] 

    
def move_queen_to_column(board_object, move_queen_index, dest_column):
    queen_start_pos = board_object.q_locs[move_queen_index]
    board_object.rows[queen_start_pos[0]][queen_start_pos[1]] = 0
    board_object.rows[queen_start_pos[0]][dest_column] = 1
    board_object.q_locs[move_queen_index] = (queen_start_pos[0], dest_column)


def solve_queens_problem(board_object, max_steps = 50, verbose = False, 
    stop_each = None):
    '''Should this return anything? The number of steps it took and the 
    solution state is my first guess...
    '''
    steps_taken = 0
    if verbose:
        print(f"Solving the {board_object.dim}-queens problem ...")
        board_object.display()
    # q_locs = locate_the_queens(board_object, verbose = verbose)
    is_solved = check_if_solved(board_object, verbose = verbose)
    while not is_solved and steps_taken < max_steps:
        mv_queen = choose_max_conflict_queen(board_object)
        mv_col = find_best_column_for_queen(board_object, 
            focus_queen_index = mv_queen, curr_step = steps_taken, 
            verbose = verbose)
        move_queen_to_column(board_object, move_queen_index = mv_queen, 
            dest_column = mv_col)
        steps_taken += 1
        is_solved = check_if_solved(board_object, verbose = verbose)
        if isinstance(stop_each, int): 
            if not is_solved and (steps_taken % stop_each == 0):
                print(f"Pausing after {steps_taken} steps.")
                if verbose:
                    board_object.display()
                ipdb.set_trace()
    return is_solved, steps_taken


def solution_shortdoc(board_object, solved_bool, n_steps):
    if solved_bool:
        print(f"Solved the {board_object.dim}-queens problem in {n_steps} steps!")
    else:
        print(f"Took {n_steps} steps and found no solution...")


def solve_many_boards(seed_list, dim_each = 8, steps_each = 50,
    verbose = False, stop_each = None):
    bcount = len(seed_list)
    print(f"Working on {bcount} test cases...")
    for i, s in enumerate(seed_list):
        print(f"Case {i+1} of {bcount} (seed {s})")
        s_board = chessBoard(dimension = dim_each, queen_seed = s)
        solved, n_steps = solve_queens_problem(board_object = s_board, 
            max_steps = steps_each, verbose = verbose, 
            stop_each = stop_each)
        solution_shortdoc(s_board, solved, n_steps)
        print("-" * bcount, "\n")


if __name__ == "__main__":
        
    # BRANCH 1 -- Just 10 random cases to get a sence of what's "normal"
    # board_seeds = random.sample([j for j in range(9999)], 10)
    # solve_many_boards(seed_list = board_seeds)

    
    # BRANCH 2 -- 5489, 8675309, and 999 are known problem children
    # board_seeds = [42, 555, 5489, 666, 8675309, 999]
    # solve_many_boards(seed_list = board_seeds)

    
    # BRANCH 3 -- Solving the same board 5 different times. Good example for repeated state
    board_seeds = [50] * 5
    solve_many_boards(seed_list = board_seeds, verbose = True)


    # IT WERKS FOR MORE THAN 8 queens!!!
    # board_dim = 25
    # dat_board = chessBoard(dimension = board_dim, queen_seed = 42)
    # soln_bool, soln_score = solve_queens_problem(board_object = dat_board, 
    #     max_steps = 100, verbose = True, stop_each = 10)
    # solution_shortdoc(dat_board, soln_bool, soln_score)

    # TODO: 
    # 1. Create a base_solver class.
    # 2. I'd like to experiment with repeated state checking to avoid loops
    # 3. It seems like there's a better way to choose which queen to move. Instead of 
    #    randomly choosing in the case of ties, perhaps make sure that moving the
    #    queen actually represents an improvement.