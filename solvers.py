import random
import ipdb

from collections import Counter


class baseSolver(object):
    

    def __init__(self, board_object, max_moves = 50):
        '''Any solver needs a board configuration that it will presumably 
        solve and a maximum number of moves to make in any solution. We check 
        to see if that initial configuration is already solved, and then build 
        an initial seen_states object.

        The seen_states object will track child_state:parent_state for any 
        move that the solver makes. I haven't actually implemented this yet.
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


    def solution_shortdoc(self, n_steps):
        '''You know what would be great? Being able to deduce the number of 
        steps taken to solve this from the length of self.seen_states.

        We'll get there someday. Someday, we'll get there.
        '''
        if self.is_solved:
            print(f"Solved the {self.board.dim}-queens problem in {n_steps} steps!")
        else:
            print(f"Took {self.move_limit} steps and found no solution...")


    def solve(self):
        '''Only implemented in child classes
        '''
        raise NotImplementedError


class columnwiseCSPSolver(baseSolver):
    

    def choose_max_conflict_queen(self):
        '''Find the queen in the current board configuration that presents the 
        largest number of conflicts. Returns the queen_index of that queen, 
        choosing randomly in the case of ties.
        '''
        conf_by_qn = self.board.count_conflicts_by_queen()
        C = max(conf_by_qn.values())
        max_queens = [q for q in conf_by_qn.keys() if conf_by_qn[q] == C]
        return random.choice(max_queens)


    def get_min_conflict_column(self, focus_queen, curr_step, verbose = False):
        '''Again, ideally the state tree would be able to tell you what the 
        current step is ...

        A bigger to do...check to make sure that your new state isn't one you 
        have already visited in this solution path
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
        # Check columns - Also, should this be a standalone function?
        other_inds = [x for x in self.board.q_locs.values() if x != focus_ind]
        for k in conflicts_by_col.keys():
            diags = self.board.get_diagonals((focus_ind[0],k))
            diag_conf = set(diags).intersection(set(other_inds))
            conflicts_by_col[k] += len(diag_conf)
        conf = conflicts_by_col[focus_ind[1]]
        del(conflicts_by_col[focus_ind[1]])
        min_conf = sorted(conflicts_by_col.items(), key = lambda v: v[1])[0]
        # ARE WE ACTUALLY MOVING TO A NEW STATE?
        if verbose:
            focus_loc = (focus_ind[0] + 1, focus_ind[1] + 1)
            print(f"{curr_step + 1}. Queen at {focus_loc} causes {conf} conflicts.")
            print(f"Moving to column {min_conf[0] + 1} causes {min_conf[1]} conflicts.")
        return min_conf[0] 


    def move_queen_to_column(self, focus_queen, dest_column):
        '''Once you know the column you want to move the queen to, move 

        TODO: Check to see if the goal state is actually an unseen state
        before making the move. Otherwise, don't do it.

        This whole  "is my next step unseen?" question may be a separate 
        bit of functionality
        '''
        queen_start_pos = self.board.q_locs[focus_queen]
        parent_state = self.board.get_state_string()
        self.board.rows[queen_start_pos[0]][queen_start_pos[1]] = 0
        self.board.rows[queen_start_pos[0]][dest_column] = 1
        self.board.q_locs[focus_queen] = (queen_start_pos[0], dest_column)
        #self.seen_states[self.board.get_state_string] = queen_start_state
    

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

        TODO: Also, implementing repeated state checking might change some 
        of this entire thing.
        '''
        moves_made = 0
        if verbose:
            print(f"Solving the {self.board.dim}-queens problem ...")
            self.board.display()
        self.is_solved = self.check_if_solved(verbose = verbose)
        while not self.is_solved and moves_made < self.move_limit:
            mv_queen = self.choose_max_conflict_queen()
            mv_col = self.get_min_conflict_column(focus_queen = mv_queen, 
                curr_step = moves_made, verbose = verbose)
            # ARE WE ACTUALLY MOVING TO A NEW STATE?
            self.move_queen_to_column(focus_queen = mv_queen, 
                dest_column = mv_col)
            moves_made += 1
            self.is_solved = self.check_if_solved(verbose = verbose)
            if isinstance(stop_each, int): 
                if not self.is_solved and (moves_made % stop_each == 0):
                    print(f"Pausing after {moves_made} steps.")
                    if verbose:
                        self.board.display()
                    ipdb.set_trace()
        return moves_made


if __name__ == "__main__":

    pass
