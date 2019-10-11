import random
import ipdb

from collections import Counter, defaultdict
from chess_board import chessBoard
from pprint import pprint


class baseSolver(object):
    

    def __init__(self, board_object, max_moves = 50):
        '''Any solver needs a board configuration that it will presumably 
        solve and a maximum number of moves to make in any solution. We check 
        to see if that initial configuration is already solved, and then build 
        an initial seen_states object, which tracks child_state:parent_state 
        for any move that the solver makes. '''
        self.board = board_object
        self.move_limit = max_moves
        self.seen_states = {self.board.get_state_string(): None}
        self.n_moves = self.tally_moves_made()
        self.below_limit = self.check_if_moves_remain()
        self.is_solved = self.check_if_solved(verbose = False)
        

    def check_if_state_is_new(self, next_state):
        return False if next_state in self.seen_states.keys() else True


    def tally_moves_made(self):
        return len(self.seen_states) - 1


    def check_if_moves_remain(self):
        self.n_moves = self.tally_moves_made()
        return self.n_moves < self.move_limit


    def check_if_solved(self, verbose = False):
            conflicted_queens = self.board.count_conflicts_by_queen()
            if not conflicted_queens:
                return True
            else:
                if verbose:
                    print("Not solved yet...")
                    print(f"\t{len(conflicted_queens)} queens still conflicted")
                    for q, n in conflicted_queens.items():
                        print(f"\tQueen in row {q + 1} has {n} conflicts")
                    print("\n")
            return False


    def solution_shortdoc(self):
        '''Houston, we have a solution!
        '''
        if self.is_solved:
            n = len(self.seen_states) - 1
            return f"Solved the {self.board.dim}-queens problem in {n} steps!"
        else:
            return f"Took {self.move_limit} steps and found no solution..."


    def walk_solution_path(self):
        '''Will traverse self.seen_states backwards and builds out a 
        representation of the steps that were taken by the solver. Returns an
        object with a `coords` attribute--an array of fromCoord, toCoord that 
        the front end can use to product the moves--and a `text` attribute--an 
        array of human-readible sentences that...I'm not sure is actually 
        useful?
        '''
        soln_path = defaultdict(list)
        pointB = self.board.get_state_string()
        while pointB is not None:
            pointA = self.seen_states[pointB]
            if pointA is not None:
                txt_step = self.solution_step_as_text(parent_state = pointA, 
                    child_state = pointB)
                soln_path["text"].insert(0, txt_step)
                crd_pair = self.solution_step_as_coords(parent_state = pointA, 
                    child_state = pointB)
                soln_path["coords"].insert(0, crd_pair)
            pointB = pointA    
        return soln_path


    def get_change_between_states(self, parent_state, child_state):
        '''TODO (?): Won't always be slicing by two for larger orders of 
        magnitude of self.board.dim'''
        for v in range(self.board.dim):
            coord_p = parent_state[(2 * v):2 * (v + 1)]
            coord_c = child_state[(2 * v):2 * (v + 1)]
            if coord_p != coord_c:
                return coord_p, coord_c


    def solution_step_as_coords(self, parent_state, child_state):
        step_coords = []
        for pos in self.get_change_between_states(parent_state, child_state):
            coord_pair = [int(v) - 1 for v in pos]
            step_coords.append(coord_pair)
        return step_coords


    def solution_step_as_text(self, parent_state, child_state):
        coord_p, coord_c = self.get_change_between_states(parent_state, 
            child_state)
        s1 = f"Move queen at ({coord_p[0]},{coord_p[1]})"
        s2 = f"to ({coord_c[0]},{coord_c[1]})"
        return " ".join([s1, s2]) 


    def get_move_dimension(self, parent_state, child_state):
        '''For collapsing successive moves in the same row/column together, we 
        need to see whether an entry in self.seen_states is in "row 5" or "
        column 3"

        TODO: This may need to be refactored if I support board.dim with order
        of magnitude larger than 1
        '''
        coord_p, coord_c = self.get_change_between_states(parent_state, 
            child_state)
        if coord_p[0] == coord_c[0]:
            return f"row {coord_p[0]}"
        return f"col {coord_c[0]}"


    def collapse_seen_states(self):
        '''In some cases, our solver will make successive moves in the same
        dimension (eg. a move from 1,5 to 1,4 followed by a move from 1,4 to 
        1,8). This is a similar method to self.walk_solution_path, but it will
        collapse successive states like this together into one move and 
        recalculate some of the solver's metadata.

        I apologize that this is not tremendously readable ...

        TODO: Could be possible to try this within .solve to make sure that
        when we hit a move limit 
        '''
        child = self.board.get_state_string()
        while child is not None:
            parent = self.seen_states[child]
            grandparent = self.seen_states[parent]
            if grandparent is None:
                child = grandparent
                continue
            this_move_dim = self.get_move_dimension(parent, child)
            last_move_dim = self.get_move_dimension(grandparent, parent)
            if this_move_dim == last_move_dim:
                self.seen_states[child] = grandparent
                self.seen_states.pop(parent)
                # Turned out to be crucial to NOT increment child in this case
            else:
                child = parent
        self.n_moves = self.tally_moves_made()


    def get_solution(self, prune_solution = True):
        '''Basically packages up the information from calling solver.solve()
        in a format that our front end can interpret '''
        out_json = {"is_solved":self.is_solved}
        if not self.is_solved:
            out_json["n_tries_made"] = self.move_limit
        else:
            if prune_solution:
                self.collapse_seen_states()
            out_json["solution"] = self.walk_solution_path()
        out_json["message"] = self.solution_shortdoc()
        return out_json


    def solve(self):
        '''Only implemented in child classes
        '''
        raise NotImplementedError


