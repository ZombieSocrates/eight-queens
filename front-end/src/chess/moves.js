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
