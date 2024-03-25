<script setup>
defineProps(['evs']);
</script>

<template>
  <ul class="card-text d-flex flex-wrap justify-content-center text-success text-center my-2">
      <li 
      v-for="(ev, idx) in evs"
      :key="idx"
      class="d-inline-block col-4 p-0 m-0">
        <strong>{{ idx.toUpperCase() }}</strong> {{ ev }}
      </li>
    </ul>
</template>