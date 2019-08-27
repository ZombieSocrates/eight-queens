import ipdb
import random
from collections import Counter

from chess_board import chessBoard
from solvers import columnwiseCSPSolver





def solve_many_boards(seed_list, dim_each = 8, n_moves = 50,
    verbose = False, stop_each = None):
    '''Given a list of queen positioning seeds, a size for each board, and 
    a maximum number of steps for 

    Don't hate the playa, hate the game
    '''
    bcount = len(seed_list)
    print(f"Working on {bcount} test cases...")
    for i, s in enumerate(seed_list):
        print(f"Case {i+1} of {bcount} (seed {s})")
        game = chessBoard(dimension = dim_each, queen_seed = s)
        player = columnwiseCSPSolver(board_object = game, max_moves = n_moves)
        n_steps = player.solve(verbose = verbose, stop_each = stop_each)
        player.solution_shortdoc(n_steps)
        print("-" * bcount, "\n")


if __name__ == "__main__":
        
    # BRANCH 1 -- Just 10 random cases to get a sense of what's "normal"
    # board_seeds = random.sample([j for j in range(9999)], 10)
    # solve_many_boards(seed_list = board_seeds)
    # ipdb.set_trace()
    
    # BRANCH 2 -- 5489, 8675309, and 999 are known problem children
    board_seeds = [42, 555, 5489, 666, 8675309, 999]
    solve_many_boards(seed_list = board_seeds)
    ipdb.set_trace()

    
    # BRANCH 3 -- Solving the same board 5 different times. Good example for repeated state
    # board_seeds = [50] * 5
    # solve_many_boards(seed_list = board_seeds, verbose = True)


    # IT WERKS FOR MORE THAN 8 queens!!!
    board_dim = 25
    dat_board = chessBoard(dimension = board_dim, queen_seed = 42)
    solver = columnwiseCSPSolver(board_object = dat_board, max_moves = 500)
    n_steps = solver.solve(verbose = True, stop_each = 20)
    solver.solution_shortdoc(n_steps)

    # TODO: 
    # - I'd like to experiment with repeated state checking to avoid loops
    # - It seems like there's a better way to choose which queen to move. Instead of 
    #   randomly choosing in the case of ties, perhaps make sure that moving the
    #   queen actually represents an improvement.