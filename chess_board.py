import ipdb
import random

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


    def get_state_string(self, move_queen = None, to_col = None):
        '''Returns a representation of the chess board's queen positions as a 
        (dim*2)-digit string. Every two characters is the row, column location 
        of a queen in the order they were initially placed on the board. 

        Calling this function with no arguments supplied will return the state 
        of the current queen positions on the board. Supplying the arguments 
        will returns what the state string would be if you moved a given queen 
        to a new column position, so we can avoid hitting repeated states.
        '''
        loc_strs = []
        for k, v in self.q_locs.items():
            if k == move_queen:
                loc_strs.append(f"{v[0] + 1}{to_col + 1}")
            else:
                loc_strs.append(f"{v[0] + 1}{v[1] + 1}")
        return "".join(loc_strs)   

   
    def check_up_and_left(self, coord):
        '''Generate a valid coordinate one unit up and left from coord.
        Would be a private method if python did that ...
        '''
        new_coord = coord[0] - 1, coord[1] - 1
        if (new_coord[0] >= 0) and (new_coord[1] >= 0):
            return new_coord
        return None


    def check_up_and_right(self, coord):
        '''Generate a valid coordinate one unit up and right from coord.
        Would be a private method if python did that ...
        '''
        bound = self.dim - 1
        new_coord = coord[0] - 1, coord[1] + 1
        if (new_coord[0] >= 0) and (new_coord[1] <= bound):
            return new_coord
        return None


    def check_down_and_right(self, coord):
        '''Generate a valid coordinate one unit down and right from coord.
        Would be a private method if python did that ...
        '''
        bound = self.dim - 1
        new_coord = coord[0] + 1, coord[1] + 1
        if (new_coord[0] <= bound) and (new_coord[1] <= bound):
            return new_coord
        return None


    def check_down_and_left(self, coord):
        '''Generate a valid coordinate one unit down and left from coord.
        Would be a private method if python did that ...
        '''
        bound = self.dim - 1
        new_coord = coord[0] + 1, coord[1] - 1
        if (new_coord[0] <= bound) and (new_coord[1] >= 0):
            return new_coord
        return None


    def get_diagonals(self, coord):
        '''Calculates all the relative diagonal positions from the given 
        coordinate, mainly for the purpose of saying "Is there a queen in any 
        of these diagonal positions?"
        '''
        diags = []
        diag_checker = {"up_left":self.check_up_and_left, 
            "up_right":self.check_up_and_right,
            "down_right":self.check_down_and_right,
            "down_left":self.check_down_and_left
            }
        for d in diag_checker.keys():
            new_pos = diag_checker[d](coord)
            if new_pos is None:
                continue
            else:
                while new_pos is not None:
                    diags.append(new_pos)
                    new_pos = diag_checker[d](new_pos)
        return diags

    
    def count_orthogonal_conflicts_by_queen(self):
        '''Returns a dictionary keyed by queen_index (0th queen, 1st queen) 
        with values as the number of conflicts that queen is creating in 
        orthogonal directions (rows or columns).

        TODO: Maybe some day disambiguating between row conflicts and column 
        conflicts will be helpful?
        '''
        orth_conf_dict = {}
        for k in self.q_locs.keys():
            orth_conf_dict[k] = 0
            for d in [0,1]:
                curr_d = self.q_locs[k][d]
                d_count = [1 for v in self.q_locs.values() if v[d] == curr_d]
                orth_conf_dict[k] += sum(d_count) - 1
        return orth_conf_dict


    def count_diagonal_conflicts_by_queen(self):
        '''Returns a dictionary keyed by queen_index (0th queen, 1st queen) 
        with values as the number of conflicts that queen is creating in 
        diagonal directions.
        '''
        diag_conf_dict = {}
        for k in self.q_locs.keys():
            this_qn = self.q_locs[k]
            diag_sqrs = self.get_diagonals(this_qn)
            othr_qns = [q for q in self.q_locs.values() if q != this_qn]
            diag_conf_dict[k] = len(set(diag_sqrs).intersection(set(othr_qns)))
        return diag_conf_dict


    def combine_conflict_counts(self, conflict_dicts):
        '''Helper functioned designed to sum the outputs of orthogonal and 
        diagonal conflict dicts together.
        '''
        all_confs = None
        for conf in conflict_dicts:
            if all_confs is None:
                all_confs = conf.copy()
                continue
            for k in conf.keys():
                all_confs[k] += conf[k]
        return all_confs


    def count_conflicts_by_queen(self):
        '''Combine the results of the above three methods, breh. Then deletes any 
        queen key that does not have any conflicts.'''
        conf_dicts = [self.count_orthogonal_conflicts_by_queen(),
            self.count_diagonal_conflicts_by_queen()]
        conf_smash = self.combine_conflict_counts(conf_dicts)
        return {k:v for k,v in conf_smash.items() if v!= 0}


if __name__ == "__main__":

    pass
