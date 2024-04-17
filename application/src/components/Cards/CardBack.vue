<script setup>
import { Pokemon } from 'koffing';

defineProps(['pokemon'])


</script>
<template>
  <div class="opacity-wrapper">
    <div class="col card back align-items-center justify-content-evenly card-body">

      <div class="card-body">
        <div class="card-title">{{ pokemon.name[0].toUpperCase() + pokemon.name.slice(1) }}</div> 
        <ul>
          <li style="display: flex; flex-direction: row;" v-for="type in pokemon.type">{{ type }}</li>
        </ul>
        <!-- fill the rest of this in later, basically just a different version of the front, but i probably want to jazz it up a bit, otherwise it just makes sense to leave it blank -->
        
      </div>
      
    </div>
  </div>
</template>

<style lang="scss">
  .back {
    background-image: url('/assets/cardback-bg2.svg');
    background-size: cover;
    background-position: center;
    
    height: 100%;
    width: 100%;
    display: flex;
    align-items: center;
    flex-basis: calc(100% / 6);
    
    background-color: rgba(255,255,255,.2);
  } 


  .opacity-wrapper {
    padding: 0;
    margin: 0;
    height: 100%;
    width: 100%;
    background-color: whitesmoke;
    border-radius: 10px;
  }
</style>