<template>
  <div id="app">
    <img alt="Vue logo" src="./assets/logo.png">
    <!-- <HelloWorld msg="You are bad at vue"/> -->
    <Cell></Cell>
    <Cell :coordinate="[0,1]"></Cell>
  </div>
</template>

<script>
// import HelloWorld from '@/components/HelloWorld'
import Cell from '@/components/Cell'

export default {
  name: 'app',
  components: {
    // HelloWorld,
    Cell
  }
}
</script>

<style>
#app {
  font-family: 'Avenir', Helvetica, Arial, sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  text-align: center;
  color: #2c3e50;
  margin-top: 60px;
}
</style>
