<script setup>
import { RouterLink, useRouter } from 'vue-router';
import { useAuthStore } from '../stores/authStore';
import { reactive } from 'vue';


const route = useRouter();
const user = reactive({
  username: "",
  password: ""
});

const authStore = useAuthStore();

function login() {
  const formData = {
    username: user.username, 
    password: user.password
  };
  if(authStore.loginUser(formData)){
    route.push({path: '/', replace: true});
  };
  
}

</script>

<template>
  <div class="container d-flex flex-column align-items-center justify-content-center h-50">
    <h4>some image here</h4>
    <form @submit.prevent="login()">
      <div class="input-group mb-3">
        <span class="input-group-text">Username: </span>
        <div class="form-floating">
          <input v-model="user.username" name="username" type="text" class="form-control" id="floatingUsernameInput"
            placeholder="Username">
          <label for="floatingUsernameInput">Username</label>
        </div>
      </div>
      <div class="input-group mb-3">
        <span class="input-group-text">Password: </span>
        <div class="form-floating">
          <input v-model="user.password" name="password" type="password" class="form-control" id="floatingPasswordInput"
            placeholder="password">
          <label for="floatingPasswordInput">Password</label>
        </div>
      </div>
      <div class="row g-3">
        <button class="col btn btn-success form-control mx-1">Login</button>
        <button class="col btn btn-danger form-control mx-1">Reset</button>
      </div>
    </form>
    <div class="fs-6">Don't have an account? <RouterLink to="./register" class="link-light link-opacity-100-hover">Register here</RouterLink>.</div>
  </div>
</template>