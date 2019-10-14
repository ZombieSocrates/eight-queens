import random
import ipdb

from collections import Counter, defaultdict


class chessBoard(object):


    def __init__(self, dimension, state_string = None, queen_seed = None):
        '''Sets up a chess board of a specified dimension and puts queens at
        given positions or at entirely random positions. 

        In the context of the app, this class will be initialized with strings 
        representing the position of each queen on the board. We check to make 
        sure that the positions aren't junky. 

        You can also leave state_string as None and supply a seed to put a 
        queen randomly in each row.

        TODO: state_string will be more complicated if dimension is of 
        order of magnitude 2'''
        self.dim = dimension
        if state_string is None:
            self.rows = self.random_queen_each_row(queen_seed)
        elif not self.validate_state_string(state_string):
            raise NotImplementedError("I'm afraid I can't let you do that...")
        else:
            self.rows = self.place_queens_from_state_string(state_string)
        self.q_locs = self.get_queen_locations()
        self.board_state = self.get_state_string()
        self._make_move = {
             "UP": lambda xy: (xy[0] - 1, xy[1]),
             "DOWN": lambda xy: (xy[0] + 1, xy [1]),
             "LEFT": lambda xy: (xy[0], xy[1] - 1),
             "RIGHT": lambda xy: (xy[0], xy [1]  + 1),
             "UP_LEFT": lambda xy: (xy[0] - 1, xy[1] - 1),
             "UP_RIGHT": lambda xy: (xy[0] - 1, xy[1] + 1),
             "DOWN_LEFT": lambda xy: (xy[0] + 1, xy[1] - 1),
             "DOWN_RIGHT": lambda xy: (xy[0] + 1, xy[1] + 1),
             }


    def random_queen_each_row(self, queen_seed):
        '''Places a single queen (1) in each row of the chessboard according 
        to the `dim` and `q_seed` attributes. '''
        rows = []
        random.seed(queen_seed)
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


    def validate_state_string(self, state_string):
        '''This gets more complicated if dim order of magnitude is > 2. In fact,
        a pure string almost certainly won't work unless you zero-pad every
        coordinate to be the order of magnitude of the dimension of the board.

        THAT'S A PROBLEM FOR ANOTHER DAYY
        '''
        right_len = len(state_string)//2 == self.dim
        in_bounds = self.check_state_string_bounds(state_string)
        no_dupes = self.check_duplicate_positions(state_string)
        return (right_len & in_bounds & no_dupes)

        
    def check_state_string_bounds(self, state_string):
        '''Do all of the coordinates in the state string fall within the 
        dimensions of the board?
        '''
        try:
            min_cond = int(min(state_string)) >= 1
            max_cond = int(max(state_string)) <= self.dim
        except ValueError as e:
            return False
        return (max_cond & min_cond)


    def check_duplicate_positions(self, state_string):
        '''Does a state string that you are passing in to the creation
        function contain duplicate positions?

        Also, see above note about this assuming each coordinate being a 
        one digit string for the time being
        '''
        positions = [state_string[2*i:(2*i + 2)] for i in range(self.dim)]
        return max(Counter(positions).values()) == 1


    def get_state_string(self, move_queen = None, to_coord = None):
        '''Returns a representation of the chess board's queen positions as a 
        (dim*2)-digit string. Every two characters is the row, column location 
        of a queen in the order they were initially placed on the board. 

        Calling this function with no arguments supplied will return the state 
        of the current queen positions on the board. Supplying the arguments 
        will returns what the state string would be if you moved a given queen 
        to a new column position, so we can avoid hitting repeated states. '''
        loc_strs = []
        for k, v in self.q_locs.items():
            if k == move_queen:
                loc_strs.append(f"{to_coord[0] + 1}{to_coord[1] + 1}")
            else:
                loc_strs.append(f"{v[0] + 1}{v[1] + 1}")
        return "".join(loc_strs)


    def place_queens_from_state_string(self, state_string):
        rows = [[0] * self.dim for i in range(self.dim)]
        for i in range(self.dim):
            r_ind = int(state_string[(2*i)]) - 1
            c_ind = int(state_string[2*i + 1]) - 1
            rows[r_ind][c_ind] = 1
        return rows       


    def _out_of_bounds(self, coord):
        if (max(coord) >= self.dim) or (min(coord) < 0):
                return True
        return False


    def _move_in_direction(self, direction, coord, blocked_coords, 
        ok_moves = []):
        '''
        Calculate the valid moves in a single direction (string) that 
        you can make from coord, taking into account any blocked
        coordinates specified in blocked coords.

        Somehow, repeatedly calling this function is saving the ok_moves
        variable...OH WELL NO TIME TO FIX THIS THIS NOW LAWLLL
        '''
        if direction not in self._make_move.keys():
            valid_dirs = ",".join([d for d in self._make_move.keys()])
            err = f"Invalid direction: Must be one of {valid_dirs}"
            raise ValueError(err)
        next_coord = self._make_move[direction](coord)
        off_board = self._out_of_bounds(next_coord)
        hit_piece = next_coord in blocked_coords
        if not off_board and not hit_piece:
            ok_moves.append(next_coord)
            self._move_in_direction(direction, next_coord, 
                blocked_coords, ok_moves)
        return ok_moves
            

    def get_move_coords(self, base_coord, directions_to_move, blocked_coords):
        '''Calculate all moves from base_coord in the directions specified in 
        directions_to_move, taking into account any blocked locations 
        specified in blocked_coords
        '''
        avail_coords = []
        if not directions_to_move:
            directions_to_move = [d for d in self._make_move.keys()]
        for d in directions_to_move:
            dir_moves = self._move_in_direction(direction = d, 
                coord = base_coord, blocked_coords = blocked_coords, 
                ok_moves = [])
            avail_coords.extend(dir_moves)
        return avail_coords


    def get_diagonals(self, base_coord):
        diag_directions = [d for d in self._make_move.keys() if "_" in d]
        return self.get_move_coords(base_coord, 
            directions_to_move = diag_directions,
            blocked_coords = [])
        

    def _orthogonal_conflicts_by_queen(self):
        '''Returns a dictionary keyed by queen_index (0th queen, 1st queen) 
        with values as the number of conflicts that queen is creating in 
        orthogonal directions (rows or columns).

        TODO: Maybe some day disambiguating between row conflicts and column 
        conflicts will be helpful? '''
        orth_conf_dict = {}
        for k in self.q_locs.keys():
            orth_conf_dict[k] = 0
            for d in [0,1]:
                curr_d = self.q_locs[k][d]
                d_count = [1 for v in self.q_locs.values() if v[d] == curr_d]
                orth_conf_dict[k] += sum(d_count) - 1
        return orth_conf_dict


    def _diagonal_conflicts_by_queen(self):
        '''Returns a dictionary keyed by queen_index (0th queen, 1st queen) 
        with values as the number of conflicts that queen is creating in 
        diagonal directions. '''
        diag_conf_dict = {}
        for k in self.q_locs.keys():
            this_qn = self.q_locs[k]
            diag_sqrs = self.get_diagonals(this_qn)
            othr_qns = [q for q in self.q_locs.values() if q != this_qn]
            diag_conf_dict[k] = len(set(diag_sqrs).intersection(set(othr_qns)))
        return diag_conf_dict


    def combine_conflict_counts(self, conflict_dicts):
        '''Helper functioned designed to sum the outputs of orthogonal and 
        diagonal conflict dicts together. '''
        all_confs = None
        for conf in conflict_dicts:
            if all_confs is None:
                all_confs = conf.copy()
                continue
            for k in conf.keys():
                all_confs[k] += conf[k]
        return all_confs


    def count_conflicts_by_queen(self):
        '''Combine the results of the above three methods, breh. Then deletes 
        any queen key that does not have any conflicts. '''
        conf_dicts = [self._orthogonal_conflicts_by_queen(),
            self._diagonal_conflicts_by_queen()]
        conf_smash = self.combine_conflict_counts(conf_dicts)
        return {k:v for k,v in conf_smash.items() if v!= 0}


    def _validate_dim(self, change_dim):
        if change_dim not in [0,1]:
            e_msg = "Right now, you can change either row (0) or column (1)"
            raise NotImplementedError(e_msg)
        return change_dim


    def _orthogonal_conflicts_by_square(self, change_dim):
        '''Return the number of queens within each row (change_dim = 0)
        or column (change_dim = 1). This is the number of conflicts we
        would incur if we moved within said dimension

        TODO: Is this really that different from 
        self._orthogonal_conflicts_by_queen?
        '''
        cdim = self._validate_dim(change_dim)
        return Counter([v[cdim] for v in self.q_locs.values()])


    def _diagonal_conflicts_by_square(self, base_coord, change_dim):
        '''Return the number of diagonal conflicts we would incur
        if we moved from base_coord to any possible space within 
        the current row (change_dim = 0) or column (change_dim = 1)

        TODO: Is this really that different from 
        self._diagonal_conflicts_by_queen?
        '''
        cdim = self._validate_dim(change_dim)
        diag_conf = {}
        queen_coords = [x for x in self.q_locs.values()] #if x != base_coord]
        for k in self.q_locs.keys():
            move_coord = self._get_orthogonal_move(base_coord, cdim, k)
            diags = self.get_diagonals(move_coord)
            n_conf = set(diags).intersection(set(queen_coords))
            diag_conf[k] = len(n_conf)
        return diag_conf


    def _get_orthogonal_move(self, base_coord, change_dim, move_dest):
        '''If we're moving in row space, our column stays constant and
        vice versa
        '''
        constant_dim = 1 - change_dim
        if change_dim == 1:
            return (base_coord[constant_dim], move_dest)
        return (move_dest, base_coord[constant_dim])


    def _get_base_conflicts(self, base_coord, change_dim):
        '''
        If you're moving a queen within a row, there's a certain number of 
        pre-existing column conflicts that will impact that move,  and vice 
        versa. This preloads the result of self.count_conflicts_at_square() 
        with existing conflicts in a constant dimension.
        '''
        const_dim = 1 - self._validate_dim(change_dim)
        dim_confs = self._orthogonal_conflicts_by_square(const_dim)
        exist_confs = dim_confs[base_coord[const_dim]] - 1
        return {k: exist_confs for k in self.q_locs.keys()}


    def count_conflicts_at_square(self, move_queen, change_dim):
        '''Let's assume you are moving focus_queen within either rows or
        columns (dim  = 0 or dim = 1). This returns a dictionary 
        where the keys are each row or column index and the values are
        the number of conflicts you would have if you moved the queen
        to that space from its current one.

        Basically, this is an analog to count_conflicts_by_queen designed 
        to measure future states instead of current ones. 
    
        TODO 1: Port to the front end if we want to surface scores of 
        hypothesized moves?

        TODO 3: Implementing this to also take diagonal moves into account. 
        It seems like it'd be hard but maybe not necessary.
        '''
        base_coord = self.q_locs[move_queen]
        conf_dicts = [self._get_base_conflicts(base_coord, change_dim), 
            self._orthogonal_conflicts_by_square(change_dim),
            self._diagonal_conflicts_by_square(base_coord, change_dim)]
        conf_smash = self.combine_conflict_counts(conf_dicts)
        return {k:v for k,v in conf_smash.items() if k != base_coord[change_dim]}


    def get_queens_by_row(self):
        '''Returns a dictionary of {row_idx:[list of q_idx]}
        '''
        queens_by_row = defaultdict(list)
        for queen, position in self.q_locs.items():
            queens_by_row[position[0]].append(queen)
        return queens_by_row


    def is_row_conflicted(self):
        '''If there's more than one queen in each row, we got PROBLEMS
        '''
        n_queens_per_row = [len(r) for r in self.get_queens_by_row().values()]
        return max(n_queens_per_row) > 1


    def find_unoccupied_rows(self):
        '''
        '''
        occupied_rows = set([r for r in self.get_queens_by_row()])
        all_rows = set([r for r in range(self.dim)])
        return list(all_rows.difference(occupied_rows))


    def row_conflicted_queens(self):
        '''If the board were in a row-conflicted state, these are the
        queens that would need to move.
        '''
        rq = []
        for queens in self.get_queens_by_row().values():
            rq.extend(queens[1:])
        return rq


    


if __name__ == "__main__":

    #TODO: Maybe move these to a test folder?
    print("Failing with an invalid initialization string")
    for junky_str in ["","555"]:
        try:
            chessBoard(dimension = 8, state_string = junky_str)
        except NotImplementedError as e:
            print(f"\t{e}")

    print("Init from random number")
    foo = chessBoard(dimension = 8, queen_seed = 42)
    foo.display()
    print(f"Row conflicted? {foo.is_row_conflicted()}")
    print(f"Unoccupied Rows: {foo.find_unoccupied_rows()}")
    print(f"MOVE DEEZ QUEENS: {foo.row_conflicted_queens()}")
    print("\n-----------")
    

    print("Init from determined positions")
    bar = chessBoard(dimension = 8, state_string = "1112131415161718")
    bar.display()
    print(f"Row conflicted? {bar.is_row_conflicted()}")
    print(f"Unoccupied Rows: {bar.find_unoccupied_rows()}")
    print(f"MOVE DEEZ QUEENS: {bar.row_conflicted_queens()}")
    print("\n-----------")


    


    




