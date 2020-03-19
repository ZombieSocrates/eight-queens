<template>

  <table class="board">
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
      currentState: this.startState,
      queenLocations: []
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
      let stateString = ''
      let takenKeys = []
      while (stateString.length < this.queensCount * 2) {
        let randKey = Math.floor(Math.random() *
          Math.pow(this.dimension, 2))
        if (!takenKeys.includes(randKey)) {
          takenKeys.push(randKey)
          stateString = `${stateString}${this.cellKeyAsState(randKey)}`
        }
      }
      return stateString
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
    // will need some updatePositions method
  },
  created: function () {
    this.currentState = this.initializeState()
    this.queenLocations = this.placeQueens()
  }
}

</script>

<style>

</style>
