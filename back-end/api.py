from flask import Flask, request, jsonify, make_response
from pprint import pprint

from chess_board import chessBoard
from solvers import minConflictColumnSolver

app = Flask(__name__)

@app.route("/status")
def hello():
    return '''
        <h1> Time to move some 
            <a href = "https://youtu.be/HgzGwKwLmgM?t=35">Queens</a>
        </h1>  
    '''

@app.route("/solve", methods = ["GET"])
def solve_puzzle():
    '''Accessing args with [] indicates a required param (we throw a 
    400-BAD REQUEST if it isn't included).

    TODO A: Should I made the Bad Request case more explicit?
    TODO B: CORS????

    example usage: "http://localhost:5000/solve?dimension=8&state_string=1525384358627583"
    '''
    board_dim = int(request.args["dimension"])
    board_state = request.args["state"]
    max_moves = request.args.get("max_moves")
    if max_moves is None:
        max_moves = 50
    cboard = chessBoard(dimension = board_dim, state_string = board_state)
    solver = minConflictColumnSolver(board_object = cboard, max_moves = max_moves)
    solver.solve()
    rsp_data = solver.get_solution()
    rsp_headers = {"Content-Type":"application/json"}
    return make_response(rsp_data, 200, rsp_headers)


if __name__ == "__main__":
    app.run()