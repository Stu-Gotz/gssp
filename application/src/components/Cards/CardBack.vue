<script setup>
// import { Pokemon } from 'koffing';
import { titleCase, normaliseNames } from '../../utils/utils';
defineProps(['pokemon'])


</script>
<template>
  <div class="opacity-wrapper">
    <div class="col card back align-items-center justify-content-evenly card-body">

      <div class="card-body">
        <h2 class="card-back-name">{{ titleCase(normaliseNames(pokemon.name, " ", "-")) }}</h2>
        <ul>
          <li class="card-back-type" v-for="type in pokemon.type">{{ type.toUpperCase() }}</li>
        </ul>
        <!-- fill the rest of this in later, basically just a different version of the front, but i probably want to jazz it up a bit, otherwise it just makes sense to leave it blank -->
        <!-- Think I might list top team-mates or something? I dont know what do with this. -->
      </div>

    </div>
  </div>
</template>

<style lang="scss">
.back {
  background-image: url('/assets/cardback-bg2.svg');
  background-size: cover;
  background-position: center;

  border: 5px solid var(--color-border);
  border-radius: 10px;

  height: 100%;
  width: 100%;
  display: flex;
  align-items: center;
  flex-basis: calc(100% / 6);

  background-color: rgba(255, 255, 255, .2);
}


.opacity-wrapper {
  padding: 0;
  margin: 0;
  height: 100%;
  width: 100%;
  background-color: whitesmoke;
  border-radius: 10px;
}

.card-back-name {
  text-align: center;
  -webkit-text-stroke: 2px darkblue;
  color: goldenrod;
  font-weight: 800;
}

.card-back-types {
  display: flex;
  flex-direction: row;
}
</style>