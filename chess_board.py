import random
import ipdb

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
    representing where queens are'''
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


def locate_the_queens(chess_board):
    '''Calls search_across_row for every row in the chess_board, continuing 
    only when no more queens are found in the row. Will print the location 
    of any queen it finds

    TODO: Might be necessary to return the positions of each queen?
    '''
    for i, chess_row in enumerate(chess_board):
        j = search_across_row(chess_row)
        if j is None:
            print(f"No queens in row {i}")
            continue
        else:
            while j is not None:
                print(f"Queen found at row {i}, column {j}")
                j = search_across_row(chess_row, from_column = j + 1)


        

if __name__ == "__main__":
    dat_board = make_chess_board(queen_loc_seed = 42)
    display_chess_board(dat_board)
    locate_the_queens(dat_board)
    ipdb.set_trace()