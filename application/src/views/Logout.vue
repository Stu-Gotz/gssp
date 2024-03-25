<script setup>
import { useRouter } from 'vue-router';
import { useUserStore } from '../stores/userStore';


const route = useRouter();
const userStore = useUserStore();

function logoutUser() {
  userStore.logout();
  route.push({path: '/', replace: true});
}
</script>

<template>
<div class="d-flex flex-column align-items-center justify-content-center h-100"><h2>Do you want to logout?</h2>
<div class="d-flex justify-content-between buttons">
<button @click="logoutUser()" class="col btn btn-success form-control mx-1">Yes</button>
<RouterLink class="col btn btn-danger form-control mx-1 link-light link-opacity-100-hover" to="/">No</RouterLink></div>
</div>

</template>