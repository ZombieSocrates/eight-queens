/*
MORE OR LESS A PORT OF THE FUNCTIONALITY FROM back-end/chess_board.py from
python into vanilla javascript. 
*/

const directions = {
    "UP":"up",
    "DOWN":"down",
    "LEFT":"left",
    "RIGHT":"right",
    "UP_LEFT":"up_left",
    "UP_RIGHT":"up_right",
    "DOWN_LEFT":"down_left",
    "DOWN_RIGHT":"down_right"
}


function getNextCoordinate(coord, direction) {
    switch (direction) {
        case directions.UP:
            return [coord[0] - 1, coord[1]]
        case directions.DOWN:
            return [coord[0] + 1, coord[1]]
        case directions.LEFT:
            return [coord[0], coord[1] - 1]
        case directions.RIGHT:
            return [coord[0], coord[1] + 1]
        case directions.UP_LEFT:
            return [coord[0] - 1, coord[1] - 1]
        case directions.UP_RIGHT:
            return [coord[0] - 1, coord[1] + 1]
        case directions.DOWN_LEFT:
            return [coord[0] + 1, coord[1] - 1]
        case directions.DOWN_RIGHT:
            return [coord[0] + 1, coord[1] + 1]
    }
}


function checkOutOfBounds(coord, boardSize, direction) {
    let upperBound = boardSize - 1
    switch (direction) {
        case directions.UP:
            return (coord[0] < 0)
        case directions.DOWN:
            return (coord[0] > upperBound)
        case directions.LEFT:
            return (coord[1] < 0)
        case directions.RIGHT:
            return (coord[1] > upperBound)
        case directions.UP_LEFT:
            return (coord[0] < 0) || (coord[1] < 0)
        case directions.UP_RIGHT:
            return (coord[0] < 0) || (coord[1] > upperBound)
        case directions.DOWN_LEFT:
            return (coord[0] > upperBound) || (coord[1] < 0)
        case directions.DOWN_RIGHT:
            return (coord[0] > upperBound) || (coord[1] > upperBound)
    }
}


/*
Fun fact: The Javascript equality operator will only return true if they
reference the same object. This means that [1,3] != [1,3], and this function 
gets around that
*/
function checkIfOccupied(coord, queenLocsArray) {
    let queenLocsStr = JSON.stringify(queenLocsArray)
    let coordStr = JSON.stringify(coord)
    return queenLocsStr.indexOf(coordStr) > -1 ? true : false
}


function movesInDirection(coord, queenLocsArray, direction, moves = []) {
    let blocked = false;
    while (!blocked) {
        let newCoord = getNextCoordinate(coord, direction)
        let hitPiece = checkIfOccupied(newCoord, queenLocsArray)
        let outOfBounds = checkOutOfBounds(newCoord, queenLocsArray.length, 
            direction)
        if (!hitPiece && !outOfBounds) {
            moves.push(newCoord)
            movesInDirection(newCoord, queenLocsArray, direction, moves)
        }
        else {blocked = true}
    return moves
    }
}


function getMoves(coord, queenLocsArray) {
    let possibleMoves = []
    Object.values(directions).forEach(function(dir) {
        let dirMoves = movesInDirection(coord, queenLocsArray, dir)
        possibleMoves.push(...dirMoves)
        }
    )
    return possibleMoves
}


/*
Converts a (dim * 2)-digit string into an array of [row,col]
coordinates at which to put queens. Maybe @deprecated?
*/
function parseStateString(stateString) {
    let positions = [];
    for (i = 0; i < stateString.length/2; i++) {
        rowInd = parseInt(stateString[2*i]);
        colInd = parseInt(stateString[2*i + 1]);
        positions.push([rowInd - 1, colInd - 1]);
    }
    return positions;
};

/*
Places n queens of a type specified by queenObj on the board given by
boardObj. We either parse the positions from a stateString, or choose
a random column for each row to have a queen
*/
function placeQueens(boardObj, queenObj, stateString = null) {
    if (stateString !== null) {
        let placements = parseStateString(stateString);
        placements.forEach(function(position) {
            // jsboard mandates that you put a clone of a piece in each position
            boardObj.cell(position).place(queenObj.clone())
            }
        )
    }
    else {
        let dim = boardObj.rows()
        for (i = 0; i < dim; i ++) {
            j = Math.floor(Math.random() * dim)
            boardObj.cell([i, j]).place(queenObj.clone())
        }
    }
};

/*
Returns a column for a row in the jsboard matrix where a 
queen is found, or null if no queen is in that row
*/
function locateQueenInRow(rowArray, startIndex = 0) {
    let colInd = rowArray.slice(startIndex).indexOf("1");
    return colInd == -1 ? null : colInd;
}

/*
Calls locateQueenInRow() for every row in the boardObject, 
returning an object with queen_index: [row_index, col_index]

TODO: This breaks when a queen is in more than one row
example string = "1112131415161718" 
*/
function getQueenLocations(boardObj) {
    let qLocs = {};
    let qIdx = 0;
    for (i = 0; i < boardObj.rows(); i ++) {
        row = boardObj.matrix()[i]
        j = locateQueenInRow(row);
        if (j === null) { continue }
        else {
            while (j !== null) {
                qLocs[qIdx] = [i, j]
                qIdx += 1
                j = locateQueenInRow(row, startIndex = j + 1)
            }
        }
    }
    return qLocs;
}

/*
Returns a representation of a chess board's current queen positions as
a (dim * 2)-digit string with row and column coordinates INDEXED FROM ONE.
These strings are the primary way the front end will ask the back end for
solutions.

Specifying move_queen and move_col will generate a potential future state.
This may be @deprecated for the perspective of the front end.
*/
function getStateString(boardObj, move_queen = null, move_col = null) {
    let stateStr = ""
    let qLocs = getQueenLocations(boardObj)
    for (qIdx in qLocs) {
        if (qIdx == move_queen) {
            stateStr += `${move_queen + 1}${move_col + 1}`
        }
        else {stateStr += `${qLocs[qIdx][0] + 1}${qLocs[qIdx][1] + 1}`}
    }
    return stateStr
}


// An archetypal board that will render in the browser
let b = jsboard.board({ attach:"game", size:"8x8", style:"checkerboard" });
b.cell("each").style({ width:"60px", height:"60px" });

// A generic queen that will get placed in each square.  
let queen = jsboard.piece({ text:"1", textIndent:"-9999px", 
    background:"url(src/jsboard/images/chess/queen.png", 
    width:"50px", height:"50px"});

// let stateString = null;
// using a fixed state as a test case for moving pieces
let stateString = "1525384358627583"

placeQueens(b, queen, stateString);
let foo = getQueenLocations(b);



console.log(foo);
console.log(getStateString(b));

