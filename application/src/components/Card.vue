<script setup>
import CardFront from './Cards/CardFront.vue';
import CardBack from './Cards/CardBack.vue';
import { ref, computed } from 'vue';

defineProps(['pokemon']);
const isFlipped = ref(false);
const cardSide = computed(() => {
  if (!isFlipped.value) return CardFront;
  else return CardBack;
});

function toggleFlip() {
  isFlipped.value = !isFlipped.value;
};
</script>

<template>
  <component :is="cardSide" v-for="mon in pokemon" :pokemon="mon" @click="toggleFlip()" />
</template>