class minConflictColumnSolver(baseSolver):
    

    def prioritize_queens(self):
        '''Returns a priority queue for the queens that the solver may want to 
        move. The queen(s) with the largest number of current conflicts will
        appear at the front of the list.
        '''
        conf_by_qn = self.board.count_conflicts_by_queen().items()
        qn_sort = sorted(conf_by_qn, key = lambda v: v[1], reverse = True) 
        return [w[0] for w in qn_sort]


    def prioritize_cols(self, focus_queen, conflict_cutoff):
        '''Given a queen that the solver is considering moving and a number of 
        conflicts to try and improve upon, this method returns a list of tuples 
        containing possible destination columns for that queen. The tuples are 
        like (column index, n_conflicts), with n_conflicts <= conflict_cutoff, 
        and the array itself is sorted by n_conflicts increasing 


        TODO: If I am using queen_to_unoccupied_row(), all I need is to get the resultant
        conflict score of that move ... I might be able to repurpose some stuff here
        to do that.
        '''
        conflicts_by_col = self.board.conflicts_for_move(focus_queen,1)
        improve_cols = [v for v in conflicts_by_col.items() if v[1] <= conflict_cutoff]
        return sorted(improve_cols, key = lambda v: v[1])


    def worst_queen_to_best_column(self, conflict_cutoff = None, 
        verbose = False):
        '''This is the standard method of trying to move the most conflicted 
        queen to its least conflicted column, so long as the resulting 
        conflictedness is at or below a given conflict cutoff. 

        Invoking this with conflict_cutoff as None will try to move a queen to 
        an unseen state with conflictedness less than or equal to what it is 
        currently at. If that doesn't return anything, it will automatically 
        relax the cutoff until you find some slightly worse, but viable option.

        TODO 1: Might be interesting to track how often the solver gets stuck in 
        local optima and needs to re-call itself. That's the only reason for 
        the verbose parameter right now)
        '''
        if conflict_cutoff is None:
            conflict_cutoff = max(self.board.count_conflicts_by_queen().values())
        queen_pq = self.prioritize_queens()
        for cand_qn in queen_pq:
            col_pq = self.prioritize_cols(cand_qn, conflict_cutoff)
            qn_row = self.board.q_locs[cand_qn][0]
            for c_tuple in col_pq:
                cand_coord = (qn_row, c_tuple[0])
                cand_cnflct = c_tuple[1]
                resulting_state = self.board.get_state_string(cand_qn, cand_coord)
                if self.check_if_state_is_new(resulting_state):
                    return cand_qn, cand_coord, cand_cnflct
        if verbose:
            print("Relaxing conflict cutoff by one ...")
        return self.worst_queen_to_best_column(conflict_cutoff + 1, verbose)


    def document_chosen_move(self, cand_queen, cand_coord, rslt_conf):
        '''For debugging in implementing repeated state checking.'''
        curr_conf = self.board.count_conflicts_by_queen()[cand_queen]
        focus_ind = self.board.q_locs[cand_queen]
        init_loc = (focus_ind[0] + 1, focus_ind[1] + 1)
        dest_loc = (cand_coord[0] + 1, cand_coord[1] + 1)
        print(f"{len(self.seen_states)}. Queen at {init_loc} causes {curr_conf} conflicts.")
        print(f"Moving to {dest_loc} causes {rslt_conf} conflicts.")


    def update_board(self, focus_queen, dest_coord):
        '''Once you know the place you want to move the queen to, change the 
        attributes of the underlying board to refelct that move. 
        '''
        init_coord = self.board.q_locs[focus_queen]
        self.board.rows[init_coord[0]][init_coord[1]] = 0
        self.board.rows[dest_coord[0]][dest_coord[1]] = 1
        self.board.q_locs[focus_queen] = dest_coord
        # This is more of a housekeeping step rather than actually crucial
        self.board.board_state = self.board.get_state_string()
    

    def update_seen_states(self, focus_queen, dest_coord):
        parent_st = self.board.get_state_string()
        child_st = self.board.get_state_string(move_queen = focus_queen, 
            to_coord = dest_coord)
        self.seen_states.update({child_st:parent_st})


    def move_queen_to_coord(self, focus_queen, dest_coord, verbose = False):
        '''Handles all the instance attributes that need to change when we've 
        actually decided move one of the queens: updates the history of seen 
        states, updates the board locations, checks to see if we're at a goal
        state, and increments the solver's move counter.
        '''
        self.update_seen_states(focus_queen, dest_coord)
        self.update_board(focus_queen, dest_coord)
        self.is_solved = self.check_if_solved(verbose = verbose)
        self.below_limit = self.check_if_moves_remain()


    def moves_within_column(self, focus_queen):
        focus_loc = self.board.q_locs[focus_queen]
        occupied_locs = [v for v in self.board.q_locs.values()]
        return self.board.get_move_coords(base_coord = focus_loc,
            directions_to_move = ["UP","DOWN"],
            blocked_coords = occupied_locs)


    def queen_to_unoccupied_row(self):
        '''Uh ... I think this should work, actually
        '''
        row_conf_queens = self.board.row_conflicted_queens()
        unoccupied_rows = self.board.find_unoccupied_rows()
        for qn in row_conf_queens:
            new_row_coords = self.moves_within_column(qn)
            for coord in new_row_coords:
                if coord[0] in unoccupied_rows:
                    conflicts_by_row = self.board.conflicts_for_move(qn, 0)
                    # The only issue right now is I have no obvious way 
                    # of figuring out the new conflict score of a move. 
                    return qn, coord, conflicts_by_row[coord[0]]


    def choose_next_move(self, verbose = False):
        '''The solver will only ever use two move choosing strategies. This
        arbitrates between the two of them.

        Returns the index of the queen to be moved, the location we
        will move it to, and a conflict score that is helpful for server-side 
        debugging but (at least for the time being, isn't surfaced now
        '''
        if self.board.is_row_conflicted():
            return self.queen_to_unoccupied_row()
        return self.worst_queen_to_best_column(verbose = verbose)

       
    def solve(self, verbose = False, stop_each = None):
        '''This is the main public method, essentially repeats the following 
        four  steps as long as the board isn't solved and we're under the move 
        threshold for the solver

            - If there are unoccupied rows, move a queen to an unoccupied row
            - Otherwise, find the queen that has the most conflicts
            - find a new column in the same row that minimizes conflicts
            - Move the queen to that column
        
        Returns nothing; all returning of data is handled in the 
        get_solution method()...
        '''
        if verbose:
            print(f"Solving the {self.board.dim}-queens problem ...")
            self.board.display()
        self.is_solved = self.check_if_solved(verbose = verbose)
        while not self.is_solved and self.below_limit:
            # THIS IS WHERE WE SHOULD CHECK FOR ROW CONFLICTS AND
            # GO INTO SOME SORT OF SUBROUTINE
            mv_queen, mv_coord, mv_conf = self.choose_next_move()
            if verbose:
                self.document_chosen_move(cand_queen = mv_queen, 
                    cand_coord = mv_coord, rslt_conf = mv_conf)
            self.move_queen_to_coord(focus_queen = mv_queen, 
                dest_coord = mv_coord, verbose = verbose)
            if isinstance(stop_each, int):
                if not self.is_solved and ((self.n_moves) % stop_each == 0):
                    print(f"Pausing after {self.n_moves} steps.")
                    if verbose:
                        self.board.display()
                    ipdb.set_trace()


    def random_queen_to_random_col(self):
        '''If we can't move one of our worst queens to an unseen state, this 
        random move will hopefully shake us out of that local optimum. In some 
        cases, randomly teleporting may converge faster than calling 
        `worst_queen_to_best_column` while backing off the conflict limit.

        TODO: I'm not using this right now, but it could be another strategy
        '''
        rand_queen = random.choice([v for v in range(self.board.dim)])
        curr_col = self.board.q_locs[rand_queen][1]
        rand_col = random.choice([v for v in range(self.board.dim) if v != curr_col])
        new_rand_pos = (self.board.q_locs[rand_queen][0], rand_col)
        resulting_state = self.board.get_state_string(rand_queen, new_rand_pos)
        if self.check_if_state_is_new(resulting_state):
            return rand_queen, new_rand_pos
        return None, None


if __name__ == "__main__":
    
    #TODO: Maybe move these to a tests folder?
    # Solution for a non row-conflicted board
    cb = chessBoard(dimension = 8, queen_seed = 42)
    sv = minConflictColumnSolver(board_object = cb, max_moves = 50)
    sv.solve()
    pprint(sv.walk_solution_path()["text"])
    print(sv.solution_shortdoc())
    print("\n")

    # Solution for a row conflicted board
    cb = chessBoard(dimension = 8, state_string = "1112131415161718")
    sv = minConflictColumnSolver(board_object = cb, max_moves = 50)
    sv.solve(verbose = True, stop_each = 7)
    pprint(sv.walk_solution_path()["text"])
    print(sv.solution_shortdoc())
    print("\n")

    # Test case for pruning solution path
    cb = chessBoard(dimension = 8, state_string = "1525384358627583")
    sv = minConflictColumnSolver(board_object = cb, max_moves = 50)
    print("ORIGINAL")
    sv.solve()
    pprint(sv.walk_solution_path()["text"])
    print(sv.solution_shortdoc())
    print("PRUNED")
    sv.collapse_seen_states()
    pprint(sv.walk_solution_path()["text"])
    print(sv.solution_shortdoc())
    



