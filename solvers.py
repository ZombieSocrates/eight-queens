import random
import ipdb

from collections import Counter


class baseSolver(object):
    

    def __init__(self, board_object, max_moves = 50):
        '''Any solver needs a board configuration that it will presumably 
        solve and a maximum number of moves to make in any solution. We check 
        to see if that initial configuration is already solved, and then build 
        an initial seen_states object, which tracks child_state:parent_state 
        for any move that the solver makes. 
        '''
        self.board = board_object
        self.move_limit = max_moves
        self.is_solved = self.check_if_solved(verbose = False)
        self.seen_states = {self.board.get_state_string(): None}


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


    def check_if_state_is_new(self, next_state):
        return False if next_state in self.seen_states.keys() else True


    def solution_shortdoc(self):
        '''You know what would be great? Being able to deduce the number of 
        steps taken to solve this from the length of self.seen_states.

        We'll get there someday. Someday, we'll get there.
        '''
        if self.is_solved:
            n = len(self.seen_states) - 1
            print(f"Solved the {self.board.dim}-queens problem in {n} steps!")
        else:
            print(f"Took {self.move_limit} steps and found no solution...")


    def retrieve_solution_steps(self):
        steps_taken = []
        pointB = self.board.get_state_string()
        while pointB is not None:
            pointA = self.seen_states[pointB]
            if pointA is not None:
                steps_taken.append(self.describe_step(parent_state = pointA, 
                    child_state = pointB))
            pointB = pointA    
        return steps_taken[::-1]


    def describe_step(self, parent_state, child_state):
        for v in range(self.board.dim):
            p_pos = parent_state[(2 * v):2 * (v + 1)]
            c_pos = child_state[(2 * v):2 * (v + 1)]
            if p_pos != c_pos:
                s1 = f"Move queen at ({p_pos[0]},{p_pos[1]})"
                s2 = f"to ({c_pos[0]},{c_pos[1]})"
                return " ".join([s1, s2])


    def solve(self):
        '''Only implemented in child classes
        '''
        raise NotImplementedError


