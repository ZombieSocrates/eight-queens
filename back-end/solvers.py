import random
import pdb

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


    def retrieve_solution_steps(self):
        '''TODO: The solve method should only call this particular method if 
        we terminate with is_solved True
        '''
        solution_json = {
            "is_solved": self.is_solved,
            "shortdoc": self.solution_shortdoc(),
            "data":defaultdict(list)
        }
        pointB = self.board.get_state_string()
        while pointB is not None:
            pointA = self.seen_states[pointB]
            if pointA is not None:
                txt_step = self.solution_step_as_text(parent_state = pointA, 
                    child_state = pointB)
                solution_json["data"]["text"].insert(0, txt_step)
                crd_pair = self.solution_step_as_coords(parent_state = pointA, 
                    child_state = pointB)
                solution_json["data"]["coords"].insert(0, crd_pair)
            pointB = pointA    
        return solution_json


    def get_change_between_states(self, parent_state, child_state):
        '''TODO (?): Won't always be slicing by two for larger orders of 
        magnitude of self.board.dim'''
        for v in range(self.board.dim):
            parent_pos = parent_state[(2 * v):2 * (v + 1)]
            child_pos = child_state[(2 * v):2 * (v + 1)]
            if parent_pos != child_pos:
                return parent_pos, child_pos


    def solution_step_as_coords(self, parent_state, child_state):
        step_coords = []
        for pos in self.get_change_between_states(parent_state, child_state):
            coord_pair = [int(v) - 1 for v in pos]
            step_coords.append(coord_pair)
        return step_coords


    def solution_step_as_text(self, parent_state, child_state):
        p_pos, c_pos = self.get_change_between_states(parent_state, child_state)
        s1 = f"Move queen at ({p_pos[0]},{p_pos[1]})"
        s2 = f"to ({c_pos[0]},{c_pos[1]})"
        return " ".join([s1, s2]) 



    def describe_step(self, parent_state, child_state):
        '''deprecated'''
        pass


    def solve(self):
        '''Only implemented in child classes
        '''
        raise NotImplementedError


