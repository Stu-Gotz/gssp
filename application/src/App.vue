<script setup>
import { RouterLink, RouterView } from 'vue-router';
import Navigation from './components/Navigation.vue';
</script>

<template>
  <Navigation />
  <RouterView />
</template>

<style lang="scss">

@media (min-width: 1024px) {
  header {
    display: flex;
    place-items: center;
    padding-right: calc(var(--section-gap) / 2);
  }

  .logo {
    margin: 0 2rem 0 0;
  }

  header .wrapper {
    display: flex;
    place-items: flex-start;
    flex-wrap: wrap;
  }
}

body {
  background-color: #9e82c2;
}
ul,
li {
  list-style: none;
  margin: 0;
  padding: 0;
}

.bug {
  color: #8fa832;
}
.dark {
  color: #444;
}
.dragon {
  color: #3238a8;
}
.electric {
  color: #a8ab00;
}
.fairy {
  color: #f9a3ff;
}
.fighting {
  color: #913d00;
}
.fire {
  color: #f06500;
}
.flying {
  color: #babcff;
}
.ghost {
  color: #500091;
}
.grass {
  color: #009113;
}
.ground {
  color: #694b30;
}
.ice {
  color: #9cf7ff;
}
.normal {
  color: #bfbfbf;
}
.poison {
  color: #bc00f5;
}
.psychic {
  color: #a144bd;
}
.rock {
  color: #5e4e46;
}
.steel {
  color: #969696;
}
.water {
  color: #3030ff;
}
</style>
