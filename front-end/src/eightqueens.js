/*
MORE OR LESS A PORT OF THE FUNCTIONALITY FROM back-end/chess_board.py from
python into vanilla javascript. I tried to put the board as an attribute of 
some broader class with all these methods, and the browser yelled at me. 
See `foo.js` for more hilarious such failures


TODO: Perhaps move all the function definitions into a chess/placement.js 
file and then turn eightqueens.js into a minimal app
*/


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
let qLocs = getQueenLocations(b);
console.log(qLocs);
console.log(getStateString(b));