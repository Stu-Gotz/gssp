<script async setup>
import CardTop from '../cardComponents/CardTop.vue';
import CardFrontImages from '../cardComponents/CardFrontImages.vue';
import CardEvs from '../cardComponents/CardEvs.vue';
import CardMoves from '../cardComponents/CardMoves.vue';

defineProps(['pokemon'])

function typeBackground(type) {
  const backgroundImageUrls = [];
  var backgroundPosition = '';

  for (const t in type) {
    backgroundImageUrls.push('url(./assets/' + type[t] + '.svg)')
  }
  if (backgroundImageUrls.length !== 1) {
    backgroundPosition = 'left, right'
  } else {
    backgroundPosition = 'center'
  }
  return {
    backgroundImage: backgroundImageUrls.join(', '),
    backgroundPosition
  }
}
</script>

<template>
  <div class="col card front align-items-center justify-content-evenly card-body" >
    <!-- Div for the images -->
    <CardFrontImages :style="typeBackground(pokemon.type)" :sprite="pokemon.spriteUrl" :helditem="pokemon.itemUrl" />
    <!-- Data about the pokemon, name, move, stats etc -->
    <CardTop :name="pokemon.name" :ability="pokemon.ability" :item="pokemon.item" :nature="pokemon.nature" />
    <div class="border border-info-subtle border-3 mx-2 rounded">
      <!-- EVs, to be input iteratively -->
      <CardEvs :evs="pokemon.evs" />
      <!-- Moves, as well to be input iteratively -->
      <CardMoves :moves="pokemon.moves" />
    </div>
  </div>
</template>

<style lang="scss">
.front {
  height: 100%;
  display: flex;
  align-items: center;
  flex-basis: calc(100% / 6);

  border: 5px solid var(--color-border);
  border-radius: 10px;
  background: #5a5179;
  box-shadow: 1px 1px 2px rgba(0, 0, 0, .3);

  background-size: contain;
  background-repeat: no-repeat;

  &:hover {
    transform: scale(1.05);
    box-shadow: 0px 0px 15px rgba(0, 0, 0, .5);
    z-index: 1000;
    overflow: visible;
  }

  @media(max-width: 1400px) {
    flex-basis: calc(100%/3);
    height: 50%;
  }
}

.card-body {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
}

.front {
  padding: 1rem 0;
}
</style>