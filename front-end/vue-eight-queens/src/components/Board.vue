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
  //   out = {
  //     positions: []
  //   }
  //   for (let q = 0, q < this.queens_count, q++) {
  //       let p_r = parseInt(this.initialState[2*q])
  //       let p_q = parseInt(this.initialState[2*q + 1])
  //       out.positions.push([p_r, p_q])
  //   }
  //   return out
  // }
  methods: {
    getCellKey: function (rowInd, colInd) {
      return (rowInd - 1) * this.dimension + colInd
    },
    getRowKey: function (rowInd) {
      // probably could've just had this return an integer but meh
      return `row-${rowInd}`
    }
  },
  computed: {
    initialState: function () {
      // let stateString = ''
      let takenCells = []
      while (takenCells.length < this.queens_count) {
        let randCell = Math.floor(Math.random() *
          Math.pow(this.dimension, 2))
        if (!takenCells.includes(randCell)) {
          let r = Math.floor(randCell / this.dimension)
          let c = randCell % this.dimension
          takenCells.push([r, c])
        }
      }
      return takenCells
    }
  }

}

</script>

<style>

</style>
