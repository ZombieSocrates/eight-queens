<template>
  <td class="cell" @click="changeColor()" :style="cellStyle"></td>
</template>

<script>
export default {
  name: 'Cell',
  props: ['coordinate'],
  data: function () {
    return {
      hasQueen: true,
      cellStyle: {
        backgroundColor: '#000000'
      }
    }
  },
  methods: {
    changeColor () {
      if (this.hasQueen) {
        this.cellStyle.backgroundColor = '#ffffff'
      }
    }
  }
}
</script>

<style>

.cell {
  width: 90px;
  height: 90px;
  border: 6px solid #2c3e50;
  background-color: #000000;
}

</style>
