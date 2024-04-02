<script setup>
import { RouterLink } from 'vue-router';
import { useUserStore } from '../stores/userStore';
import { storeToRefs } from 'pinia';
import { computed } from 'vue';

const userStore = useUserStore();

userStore.$subscribe((mutation, state) => {return}, { detached: true })

</script>

<template>
  <nav class="navbar navbar-expand-lg bg-body-tertiary mt-0 pt-0">
    <div class="container-fluid">
      <RouterLink class="navbar-brand" to="/main">Main Page</RouterLink>
      <button class="navbar-toggler" type="button" data-bs-toggle="collapse" data-bs-target="#navbarSupportedContent"
        aria-controls="navbarSupportedContent" aria-expanded="false" aria-label="Toggle navigation">
        <span class="navbar-toggler-icon"></span>
      </button>
      <div class="collapse navbar-collapse" id="navbarSupportedContent">
        <ul class="navbar-nav me-auto mb-2 mb-lg-0">
          <li class="nav-item">
            <RouterLink class="nav-link active" to="/"><i class="bi bi-house-door"></i></RouterLink>
          </li>
          <li v-if="userStore.getLoginStatus" class="nav-item">
          <li class="nav-item dropdown">
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
          </li>
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
                <li><RouterLink class="nav-link active" to="/logout">Logout</RouterLink></li>
                <hr class="dropdown-divider">
              </li>
              <li><a class="dropdown-item" href="http://127.0.0.1:5500/index.html">API</a></li>
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