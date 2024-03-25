<script setup>
defineProps(['name', 'item', 'nature', 'ability']);
</script>

<template>
  <div
    class="card-text d-flex flex-column align-items-center justify-content-stretch w-100 p-0 mb-2 border-dark border-2 text-center">
    <div class="text-header w-100 d-flex align-self-center justify-content-center">
      <p class="p-0 m-0">{{ name }} @ {{ item }}</p>
      <p class="p-0 m-0">Nature: {{ nature }}</p>
      <p class="p-0 m-0">Ability: {{ ability }}</p>
    </div>
  </div>
</template>