class columnwiseCSPSolver(baseSolver):
    

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
        '''
        focus_ind = self.board.q_locs[focus_queen]
        conflicts_by_col = {k:0 for k in self.board.q_locs.keys()}
        # Check columns - Also, should this be a standalone function?
        curr_queens_by_col = Counter(v[1] for v in self.board.q_locs.values())
        for col, q_count in curr_queens_by_col.items():
            if col == focus_ind[1]:
                conflicts_by_col[col] += q_count - 1
            else:
                conflicts_by_col[col] += q_count
        # Check diagonals - Also, should this be a standalone function?
        other_inds = [x for x in self.board.q_locs.values() if x != focus_ind]
        for k in conflicts_by_col.keys():
            diags = self.board.get_diagonals((focus_ind[0],k))
            diag_conf = set(diags).intersection(set(other_inds))
            conflicts_by_col[k] += len(diag_conf)
        del(conflicts_by_col[focus_ind[1]])
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

        TODO 1: the only reason we'd ever return the conflict_cutoff is to
        be extra verbose about the move in the document_chosen_move method. 
        Long-term I think this can just return the queen to move and 
        the column.

        TODO 2: Might be interesting to track how often the solver gets stuck in 
        local optima and needs to re-call itself. That's the only reason for 
        the verbose parameter right now)
        '''
        if conflict_cutoff is None:
            conflict_cutoff = max(self.board.count_conflicts_by_queen().values())
        queen_pq = self.prioritize_queens()
        for cand_qn in queen_pq:
            col_pq = self.prioritize_cols(cand_qn, conflict_cutoff)
            for c_tuple in col_pq:
                cand_col = c_tuple[0]
                cand_cnflct = c_tuple[1]
                resulting_state = self.board.get_state_string(cand_qn, cand_col)
                if self.check_if_state_is_new(resulting_state):
                    return cand_qn, cand_col, cand_cnflct
        if verbose:
            print("Relaxing conflict cutoff by one ...")
        return self.worst_queen_to_best_column(conflict_cutoff + 1, verbose)


    def document_chosen_move(self, cand_queen, cand_col, rslt_conf):
        '''For debugging in implementing repeated state checking.'''
        curr_conf = self.board.count_conflicts_by_queen()[cand_queen]
        focus_ind = self.board.q_locs[cand_queen]
        focus_loc = (focus_ind[0] + 1, focus_ind[1] + 1)
        print(f"{len(self.seen_states)}. Queen at {focus_loc} causes {curr_conf} conflicts.")
        print(f"Moving to column {cand_col + 1} causes {rslt_conf} conflicts.")


    def update_board(self, focus_queen, dest_column):
        '''Once you know the column you want to move the queen to, change the 
        attributes of the underlying board to refelct that move. 
        '''
        queen_start_pos = self.board.q_locs[focus_queen]
        self.board.rows[queen_start_pos[0]][queen_start_pos[1]] = 0
        self.board.rows[queen_start_pos[0]][dest_column] = 1
        self.board.q_locs[focus_queen] = (queen_start_pos[0], dest_column)
        # This is more of a housekeeping step rather than actually crucial
        self.board.board_state = self.board.get_state_string()
    

    def update_seen_states(self, focus_queen, dest_column):
        parent_st = self.board.get_state_string()
        child_st = self.board.get_state_string(move_queen = focus_queen, 
            to_col = dest_column)
        self.seen_states.update({child_st:parent_st})


    def move_queen_to_column(self, focus_queen, dest_column, verbose = False):
        '''Handles all the instance attributes that need to change when we've 
        actually decided move one of the queens: updates the history of seen 
        states, updates the board locations, checks to see if we're at a goal
        state, and increments the solver's move counter.
        '''
        self.update_seen_states(focus_queen, dest_column)
        self.update_board(focus_queen, dest_column)
        self.is_solved = self.check_if_solved(verbose = verbose)
        self.below_limit = self.check_if_moves_remain()

       
    def solve(self, verbose = False, stop_each = None):
        '''This is the main public method, essentially repeats the following 
        three steps as long as the board isn't solved and we're under the move 
        threshold for the solver

            - Find the queen that has the most conflicts
            - Find a new column in the same row that minimizes conflicts
            - Move the queen to that column
        
        TODO: For the time being, we're returning human-readable steps 
        for the puzzle's solution, but this may eventually need to pass 
        back some format that a browser can understand.
        '''
        if verbose:
            print(f"Solving the {self.board.dim}-queens problem ...")
            self.board.display()
        self.is_solved = self.check_if_solved(verbose = verbose)
        while not self.is_solved and self.below_limit:
            mv_queen, mv_col, mv_conf = self.worst_queen_to_best_column(verbose = verbose)
            # If we called the above once and didn't get a queen or a column, 
            # here's where we might sub in random_queen_to_random_col() 
            if verbose:
                self.document_chosen_move(cand_queen = mv_queen, 
                    cand_col = mv_col, rslt_conf = mv_conf)
            self.move_queen_to_column(focus_queen = mv_queen, 
                dest_column = mv_col, verbose = verbose)
            if isinstance(stop_each, int):
                if not self.is_solved and ((self.n_moves) % stop_each == 0):
                    print(f"Pausing after {self.n_moves} steps.")
                    if verbose:
                        self.board.display()
                    pdb.set_trace()
        return self.retrieve_solution_steps()


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
        resulting_state = self.board.get_state_string(rand_queen, rand_col)
        if self.check_if_state_is_new(resulting_state):
            return rand_queen, rand_col
        return None, None


if __name__ == "__main__":
    
    cb = chessBoard(dimension = 8, state_string = "1525384358627583")
    sv = columnwiseCSPSolver(board_object = cb, max_moves = 50)
    soln_json = sv.solve()
    print(sv.solution_shortdoc())
    #TODO: Actually return the solution in a way the frontend can handle
    # pdb.set_trace()
    pprint(soln_json)


