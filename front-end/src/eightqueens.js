/*
MORE OR LESS A PORT OF THE FUNCTIONALITY FROM back-end/chess_board.py from
python into vanilla javascript. 

In an ideal world, anything with a let statement would exist within this
script and would have it be sort of an app.js thing. All other functionality
(placement related, movement related, idk) would exist in separate files
and be imported. Except I am bad at imports


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
function placeQueens(boardObj, queensArray, stateString = null) {
    if (stateString !== null) {
        let placements = parseStateString(stateString);
        placements.forEach(function(position) {
            let idx = placements.indexOf(position);
            boardObj.cell(position).place(queensArray[idx]);
            }
        )
    }
    else {
        for (i = 0; i < queensArray.length; i ++) {
            j = Math.floor(Math.random() * queensArray.length)
            boardObj.cell([i, j]).place(queensArray[i])
        }
    }
};

/*
Returns a column for a row in the jsboard matrix where a 
queen is found, or null if no queen is in that row
*/
function locateQueenInRow(rowArray, startIndex = 0) {
    let colInd = rowArray.slice(startIndex).indexOf("1");
    return colInd;
}

/*
Calls locateQueenInRow() for every row in the boardObject, 
returning an object with queen_index: [row_index, col_index]

TODO: This breaks when a queen is in more than one row
example string = "1112131415161718". At least now it isn't 
in an infinite loop, but we are still messing stuff up 
*/
function getQueenLocations(boardObj) {
    let qLocs = {};
    let qIdx = 0;
    for (i = 0; i < boardObj.rows(); i ++) {
        row = boardObj.matrix()[i]
        j = locateQueenInRow(row);
        if (j == -1) { continue }
        else {
            qLocs[qIdx] = [i, j]
            qIdx += 1
            j = locateQueenInRow(row, startIndex = j + 1)
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


// A board that will render in the browser
let b = jsboard.board({ attach:"game", size:"8x8", style:"checkerboard" });
b.cell("each").style({ width:"60px", height:"60px" });

// A generic queen that will get placed in each square.  
let queen = jsboard.piece({ text:"1", textIndent:"-9999px", 
    background:"url(src/jsboard/images/chess/queen.png)", 
    width:"50px", height:"50px"});

// An array with ample "clones" of all the generic pieces in play
let piecesInPlay = [];
for (i = 0; i < b.rows(); i++) {
    piecesInPlay.push(queen.clone())
}

/* 
using a fixed state as a test case for moving pieces, and putting each
of the pieces in `piecesInPlay` at the appropriate places on the board
*/
let stateString = "1525384358627583"
// let stateString = null;
placeQueens(b, piecesInPlay, stateString);
let queenLocs = getQueenLocations(b);

// Debugging bullcrap
function debugLog() {
    console.log(`We're at state ${getStateString(b)}`)
    console.log(`Tracking ${Object.values(queenLocs).length} queens`)
    console.log(`The queens are here: ${JSON.stringify(queenLocs, space = 2)}`)
}

debugLog()

/* 
Everything below here follows the chessboard example from jsboard.
*/


// variables for the piece to move and its locations
let bindMovePiece, bindMoveLocs;


//give functionality to pieces TODO: CHANGE TO A MAP STATEMENT?
for (var i=0; i<piecesInPlay.length; i++) {
    piecesInPlay[i].addEventListener("click", function() { showMoves(this); });
    }

//show new locations
function showMoves(piece) {

    resetBoard();
    let pieceLoc = b.cell(piece.parentNode).where();
    let newLocs = getMoves(pieceLoc, Object.values(queenLocs));
    bindMoveLocs = newLocs;
    bindMovePiece = piece;
    bindMoveEvents(bindMoveLocs);
}

// bind move event to new piece locations
function bindMoveEvents(locs) {

    locs.forEach(function(loc) { 
        // Does this actualy change the color now?
        b.cell(loc).style({ "background":"lightgreen" });
        b.cell(loc).on("click", movePiece);
        }
    );
}

// actually move the piece and update the queen locations
function movePiece() {
    let userClick = b.cell(this).where();
    if (bindMoveLocs.indexOf(userClick)) {
        b.cell(userClick).place(bindMovePiece);
        queenLocs = getQueenLocations(b);
        //debug locs
        debugLog();
        resetBoard();
    }
}


function revertColor(loc) {
    if ((loc[0] % 2) == (loc[1] % 2)) {
        return { "background": "lightgray"};
    }
    return { "background":"gray" };
}

/* 
blow away all event listeners that start when something is clicked
and recolor the board. Do nothing if this is the first move you've
ever made
*/
function resetBoard() {
    if (bindMoveLocs === undefined) {
        return
    }
    bindMoveLocs.forEach(function(loc) {
        b.cell(loc).removeOn("click", movePiece);
        b.cell(loc).style(revertColor(loc))
        }
    );
}





