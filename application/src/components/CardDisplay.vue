<script setup>
import CardFront from './Cards/CardFront.vue';
import CardBack from './Cards/CardBack.vue';
import Card from './Card.vue';
import WelcomeCards from './Cards/WelcomeCards.vue';
import { useTeamStore } from '../stores/teamStore';
const teamStore = useTeamStore();
</script>

<template>
  <!-- Container for the top half of the page -->
  <div class="h-50 w-100">
    <!-- Create the row to hold the cards within the top half -->
    <div class="cards">
      <!-- This begins each card element. A goal in the project is to turn this into smaller components -->
      <!-- This is technically bad practice, I will optimize later if time is available. -->
      <WelcomeCards v-if="!teamStore.team" />
      <!-- <CardFront v-else v-for="i in teamStore.team" :pokemon="i"/> -->
      <Card v-else :pokemon="teamStore.team.members" />
    </div>
  </div>
  <!-- End Top Half Page -->
</template>

<style lang="scss">
.cards {
  display: flex;
  justify-content: space-around;
  height: 100%;
  align-items: center;
  font-size: 12px;
  flex-wrap: nowrap;
  border: 4px outset #555;
  border-radius: 10px;
  padding: 2px;

  @media(max-width: 1400px) {
    flex-wrap: wrap;
  }
}
</style>