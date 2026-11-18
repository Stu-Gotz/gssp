<script setup>
import CardFront from './Cards/CardFront.vue';
import CardBack from './Cards/CardBack.vue';
import { ref, computed } from 'vue';

const cardFace = computed(() => {
  if (!isFlipped.value) return CardFront;
  else return CardBack;
});
const isFlipped = ref(false);

function toggleFlip() {
  isFlipped.value = !isFlipped.value;
};

defineProps(['pokemon']);
</script>

<template>
  <div class="wrapper" @click="toggleFlip()">
    <component :is="cardFace" :pokemon="pokemon" />
  </div>
</template>

<style lang="scss">
.wrapper {
  display: flex;
  flex-direction: row;
  height: 100%;
  width: 100%;
}
</style>