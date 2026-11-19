<script setup>
import { computed } from 'vue';
import { storeToRefs } from 'pinia';
import Card from './Card.vue';
import WelcomeCards from './Cards/WelcomeCards.vue';
import { useTeamStore } from '../stores/teamStore';
const teamStore = useTeamStore();
const { team: teamRef } = storeToRefs(teamStore);

const team = computed(() => teamRef.value.members ?? [])

</script>

<template>
  <!-- Container for the top half of the page -->
  <div class="card-area w-100">
    <!-- Create the row to hold the cards within the top half -->
    <div class="cards">
      <!-- This begins each card element. A goal in the project is to turn this into smaller components -->
      <!-- This is technically bad practice, I will optimize later if time is available. -->
      <WelcomeCards v-if="!team" />
      <!-- <CardFront v-else v-for="i in teamStore.team" :pokemon="i"/> -->
      <template v-else>
        <Card v-for="(mon, i) in team" :key="`${mon.name}-${i}`" :pokemon="mon" />
      </template>

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

.card-area {
  flex: 0 0 50%;
  min-height: 0;
}
</style>