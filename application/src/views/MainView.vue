<script setup>
import CardDisplay from '../components/CardDisplay.vue' 
import TeamForm from '../components/TeamForm.vue'
import LowerDisplay from '../components/LowerDisplay.vue'
import Footer from '../components/Footer.vue'
</script>

<template>
  <div class="content mb-0 p-0">
    <!-- left half -->
    <TeamForm />
    <!-- Right Half -->
    <div class="d-flex flex-column align-items-center justify-content-center">
      <CardDisplay />
      <LowerDisplay />
    </div>
    <!-- Footer -->
    <Footer />
  </div>
</template>

<style>
.content {
  display: grid;
  grid-template-columns: 17% auto;
  grid-template-rows: 1fr auto;
  column-gap: 20px;
  background: var(--color-background);
  flex: 1;
}

</style>
