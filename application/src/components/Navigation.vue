<script setup>
import { RouterLink } from 'vue-router';
import { useUserStore } from '../stores/userStore';
import { storeToRefs } from 'pinia';
import { computed } from 'vue';

const userStore = useUserStore();

userStore.$subscribe((mutation, state) => {return}, { detached: true })

</script>

<template>
  <nav class="navbar navbar-expand-lg mt-0 pt-0">
    <div class="container-fluid text-center">
      <RouterLink class="navbar-brand mx-auto" to="/main">Main Page</RouterLink>
      <button class="navbar-toggler" type="button" data-bs-toggle="collapse" data-bs-target="#navbarSupportedContent"
        aria-controls="navbarSupportedContent" aria-expanded="false" aria-label="Toggle navigation">
        <span class="navbar-toggler-icon"></span>
      </button>
      <div class="collapse navbar-collapse" id="navbarSupportedContent">
        <ul class="navbar-nav me-auto mb-2 mb-lg-0">
          <li>
            <RouterLink class="nav-link active" to="/"><i class="bi bi-house-door"></i></RouterLink>
          </li>
          <li v-if="userStore.getLoginStatus" class="nav-item dropdown">
            <!-- <li class="nav-item dropdown"> -->
            <!-- View if User is logged in -->
              <a class="nav-link dropdown-toggle" href="#" role="button" data-bs-toggle="dropdown" aria-expanded="false">
                Hello {{ userStore.getUsername }}
              </a>

              <ul class="dropdown-menu">
                <li>
                  <RouterLink class="nav-link active" to="/logout">Logout</RouterLink>
                </li>
                <li class="me-auto mb-2 mb-lg-0"><RouterLink class="nav-link active" to="/profile">View Profile</RouterLink></li>
              </ul>
            <!-- </li> -->
          </li>
          <!-- If not logged in, present option to login -->
          <li v-else class="nav-item">
            <RouterLink class="nav-link active" to="/login">Login</RouterLink>
          </li>
          <li class="nav-item dropdown">
            <a class="nav-link dropdown-toggle" href="#" role="button" data-bs-toggle="dropdown" aria-expanded="false">
              Other Pages
            </a>
            <ul class="dropdown-menu">
              <li>
                <RouterLink class="nav-link active" to="/logout">Logout</RouterLink>
                <hr class="dropdown-divider">
              </li>
              <li><a class="dropdown-item nav-link" href="http://127.0.0.1:5500/index.html">API</a></li>
              <li class="nav-item">
                <a class="nav-link disabled">Report a Bug</a>
              </li>
            </ul>
          </li>
        </ul>
      </div>
    </div>
  </nav>
</template>

<style lang="scss">

.container-fluid > * {
  margin-bottom: 5px;
}

.dropdown-menu {
  background-color: var(--color-background-mute);
}


.nav-link:hover,
.nav-link:focus,
a:hover {
    background-color: var(--color-background-soft) !important;
    // border-bottom: 1px solid var(--color-border) !important; //can't seem to get this to work without making things "jump"
    transition: none !important;
  }
</style>