<script setup>
defineProps(['sprite', 'helditem'])

</script>


<template>
  <div class="d-flex justify-content-center  align-items-center card-images w-100">
    <!-- Pokemon sprite -->
    <img :src="sprite" alt="" srcset="" class="h-100">
    <!-- Item -->
    <img :src="helditem" alt="" class="object-fit-contain align-self-end justify-self-end helditem">
  </div>
</template>

<style lang="scss">
.card-images {
  background-size: contain;
  background-repeat: no-repeat;
  margin: 4px;
  height: 35%;
}

.helditem {
  margin-left: -2rem;
  margin-bottom: 10px;
}
</style>