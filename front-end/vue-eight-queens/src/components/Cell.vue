<template>
  <td class="cell" @click="changeColor()" :style="getColor()"> </td>
</template>

<script>
export default {
  name: 'Cell',
  props: {
    'coordinate': {
      type: Array,
      default: function () {
        return [0, 0]
      },
      // required: true,
      validator: function (value) {
        return value.length === 2
      }
    }
  },
  computed: {
    defaultColor: function () {
      if ((this.coordinate[0] % 2) === (this.coordinate[1] % 2)) {
        return '#000000'
      }
      return '#ffffff'
    }
  },
  data: function () {
    return {
      hasQueen: true,
      active: false
    }
  },
  methods: {
    changeColor () {
      if (this.hasQueen) {
        this.active = true
      }
    },
    getColor () {
      // may evolve into a more complex switch statement
      if (!this.active) {
        return { backgroundColor: this.defaultColor }
      }
      return { backgroundColor: '#90ee90' }
    }
  }
}
</script>

<style>

.cell {
  width: 90px;
  height: 90px;
  border: 2px solid #2c3e50;
}

</style>
