<script setup>
defineProps(['moves'])
</script>

<template>
  <ul class="card-text row p-0 m-0 w-100 moves">
    <li class="move col-sm-6 p-0 m-0 text-center bold"
    v-for="(move, index) in moves"
    :key="index"
    :class="`${move.type}`">
      {{ move.name }}
    </li>
  </ul>
</template>

<style lang="scss">
  
.move {
  text-shadow: 0px 0px 1px #000;
}
</style>