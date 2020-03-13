<template>

  <td class="cell" @click="setActive()" :style="getColor()">
    <li v-if="hasQueen" class='queen'>
      <icon name="chess-queen" scale=4></icon>
    </li>
  </td>

</template>

<script>

import 'vue-awesome/icons/chess-queen'

import Icon from 'vue-awesome/components/Icon'

export default {
  name: 'Cell',
  components: { Icon },
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
    // uncertain whether some of this should be moved into HTML classes
    return {
      hasQueen: this.checkOccupancy(),
      active: false
    }
  },
  methods: {
    setActive: function () {
      if (this.hasQueen) {
        this.active = !this.active
      }
    },
    getColor: function () {
      // may evolve into a more complex switch statement
      if (!this.active) {
        return { backgroundColor: this.defaultColor }
      }
      return { backgroundColor: '#90ee90' }
    },
    checkOccupancy: function () {
      /* stupid hack to make my Cell unit tests pass when the cell
      is being mounted  without a  parent Board. */
      if (this.$parent.positions === undefined) {
        return false
      }
      let stateString = JSON.stringify(this.$parent.positions)
      let cellCoord = JSON.stringify(this.coordinate)
      return stateString.indexOf(cellCoord) > -1
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

.queen {
  color: #f3d23e;
  list-style-type: none;
  display: inline-block;
}

</style>
