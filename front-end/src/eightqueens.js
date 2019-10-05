/*
MORE OR LESS A PORT OF THE FUNCTIONALITY FROM back-end/chess_board.py from
python into vanilla javascript. 

In an ideal world, anything with a let statement would exist within this
script and would have it be sort of an app.js thing. All other functionality
(placement related, movement related, idk) would exist in separate files
and be imported. Except I am bad at imports.
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


function checkOutOfBounds(coord, boardSize) {
    let minOfCoord = coord.reduce((a,b) => a < b ? a : b);
    let maxOfCoord = coord.reduce((a,b) => a > b ? a : b);
    if ((minOfCoord < 0) || (maxOfCoord >= boardSize)) {
        return true
    }
    return false 
}

/*
Fun fact: The Javascript equality operator will only return true if they
reference the same object. This means that [1,3] != [1,3], and this function 
gets around that
*/
function checkIfOccupied(coord, blockedCoordsArray) {
    let queenLocsStr = JSON.stringify(blockedCoordsArray)
    let coordStr = JSON.stringify(coord)
    return queenLocsStr.indexOf(coordStr) > -1 ? true : false
}

/*
TODO:
Right now this function relies on one global scope variable b.rows()...if I refactor
this into a separate file that would be problematic
*/
function movesInDirection(coord, blockedCoordsArray, direction, moves = []) {

    let newCoord = getNextCoordinate(coord, direction)
    let hitPiece = checkIfOccupied(newCoord, blockedCoordsArray)
    let outOfBounds = checkOutOfBounds(coord = newCoord, 
        boardSize = b.rows()) 
    if (!hitPiece && !outOfBounds) {
        moves.push(newCoord)
        movesInDirection(newCoord, blockedCoordsArray, direction, moves)
    }
    return moves
}

