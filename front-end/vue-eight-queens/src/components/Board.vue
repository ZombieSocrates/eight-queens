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
    }
  },
  methods: {
    getCellKey: function (rowInd, colInd) {
      return (rowInd - 1) * this.dimension + colInd
    },
    getRowKey: function (rowInd) {
      // probably could've just had this return an integer but meh
      return `row-${rowInd}`
    }
  }
}

</script>

<style>

</style>
