var b = jsboard.board({ attach:"game", size:"8x8", style:"checkerboard" });
b.cell("each").style({ width:"60px", height:"60px" });

var queen = jsboard.piece({ text:"1", textIndent:"-9999px", 
    background:"url(src/jsboard/images/chess/queen.png", 
    width:"50px", height:"50px"});

let stateString = "1522354855617682"

function parseStateString(stateString) {
	positions = [];
	for (i = 0; i < stateString.length/2; i++) {
		row_ind = parseInt(stateString[2*i]);
		col_ind = parseInt(stateString[2*i + 1]);
		positions.push([row_ind - 1, col_ind - 1]);
	}
	return positions
};

function placeQueens(boardObj, queenObj, stateString) {
	placements = parseStateString(stateString);
	console.log(placements);
	placements.forEach(function(position) {
		boardObj.cell(position).place(queenObj.clone())
	    })
	};

placeQueens(b, queen, stateString);