/*
Calculate all moves in the directions specified in moveDirections, taking 
into account any blocked locations in blockedCoordsArray


TODO: Would be excellent to put everything that getMoves() depends on into
a separate import ... potentially along with showMoves()
*/
function getMoves(coord, moveDirections, blockedCoordsArray) {
    let possibleMoves = [];
    moveDirections.forEach(function(dir) {
        let dirMoves = movesInDirection(coord, blockedCoordsArray, dir)
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
    let findIndex = rowArray.slice(startIndex).indexOf("1");
    if (findIndex == -1) {
        return null
    }
    return findIndex + startIndex;
}

/*
Calls locateQueenInRow() for every row in the boardObject, 
returning an object with queen_index: [row_index, col_index]
*/
function getQueenLocations(boardObj) {
    let qLocs = {};
    let qIdx = 0;
    for (i = 0; i < boardObj.rows(); i ++) {
        row = boardObj.matrix()[i];
        j = locateQueenInRow(row);
        if (j === null) {
            continue
        }
        while (j !== null) {
            qLocs[qIdx] = [i,j];
            qIdx += 1;
            j = locateQueenInRow(row, startIndex = j + 1);
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

/* 
An array with ample "clones" of all the generic pieces in play, 
each of which has an event listener added onto it
*/
let piecesInPlay = [];
for (i = 0; i < b.rows(); i++) {
    piecesInPlay.push(queen.clone());
    piecesInPlay[i].addEventListener("click", 
        function() { showMoves(this) });
}

/* 
using a fixed state as a test case for moving pieces, and putting each
of the pieces in `piecesInPlay` at the appropriate places on the board
*/
let stateString = "1525384358627583"
// let stateString = "1827374551667281"
// let stateString = "1221354454637282"
// let stateString = null;
placeQueens(b, piecesInPlay, stateString);
let queenLocs = getQueenLocations(b);
let queenConflicts = getConflictCountsByQueen(queenLocs);


// Debugging bullcrap
function debugLog() {
    console.log(`We're at state ${getStateString(b)}`);
    console.log(`Tracking ${Object.values(queenLocs).length} queens`);
    console.log(`The queens are here: ${JSON.stringify(queenLocs)}`);
    console.log(`Total conflicts: ${Object.values(queenConflicts)
        .reduce((a, b) => a + b, 0)}`);
    console.log(`Conflicts by queen ${JSON.stringify(queenConflicts)}`);
}


/*
An array of stateStrings that the user has navigated to. We can derive
moves made by getting length of this - 1

TODO: problem for another day, but I'm uncertain whether this will support
undo/redo functionality
*/
let stateCache = [getStateString(b)];


displayMoveCount();
displayConflictScore();
debugLog()


/* 
Variables for the piece to move and its locations. Both are undefined 
initially but they get updated as people interact with the board 
*/
let bindMovePiece, bindMoveLocs;





//show new locations
function showMoves(piece) {

    resetBoard();
    let pieceLoc = b.cell(piece.parentNode).where();
    console.log(pieceLoc);
    let newLocs = getMoves(coord = pieceLoc,
        moveDirections = Object.values(directions), 
        blockedCoordsArray = Object.values(queenLocs)
        );
    bindMoveLocs = newLocs;
    bindMovePiece = piece;
    bindMoveEvents(bindMoveLocs);
}

// bind move event to new piece locations
function bindMoveEvents(locs) {

    locs.forEach(function(loc) { 
        b.cell(loc).style({ "background":"lightgreen" });
        b.cell(loc).on("click", movePieceByUser);
        }
    );
}

/* 
Everything that needs to happen whenever the user (or the solver)
has actually moved a piece...
- update the queen locations object
- pop the state onto the cache
- display the count of moves in the appropriate div
- recalculate the conflicts object
- display the conflict score in the appropriate div
- wipe all eventListeners and visual


This is starting to reveal to me all of the complexity
baked into "Many things need to happen whenever state is managed"
*/
function updateStateFromMove() {
    queenLocs = getQueenLocations(b);
    stateCache.push(getStateString(b));
    displayMoveCount();
    queenConflicts = getConflictCountsByQueen(queenLocs);
    displayConflictScore();
    debugLog(); //should remove this eventually
    resetBoard();
}



function movePieceByUser() {
    let userClick = b.cell(this).where();
    if (bindMoveLocs.indexOf(userClick)) {
        b.cell(userClick).place(bindMovePiece);
        updateStateFromMove()  
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
        b.cell(loc).removeOn("click", movePieceByUser);
        b.cell(loc).style(revertColor(loc))
        }
    );
}

/* 
This function is called everytime a move is made and just
overwrites all the stuff in the moveCounter div
*/
function displayMoveCount() {
    let div = document.getElementById("moveCount");
    div.innerHTML = `<text><b>Count of Moves: </b> ${stateCache.length - 1}</text>`;
};


function displayConflictScore() {
    let div = document.getElementById("conflictScore");
    let score = Object.values(queenConflicts).reduce((a,b) => a + b, 0);
    let itemizedScores = [];
    Object.keys(queenConflicts)
        .sort((a, b) => queenConflicts[b] - queenConflicts[a])
        .forEach(function(k) {
            let qLabel = parseInt(k) + 1;
            let qScore = queenConflicts[k];
            itemizedScores.push(`<li>Queen ${qLabel} has ${qScore} conflicts</li>`)
            }
    )
    div.innerHTML = `
          <button onclick="showScoreByQueen()" class="dropdownBtn"><b>Current Conflicts: </b>${score}
          </button>
          <div id="scoreDropdown" class="dropdownItems">
              <ul>
              ${itemizedScores.join("")}
              </ul>
          </div>`
};


function showScoreByQueen() {
    document.getElementById("scoreDropdown").classList.toggle("show")
}

// if somebody clicks outside the dropdown menu, and it's open, it will go away
window.onclick = function(event) {
    if (!(event.target.matches(".dropdownBtn"))) {
        let dropdowns = document.getElementsByClassName("dropdownItems");
        for (let item of dropdowns) {
            if (item.classList.contains("show")){
                item.classList.remove("show")
            }
        }
    }
}



// CONFLICT COUNTING LOGIC THAT SHOULD EVENTUALLY BE IMPORTED IF I EVER FIGURE OUT HOW THAT WORKS
function countOrthogonalConflicts(qLocs) {
    let orthConflicts = {};
    for (let k in qLocs) {
        orthConflicts[k] = 0;
        for (let d in [0,1]) {
            let currDim = qLocs[k][d];
            let matchDims = Object.values(qLocs).filter(m => m[d] == currDim);
            orthConflicts[k] += (matchDims.length - 1);
        }
    }
    return orthConflicts
};




/*
This just calling getMoves EXCEPT we're only doing it for certain directions 
 and we're ignoring the condition where we hit a queen by 
 making blockedCoordsArray empty

 Ideally would get refactored into a moves file but womp womp ...
*/
function getDiagonals(loc) {
    let diagDirs = Object.values(directions)
        .filter(x => x.indexOf("_") > -1);
    return getMoves(coord = loc, 
        moveDirections = diagDirs,
        blockedCoordsArray = []
        )
};


function locInequality(locA, locB) {
    return (locA[0] != locB[0]) || (locA[1] != locB[1]);
}


function setIntersection(setA, setB) {
    let intrsct = new Set()
    for (let elem of setB) {
        if (setA.has(elem)) {
            intrsct.add(elem);
        }
    }
    return intrsct
};

/*
Doing a set intersection on an array of arrays was RIDICULOUS AND
TERRIBLE
*/
function countDiagonalConflicts(qLocs) {
    let diagConflicts = {};
    const locToString = x => `${x[0]}${x[1]}`
    for (let k in qLocs) {
        let thisLoc = qLocs[k];
        let diagsFromThis = getDiagonals(thisLoc)
            .map(locToString);
        let otherLocs = Object.values(qLocs)
            .filter(x => locInequality(x, thisLoc))
            .map(locToString);
       conflictSet = setIntersection(setA = new Set(diagsFromThis), 
           setB = new Set(otherLocs));
       diagConflicts[k] = conflictSet.size
    }
    return diagConflicts
};


function combineConflictCounts(conflictCountsArray) {
    let combined;
    for (let c of conflictCountsArray) {
        if (combined === undefined) {
            combined = Object.assign({},c);
            continue
        }
        for (let k of Object.keys(c)) {
            combined[k] += c[k];
        }
    }
    return combined
};


/*
Should all this conflict by queen stuff ever get ported to a separate file,
this is the primary export default type function that will actually get 
invoked in the front end.

The last two array operations are just filtering down the conflict object
to boot out keys where the value is 0
*/
function getConflictCountsByQueen(qLocs) {
    conflictCounts = [countOrthogonalConflicts(qLocs), 
        countDiagonalConflicts(qLocs)];
    mergedCounts = combineConflictCounts(conflictCounts);
    Object.keys(mergedCounts)
        .filter(k => mergedCounts[k] == 0)
        .forEach(k => delete mergedCounts[k])
    return mergedCounts
};


/*
THINGS RELATED TO SOLVING THE PUZZLE
*/
function movePieceAuto(fromLoc, toLoc) {
    let piecesInPlay = document.querySelectorAll("div[class*=pieceID]");
    for (pc of Array.from(piecesInPlay)) {
        if (!locInequality(b.cell(pc.parentNode).where(), fromLoc)) {
            bindMovePiece = pc
            break
        }
    }
    if (bindMovePiece !== undefined) {
        b.cell(toLoc).place(bindMovePiece);
        updateStateFromMove()
    }
}

/*
I should probably document this whole n_tries behavior much better. We
do a max of 50 moves, unless we're initiating this funciton through 
the Retry button, which will boost that limit by 50
*/
function solvePuzzle(moveLimit = undefined) {
    let xmlhttp = new XMLHttpRequest();
    let boardSize = b.rows();
    let boardState = getStateString(b);
    let url = `http://localhost:5000/solve?dimension=${boardSize}&state=${boardState}`
    if (moveLimit !== undefined) {
        url = `${url}&max_moves=${moveLimit}`
    }
    xmlhttp.onreadystatechange = function () {
        if (this.readyState == 4 && this.status == 200) {
            let response = JSON.parse(this.responseText);
            displaySolveStatusModal(response);
            //uhhh ... definitely get rid of this
            // verboseStepLog(response)
        }
    }
    xmlhttp.open("GET", url = url);
    //the line below is almost certainly bad practice and doesn't even work to get around CORS
    // xmlhttp.setRequestHeader("Access-Control-Allow-Origin","http://localhost:5000")
    xmlhttp.send();
}


/*
- If the http response returns and is_solved == True, the solveModal will 
            give user the option to Play the steps
            - Clicking a `Play` button in that modal dispels the modal and invokes 
            displaySteps()
            - If the http response is_solved == False, we still display the message, but
            provide an option to retry the solver OR we just straight up exit

*/
function displaySolveStatusModal(httpResponse) {
    let modal = document.getElementById("solveStatusModal");
    modal.style.display = "block";
    populateSolveModal(httpResponse);
    setButtonConsqequences(httpResponse);
}


/*
Needs to be more complicated to support/facilitate retries
*/
function populateSolveModal(httpResponse) {
    let content = document.getElementById("modalContentContainer");
    let spanChar = httpResponse["is_solved"] ? "&#10024 " : "&#10060 ";
    content.innerHTML = `<span> ${spanChar.repeat(8)}</span>
        <p>${httpResponse["message"]}</p>`;
    if (httpResponse["is_solved"]){
        content.innerHTML += `<button class="closeModalBtn"> 
            Show Me The Solution!</button>`;
    }
    else {
        content.innerHTML += `<button class="closeModalBtn"> 
            Retry with ${bumpMoveLimit(httpResponse)} Steps</button>
            <button class="closeModalBtn">
            Back to Original Board </button>`;
    }
}


/*
BARF
*/
function setButtonConsqequences(httpResponse) {
    let actBtns = Array.from(document.getElementsByClassName("closeModalBtn"));
    actBtns.forEach(function(b, i) {
        b.style.backgroundColor = httpResponse["is_solved"] ? "#92eb34": "#7909e8";
        b.onclick = function () {
            document.getElementById("solveStatusModal").style.display = "none";
            if (httpResponse["is_solved"]){
                displaySteps(httpResponse["solution"]["coords"])
            }
            else if (!httpResponse["is_solved"] && i == 0) {
                solvePuzzle(moveLimit = bumpMoveLimit(httpResponse))
            } 
        }
    });
}


/*
Apparently, executing a function every X seconds is non-trivial
Following this: https://scottiestech.info/2014/07/01/javascript-fun-looping-with-a-delay/

TODO: Sound effects?
*/
function displaySteps(stepArray, stepIndex = 0, totalTime = 5000) {
    let timePerStep = Math.floor(totalTime / stepArray.length);
    setTimeout(function () {
        movePieceAuto(stepArray[stepIndex][0], stepArray[stepIndex][1]);
        if (++stepIndex < stepArray.length){
            displaySteps(stepArray, stepIndex);
        }
    }, timePerStep)
}


function bumpMoveLimit(httpResponse, by = 50) {
    return httpResponse["n_tries_made"] + by;
}

/*
Uh, maybe have this appear somewhere on the page when 
the solution crops up?

Or this could be deprecated/for debugging purpses only
*/
function verboseStepLog(httpResponse) {
    console.log("Here's what we did")
    httpResponse["solution"]["text"].forEach( x => console.log(x));
}


