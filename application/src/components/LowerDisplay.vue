<!-- TO DO HERE
  - Change table to actually be a table
  - Filterable (maybe) definitely allow ascending/descending order for columns
  - use either SVG/Emoji or some kind of fancy text character and colour if use text based on up down or neutral movement
  - 
-->

<script setup>
import { computed, watch, ref } from "vue";
import { storeToRefs } from "pinia";
import { useStatStore } from "../stores/statStore";
import { useTeamStore } from "../stores/teamStore";

const statStore = useStatStore();
const teamStore = useTeamStore();
const { trends, error, loading } = storeToRefs(statStore);

const filter = ref(null);

const genString = computed(() =>
  teamStore.team.gen && teamStore.team.tier ? teamStore.team.gen + teamStore.team.tier : null
);

watch(
  genString,
  (tier) => {
    if (tier) statStore.getCompare(tier);

  },
  { immediate: true }
);


// comparisons = storeToRefs(await apiGet(`/compare/${teamStore.team.gen + teamStore.team.tier}`));
const { current, previous, older } = storeToRefs(statStore);

const tableColumns = [
  { key: "sprite", label: "" },
  { key: "pokemon", label: "Name" },
  { key: "current_rank", label: "Current Rank" },
  { key: "raw_usage", label: "Usage Rate (Raw)" },
  { key: "usage_pct", label: "Usage Rate (Percent)" },
  { key: "previous_rank", label: "Previous Rank" },
  { key: "change", label: "Change" }
];

function rankChange(oldRank, newRank) {

  if (oldRank > newRank) {
    return { 'background-color': '#f57e76' };
  } else if (newRank > oldRank) {
    return { 'background-color': '#69d682' };
  } else {
    return null;
  }
}

function sort() { return }
function sortBy() { return }
</script>

<template>
  <!-- This needs to be transformed into tables 
   Wants:
    Text filter/search
    asc/desc on non-name columns
    show change in rank and highlight red or green on neg/pos
    current rank, sprite, name, total use, % use, previous don't show older but use it for rank range in previous in parenthesis
    names are hyperlinks to dex page (not started yet)-->

  <div class="table-container w-100 d-flex flex-column justify-content-between">
    <h4>This is in development still. For this reason it only displays the top 25 of each tier. This may change, but
      unlikely.</h4>
    <!-- name search v-model -->
    <input v-model="filter" type="search" class="form-control mb-2" placeholder="Filter by name">

    <!-- table container -->
    <div class="table-responsive stats-table">
      <!-- BEGIN TABLE -->
      <table class="table table-sm table-hover align-middle mb-0">
        <thead class="table-light sticky-top">
          <tr>
            <th v-for="col in tableColumns" :key="col.key" role="button">
              {{ col.label }}
            </th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="row in trends" :key="row.pokemon">
            <td> sprite </td>
            <td> {{ row.pokemon }} </td>
            <td> {{ row.current_rank }} </td>
            <td> {{ row.raw_usage.toLocaleString() }} </td>
            <td> {{ row.usage_pct.toFixed(2) }} </td>
            <td> {{ row.previous_rank }} </td>
            <td> {{ row.previous_rank - row.current_rank }}</td>
          </tr>
        </tbody>
      </table>
    </div>
  </div>
  <!-- OLD KEEP AS FALLBACK -->
  <!-- <div class="d-flex h-50 w-100 justify-content-between align-items-start flex-1">
    <div class="h-100 w-100 overflow-auto">
      <p class="position-absolute text-center m-0 p-0 border-bottom">Current Ranking</p>
      <ul class="d-flex flex-column flex-1 align-items-end">
        <li class="text-align-left pe-2" v-for="curr in current"> {{
          curr.pokemon }} -- {{ curr.rank }}</li>
      </ul>
    </div>
    <div class="h-100 w-100 overflow-auto">
      <p class="position-absolute text-center m-0 p-0 border-bottom">Previous Ranking</p>
      <ul class="d-flex flex-column flex-1 align-items-end">
        <li class="text-align-left pe-2" v-for="prev in previous">{{ prev.pokemon }} -- {{ prev.rank }}</li>
      </ul>
    </div>
    <div class="h-100 w-100 overflow-auto">
      <p class="position-absolute text-center m-0 p-0 border-bottom">Older Ranking</p>
      <ul class="d-flex flex-column flex-1 align-items-end">
        <li class="text-align-left pe-2" v-for="old in older">{{ old.pokemon }} -- {{ old.rank }}</li>
      </ul>
    </div>
  </div> -->
</template>

<style scoped>
ul>* {
  font-size: .8rem;
  text-transform: capitalize;
}

.table-container {
  flex: 1 1 0;
  min-height: 0;
  overflow: hidden;
}

td {
  text-align: left;
}

th {
  &:not(:last-child) {
    border-right: 1px solid black;

  }

  &:first-child {
    border-top-left-radius: 10px;
  }

  &:last-child {
    border-top-right-radius: 10px;
  }
}

::-webkit-scrollbar {
  width: 12px;
}

::-webkit-scrollbar-track {
  -webkit-box-shadow: inset 0 0 6px rgba(0, 0, 0, 0.3);
  border-radius: 10px;
}

::-webkit-scrollbar-thumb {
  border-radius: 10px;
  -webkit-box-shadow: inset 0 0 6px rgba(0, 0, 0, 0.5);
}

.stats-table {
  flex: 1 1 0;
  min-height: 0;
  overflow: auto;
}
</style>