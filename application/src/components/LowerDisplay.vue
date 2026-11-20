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
import { normaliseNames, titleCase } from "../utils/utils";
const statStore = useStatStore();
const teamStore = useTeamStore();
const { trends, error, loading } = storeToRefs(statStore);

const filter = ref("");
const sortKey = ref("current_rank");
const sortAsc = ref(1);


const genString = computed(() =>
  teamStore.team.gen && teamStore.team.tier ? teamStore.team.gen + teamStore.team.tier : null
);

const filteredRows = computed(() => {
  const term = filter.value.trim().toLowerCase();
  //found this indexof 'trick' on jsperf, faster version of .includes()
  const rows = (trends.value ?? []).filter((row) => !term || row.pokemon.toLowerCase().indexOf(term) !== -1);

  const dir = sortAsc.value ? 1 : -1;
  return rows.sort((a, b) => {
    const x = a[sortKey.value];
    const y = b[sortKey.value];
    if (x == null || Number.isNaN(x)) return 1;
    if (y == null || Number.isNaN(y)) return -1;
    return (typeof x === "string" ? x.localeCompare(y) : x - y) * dir;
  });
});

watch(
  genString,
  (tier) => {
    if (tier) statStore.getCompare(tier);

  },
  { immediate: true }
);

const tableColumns = [
  { key: "sprite", label: "", sortable: false },
  { key: "pokemon", label: "Name", sortable: true },
  { key: "current_rank", label: "Current Rank", sortable: true },
  { key: "raw_usage", label: "Usage Rate (Raw)", sortable: true },
  { key: "usage_pct", label: "Usage Rate (Percent)", sortable: true },
  { key: "previous_rank", label: "Previous Rank", sortable: true },
  { key: "change", label: "Change", sortable: false }
];

function rankChange(change) {

  if (change > 0) {
    return "table-success";
  } else if (change < 0) {
    return "table-danger";
  } else {
    return null;
  }
}

function sortBy(key) {
  if (sortKey.value === key) {
    sortAsc.value = !sortAsc.value;
  } else {
    sortKey.value = key;
    sortAsc.value = key !== "change"; // ranks: 1 first; change: biggest climbers first
  }
}
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
    <h6 style="text-align: center;">This is in development still. For this reason it only displays the top 25 of each
      tier. This may change, but
      unlikely.</h6>
    <!-- name search v-model -->
    <input v-model="filter" type="search" class="form-control mb-2" placeholder="Filter by name">

    <!-- table container -->
    <div class="table-responsive stats-table">
      <!-- BEGIN TABLE -->
      <table class="table table-sm table-hover align-middle mb-0">
        <thead class="table-light sticky-top">
          <tr>
            <th v-for="col in tableColumns" :key="col.key" :role="col.sortable ? 'button' : undefined"
              @click="col.sortable && sortBy(col.key)"
              :aria-sort="sortKey === col.key ? (sortAsc ? 'ascending' : 'descending') : 'none'">
              {{ col.label }}
              <span class="sort-arrow" :class="{ invisible: sortKey !== col.key }" v-if="col.sortable">{{ sortAsc ? "▲"
                : "▼" }}</span>
            </th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="row in filteredRows" :key="row.pokemon" :class="rankChange(row.previous_rank - row.current_rank)">
            <td><a href="/#"> sprite </a></td>
            <td><a href="/#"> {{ normaliseNames(titleCase(normaliseNames(row.pokemon, ' ', '-')), '-', ' ') }} </a></td>
            <td> {{ row.current_rank }} </td>
            <td>{{ row.raw_usage.toLocaleString() }} </td>
            <td>{{ row.usage_pct.toFixed(2) }} </td>
            <td>{{ row.previous_rank }} </td>
            <td>{{ row.previous_rank - row.current_rank }} </td>
          </tr>
        </tbody>
      </table>
    </div>
  </div>
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
  white-space: nowrap;


  &:first-child {
    border-top-left-radius: 10px;
  }

  &:last-child {
    border-top-right-radius: 4px;
  }
}

.sort-arrow {
  display: inline-block;
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
  border-radius: 10px;
}
</style>