class columnwiseCSPSolver(baseSolver):
    

    def sort_queens_by_conflicts(self):
        '''Returns a priority queue for the queens that the solver may want to 
        move. The queen(s) with the largest number of current conflicts will
        appear at the front of the list.

        RENAME THIS TO SOMETHING LIKE `QUEEN PRIORITY QUEUE`
        '''
        conf_by_qn = self.board.count_conflicts_by_queen().items()
        qn_sort = sorted(conf_by_qn, key = lambda v: v[1], reverse = True) 
        return [w[0] for w in qn_sort]


    def sort_columns_by_conflicts(self, focus_queen, conf_threshold):
        '''Given a queen that the solver is considering moving, this method 
        will return an array of tuples containing possible destination columns 
        for that queen. The tuples are of the form (column index, n_conflicts), 
        and the array itself is sorted by n_conflicts increasing 

        RENAME THIS TO SOMETHING LIKE `COLUMN PRIORITY QUEUE`
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
        improve_cols = [v for v in conflicts_by_col.items() if v[1] <= conf_threshold]
        return sorted(improve_cols, key = lambda v: v[1])


    def document_decision(self, cand_queen, cand_col, rslt_conf):
        '''For debugging in implementing repeated state checking.'''
        curr_conf = self.board.count_conflicts_by_queen()[cand_queen]
        focus_ind = self.board.q_locs[cand_queen]
        focus_loc = (focus_ind[0] + 1, focus_ind[1] + 1)
        print(f"{len(self.seen_states)}. Queen at {focus_loc} causes {curr_conf} conflicts.")
        print(f"Moving to column {cand_col + 1} causes {rslt_conf} conflicts.")


    def move_queen_to_column(self, focus_queen, dest_column):
        '''Once you know the column you want to move the queen to, move 

        TODO: Check to see if the goal state is actually an unseen state
        before making the move. Otherwise, don't do it.

        This whole  "is my next step unseen?" question may be a separate 
        bit of functionality
        '''
        queen_start_pos = self.board.q_locs[focus_queen]
        self.board.rows[queen_start_pos[0]][queen_start_pos[1]] = 0
        self.board.rows[queen_start_pos[0]][dest_column] = 1
        self.board.q_locs[focus_queen] = (queen_start_pos[0], dest_column)
    

    def update_seen_states(self, focus_queen, dest_column):
        parent_st = self.board.get_state_string()
        child_st = self.board.get_state_string(move_queen = focus_queen, 
            to_col = dest_column)
        self.seen_states.update({child_st:parent_st})


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
        be extra verbose about the move we're making in the document_decision 
        method. Long-term I think this can just return the queen to move and 
        the column.

        TODO 2: Might be interesting to track how often the solver gets stuck in 
        local optima and needs to re-call itself. That's the only reason for 
        the verbose parameter right now)
        '''
        if conflict_cutoff is None:
            conflict_cutoff = max(self.board.count_conflicts_by_queen().values())
        queen_pq = self.sort_queens_by_conflicts()
        for cand_qn in queen_pq:
            col_pq = self.sort_columns_by_conflicts(cand_qn, conflict_cutoff)
            for c_tuple in col_pq:
                cand_col = c_tuple[0]
                cand_cnflct = c_tuple[1]
                resulting_state = self.board.get_state_string(cand_qn, cand_col)
                if self.check_if_state_is_new(resulting_state):
                    return cand_qn, cand_col, cand_cnflct
        if verbose:
            print("Relaxing conflict cutoff by one ...")
        return self.worst_queen_to_best_column(conflict_cutoff + 1, verbose)

        
    def random_queen_to_random_col(self):
        '''If we can't move one of our worst queens to an unseen state, this 
        random move will hopefully shake us out of that stasis.

        Not implemented in this solver right now, but this is an alternative to 
        repeatedly calling `worst_queen_to_best_column` while backing off the 
        conflict limit. In some cases, randomly teleporting will outperform the 
        former strategy in avoiding local optima.
        '''
        rand_queen = random.choice([v for v in range(self.board.dim)])
        curr_col = self.board.q_locs[rand_queen][1]
        rand_col = random.choice([v for v in range(self.board.dim) if v != curr_col])
        resulting_state = self.board.get_state_string(rand_queen, rand_col)
        if self.check_if_state_is_new(resulting_state):
            return rand_queen, rand_col
        return None, None


    def solve(self, verbose = False, stop_each = None):
        '''This is the main public method, essentially repeats the following 
        three steps as long as the board isn't solved and we're under the move 
        threshold for the solver

            - Find the queen that has the most conflicts
            - Find a new column in the same row that minimizes conflicts
            - Move the queen to that column
        

        TODO: In the long run, I don't think this method needs to return 
        anything. For the time being, we're returning the number of moves 
        made as a type of "score," but I'd love to just infer that from
        building out the seen_states attribute.
        '''
        if verbose:
            print(f"Solving the {self.board.dim}-queens problem ...")
            self.board.display()
        self.is_solved = self.check_if_solved(verbose = verbose)
        below_limit = (len(self.seen_states) - 1) < self.move_limit
        while not self.is_solved and below_limit:
            mv_queen, mv_col, mv_conf = self.worst_queen_to_best_column(verbose = verbose) 
            if verbose:
                self.document_decision(mv_queen, mv_col, mv_conf)
            # update_seen_states, change_the_board, and increment the movecount
            # the move_count and whether we're below limit can probably be baseSolver attributes.
            self.update_seen_states(focus_queen = mv_queen, 
                dest_column = mv_col)
            self.move_queen_to_column(focus_queen = mv_queen, 
                dest_column = mv_col)
            self.is_solved = self.check_if_solved(verbose = verbose)
            below_limit = (len(self.seen_states) - 1) < self.move_limit
            if isinstance(stop_each, int):
                if not self.is_solved and ((len(self.seen_states) - 1) % stop_each == 0):
                    print(f"Pausing after {len(self.seen_states) - 1} steps.")
                    if verbose:
                        self.board.display()
                    ipdb.set_trace()
        return len(self.seen_states) - 1


if __name__ == "__main__":

    pass
