<script setup>
</script>

<template>
  <div class="welcome d-flex justify-content-evenly w-75">
      <img class="welcome-image" id="letter1" src="../icons/unown-h.png" alt="unown-h">
      <img class="welcome-image" id="letter2" src="../icons/unown-e.png" alt="unown-e">
      <img class="welcome-image" id="letter3" src="../icons/unown-l.png" alt="unown-l">
      <img class="welcome-image" id="letter4" src="../icons/unown-l.png" alt="unown-l">
      <img class="welcome-image" id="letter5" src="../icons/unown-o.png" alt="unown-o">
    </div>
</template>

<style>

.welcome-image {
  margin-bottom: 50px;
}
#letter1 {
  animation: bounce 4s ease-in-out infinite;
}
#letter2 {
  animation: bounce 6s ease-in-out infinite;
}
#letter3 {
  animation: bounce 8s ease-in-out infinite;
}
#letter4 {
  animation: bounce 5s ease-in-out infinite;
}
#letter5 {
  animation: bounce 7s ease-in-out infinite;
}

@keyframes bounce {
    /* shoutout: https://codepen.io/MarioDesigns/pen/woJgeo */
    0% {
      transform: translateY(5px);
    }
    50% {
      transform: translateY(-10px);
    }
    100% {
      transform: translateY(5px);
    }
  }
</style>