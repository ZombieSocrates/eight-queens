import random
import pprint
import ipdb

from collections import Counter


class chessBoard(object):

    def __init__(self, dimension, queen_seed = None):
        '''Sets up a chess board of a specified dimension and randomly 
        places a single queen in each row. Seeding this placement is 
        supported. '''
        self.dim = dimension
        self.q_seed = queen_seed
        self.rows = self.place_queens_by_row()
        self.q_locs = self.get_queen_locations()


    def place_queens_by_row(self):
        '''Places a single queen (1) in each row of the chessboard according 
        to the `dim` and `q_seed` attributes. '''
        rows = []
        random.seed(self.q_seed)
        for i in range(self.dim):
            row = [0 for c in range(self.dim)]
            q_loc = random.randint(a = 0, b = self.dim - 1)
            row[q_loc] = 1
            rows.append(row)
        return rows


    def display(self):
        '''Prints all the rows in a given chessboard, with 1's representing 
        where queens are. '''
        for row in self.rows:
            print(row)


    def search_across_row(self, chess_row, from_column = 0):
        '''Given a row and a column from which to start searching, will return 
        the column location of a queen. Returns None if no queen is found. '''
        try:
            q_col = chess_row[from_column:].index(1)
            return from_column + q_col
        except ValueError:
            return None


    def get_queen_locations(self):
        '''Calls search_across_row for every row in the board, continuing only 
        when no more queens are found in the row. Returns the locations in a 
        dictionary with the format of queen index: (row, column). '''
        queen_loc_dict = {}
        queen_index = 0
        for i, row in enumerate(self.rows):
            j = self.search_across_row(row)
            if j is None:
                continue
            else:
                while j is not None:
                    queen_loc_dict[queen_index] = (i, j)
                    queen_index += 1
                    j = self.search_across_row(row, from_column = j + 1)
        return queen_loc_dict


    def show_queen_locations(self):
        '''Displays the position of every queen stored in self.q_locs. Shifts 
        all indices by 1 to help with human readability. '''
        for q, loc in self.q_locs.items():
            r = loc[0]
            c = loc[1]
            print(f"Queen {q + 1} is at row {r + 1}, column {c + 1}")


    def queens_to_integer(self):
        '''Returns a representation of the chess board's current queen 
        positions as a (dim*2)-digit integer. Every two digits of this 
        integer is the row, column location of a queen. 

        TODO: Is it really worth some imagined performance gain to use an 
        integer? Storing it as a string makes it easier for us to index and 
        validate ... 
        '''
        loc_strs = [f"{v[0] + 1}{v[1] + 1}" for v in self.q_locs.values()]
        return int("".join(loc_strs))


    #TODO: check direction methods need to be in here

    #TODO: Maybe the conflict measurement ones need to be here too?




if __name__ == "__main__":

    qB = chessBoard(dimension = 8, queen_seed = 50)
    qB.display()
    qB.show_queen_locations()
    print(qB.queens_to_integer())
    ipdb.set_trace()
