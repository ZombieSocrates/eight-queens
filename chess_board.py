import random
import ipdb

def make_chessboard(dim = 8, queen_loc_seed = None):
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



if __name__ == "__main__":
    dat_board = make_chessboard(queen_loc_seed = 42)
    for c_row in dat_board:
        print(c_row)
    ipdb.set_trace()