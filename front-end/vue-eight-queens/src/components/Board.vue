<template>

  <table class="board">
    <tr v-for="row in dimension" class="row"> 
    </tr>
  </table>

</template>

<script>

  import 'vue-awesome/icons/chess-queen'

  import Icon from 'vue-awesome/components/Icon'

  export default {
    name: 'Board',
    components: { Icon }, 
    props: {
      'dimension': {
        type: Number,
        default: 8
      }
    } 
  }
  
</script>

<style>

</style>