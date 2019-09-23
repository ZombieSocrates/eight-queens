from flask import Flask, request, jsonify, make_response
from pprint import pprint

from chess_board import chessBoard
from solvers import columnwiseCSPSolver

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

    TODO A: Actual informative error codes and type checking
    TODO B: Logic for solver.solve if no solution was found
    TODO C: CORS????


    example usage: "http://localhost:5000/solve?dimension=8&state_string=1525384358627583"
    '''
    board_dim = int(request.args["dimension"])
    board_state = request.args["state"]
    max_moves = request.args.get("max_moves")
    if max_moves is None:
        max_moves = 50
    cboard = chessBoard(dimension = board_dim, state_string = board_state)
    solver = columnwiseCSPSolver(board_object = cboard, max_moves = max_moves)
    ## check if solution was reached TKTK
    return jsonify(solver.solve())


if __name__ == "__main__":
    app.run()