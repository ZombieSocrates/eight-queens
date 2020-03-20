<template>

  <table class="board" :key=currentState>
    <tr v-for="(rowInd, i) in dimension" class="row" :key="getRowKey(rowInd)">
      <Cell v-for="(colInd, j) in dimension" :key="getCellKey(rowInd, colInd)" :coordinate="[i, j]"></Cell>
    </tr>
  </table>

</template>

<script>

import Cell from '@/components/Cell'

export default {
  name: 'Board',
  components: { Cell },
  props: {
    'dimension': {
      type: Number,
      default: 8,
      validator: function (value) {
        return value >= 3
      }
    },
    'queensCount': {
      type: Number,
      default: 8,
      validator: function (value) {
        return value >= 0
      }
    },
    'startState': {
      type: String,
      default: null
    }
  },
  data: function () {
    return {
      moves: 0,
      currentState: this.startState
    }
  },
  methods: {
    getCellKey: function (rowInd, colInd) {
      return (rowInd - 1) * this.dimension + colInd
    },
    getRowKey: function (rowInd) {
      // probably could've just had this return an integer but meh
      return `row-${rowInd}`
    },
    cellKeyAsState: function (cellKey) {
      let rowValue = Math.floor(cellKey / this.dimension) + 1
      let columnValue = (cellKey % this.dimension) + 1
      return `${rowValue}${columnValue}`
    },
    initializeState: function () {
      return this.startState === null ? this.getRandomState() : this.startState
    },
    getRandomState: function () {
      let outState = ''
      let takenKeys = []
      while (outState.length < this.queensCount * 2) {
        let randKey = Math.floor(Math.random() *
          Math.pow(this.dimension, 2))
        if (!takenKeys.includes(randKey)) {
          takenKeys.push(randKey)
          outState = `${outState}${this.cellKeyAsState(randKey)}`
        }
      }
      return outState
    },
    coordsInBounds: function () {
      for (let d of this.currentState) {
        if ((parseInt(d) < 1) || (parseInt(d) > this.dimension)) {
          throw new TypeError('Queen Out Of Range')
        }
      }
      return true
    },
    correctQueensCount: function () {
      if (this.currentState.length !== this.queensCount * 2) {
        throw new TypeError('Improper Number of Queens')
      }
      return true
    },
    noDupePositions: function () {
      let occKeys = []
      for (let loc of this.queenLocations) {
        let locKey = this.getCellKey(loc[0], loc[1])
        if (occKeys.includes(locKey)) {
          throw new TypeError('Duplicate Queen Positions')
        }
        occKeys.push(locKey)
      }
      return true
    },
    placeQueens: function () {
      let takenCells = []
      for (let i = 0; i < this.queensCount; i++) {
        let rowPos = parseInt(this.currentState[2 * i]) - 1
        let colPos = parseInt(this.currentState[2 * i + 1]) - 1
        takenCells.push([rowPos, colPos])
      }
      return takenCells
    }
  },
  created: function () {
    this.currentState = this.initializeState()
  },
  // TODO: The errors are thrown, but they stay within the component
  // updated: function () {
  //   if (this.validBoardState !== true) {
  //     alert(this.validBoardState)
  //   }
  // },
  computed: {
    queenLocations: function () {
      return this.placeQueens()
    },
    validBoardState: function () {
      return (this.coordsInBounds() && this.correctQueensCount() &&
        this.noDupePositions())
    }
  }

}

</script>

<style>

</style>
