import ipdb
import random

from chess_board import chessBoard
from solvers import columnwiseCSPSolver


    # TODO: 
    # - I'd like to experiment with repeated state checking to avoid loops
    # - It seems like there's a better way to choose which queen to move. Instead of 
    #   randomly choosing in the case of ties, perhaps make sure that moving the
    #   queen actually represents an improvement.


DEMO_OPTS = ["Solve one case step-by-step", "Solve many random cases", 
    "Solve many predetermined cases", "Solve the same case many times",
    "Eight queens? HOW ABOUT 25?!?!?!?"]


DEMO_PARAMS = {
    "1":{
        "seed_list": [42],  
        "dim_each": 8, 
        "n_moves": 50, 
        "verbose": True, 
        "stop_each": 1
    },
    "2":{
        "seed_list": random.sample([j for j in range(9999)], 10),  
        "dim_each": 8, 
        "n_moves": 50, 
        "verbose": False, 
        "stop_each": None
    },
    "3":{
        "seed_list": [42, 555, 5489, 666, 8675309, 999],  
        "dim_each": 8, 
        "n_moves": 50, 
        "verbose": False, 
        "stop_each": None
    },
    "4":{
        "seed_list": [50] * 5,  
        "dim_each": 8, 
        "n_moves": 50, 
        "verbose": True, 
        "stop_each": None
    },
    "5":{
        "seed_list": [42],  
        "dim_each": 25, 
        "n_moves": 500, 
        "verbose": True, 
        "stop_each": 20
    }
}



def solve_many_boards(seed_list, dim_each = 8, n_moves = 50,
    verbose = False, stop_each = None):
    '''Given a list of queen positioning seeds, a size for each board, and 
    a maximum number of moves to attempt before giving up, run your 
    columnwise CSP eight queens solver on each board configuration. 

    Don't hate the playa, hate the game
    '''
    bcount = len(seed_list)
    if bcount > 1:
        print(f"Working on {bcount} test cases...")
    for i, s in enumerate(seed_list):
        if bcount > 1:
            print(f"Case {i+1} of {bcount} (seed {s})")
        game = chessBoard(dimension = dim_each, queen_seed = s)
        player = columnwiseCSPSolver(board_object = game, max_moves = n_moves)
        n_steps = player.solve(verbose = verbose, stop_each = stop_each)
        player.solution_shortdoc(n_steps)
        print("-" * bcount, "\n")


def main(menu_list = DEMO_OPTS, demo_params = DEMO_PARAMS):
    '''Lets you run some "test cases" and step through solutions to the 
    eight queens problem from the comfort of your terminal. Was it worth it to 
    engineer this bad-ass CLI? You bet'chyer bottom dollar it was!!!
    '''
    print("Welcome to the Eight Queens Demo!") 
    print("Choose a routine with your number keys:")
    chosen_opt = None
    while chosen_opt not in demo_params.keys(): 
        for i, opt in enumerate(menu_list):
            print(f"\t{i + 1}. {opt}")
        chosen_opt = input(">")
        if chosen_opt not in demo_params.keys():
            print("Sorry, that's not on the menu. Please try again")
    solve_many_boards(**demo_params[chosen_opt])


if __name__ == "__main__":

    main()

    

   

    # if chosen_opt == 1:
    #     single_base_case = 42
    #     solve_many_boards(seed_list = [single_base_case], verbose = True, 
    #         stop_each = 1)

    # elif chosen_opt == 2:
    #     # Just 10 random cases to get a sense of what's "normal"
    #     board_seeds = random.sample([j for j in range(9999)], 10)
    #     solve_many_boards(seed_list = board_seeds)
    
    # elif chosen_opt == 3:    
    #     # 5489, 8675309, and 999 are known problem children
    #     board_seeds = [42, 555, 5489, 666, 8675309, 999]
    #     solve_many_boards(seed_list = board_seeds)

    # elif chosen_opt == 4:    
    #     board_seeds = [50] * 5
    #     solve_many_boards(seed_list = board_seeds, verbose = True)

    # else:
    #     big_board = chessBoard(dimension = 25, queen_seed = 42)
    #     solver = columnwiseCSPSolver(board_object = big_board, max_moves = 500)
    #     n_steps = solver.solve(verbose = True, stop_each = 20)
    #     solver.solution_shortdoc(n_steps)


