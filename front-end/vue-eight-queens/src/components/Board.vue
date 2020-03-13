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
    'queens_count': {
      type: Number,
      default: 8,
      validator: function (value) {
        return value >= 0
      }
    }
  },
  // data: function () {
  //   moves: count of moves
  //   statesSeen: array of states?
  // }
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
    }
    // will need some updatePositions method
  },
  computed: {
    initialState: function () {
      let stateString = ''
      let takenKeys = []
      while (stateString.length < this.queens_count * 2) {
        let randKey = Math.floor(Math.random() *
          Math.pow(this.dimension, 2))
        if (!takenKeys.includes(randKey)) {
          takenKeys.push(randKey)
          stateString = `${stateString}${this.cellKeyAsState(randKey)}`
        }
      }
      return stateString
    },
    positions: function () {
      let takenCells = []
      for (let i = 0; i < this.queens_count; i++) {
        let rowPos = parseInt(this.initialState[2 * i]) - 1
        let colPos = parseInt(this.initialState[2 * i + 1]) - 1
        takenCells.push([rowPos, colPos])
      }
      return takenCells
    }
  }

}

</script>

<style>

</style>
