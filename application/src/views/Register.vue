<script setup>
import * as Yup from 'yup';
import YupPassword from 'yup-password'
import { reactive, ref } from 'vue';
import { useAuthStore } from '../stores/authStore';
import { useRouter } from 'vue-router';

const route = useRouter();
const errors = ref([]);
YupPassword(Yup);
const authStore = useAuthStore();

const userData = reactive({
  username : "",
  email : "",
  confirmEmail : "",
  password : "",
  confirmPassword : ""
});

// testing password to copypaste: P@ssw0rd

let registrationSchema = Yup.object({
  username: Yup.string().min(5, 'Username must be at least 5 characters.').max(30).required("Username is required."),
  email: Yup.string().min(5, "Email must be at least 5 characters.").email().required("Email is required."),
  confirmEmail: Yup.string().oneOf([Yup.ref('email'), null], 'Emails much match.'),
  password: Yup.string().min(8).max(20).minLowercase(1, 'Password must have at least one lower case letter. ')
    .minUppercase(1, 'Password must have at least one capital letter.')
    .minNumbers(1, 'Password must contain at least one number..')
    .minSymbols(1, 'Password must contain at least one symbol.').required(),
  confirmPass: Yup.string().oneOf([Yup.ref('password'), null], 'Passwords must match.')
});

function resetErrors(errorList){
  return errorList.splice(0);
}
async function register() {

  registrationSchema.validate(userData, { abortEarly: false })
    .then(userData => {
      resetErrors(errors.value);
    })
    .catch((err) => {
      resetErrors(errors.value);
      errors.value.push(...err.errors);
    })
    
    if(errors.value.length === 0) {
      const registrationData = {username: userData.username, password: userData.password, email: userData.email};
      if(authStore.registerUser(registrationData)){

        route.push({path: '/', replace: true});
      }
      
    }

  // pass to user server api to validate further and return errors
  // redirect to registration if unsuccessful
  // redirect to a "success" page before going to profile or main page (havent decided)
}
</script>

<template>
  
  <form @submit.prevent="register()" class="row w-50 position-absolute top-50 start-50 translate-middle">
    <ul class="d-flex flex-column justify-content-center align-items-center text-danger">
    <li class="text-danger" v-for="error in errors">{{ error }}</li>
  </ul>
    <div class="col d-flex flex-column justify-content-center align-items-center border-end mb-3">
      <div class="d-flex justify-content-center align-self-center input-group">
        <span class="input-group-text w-25">Username: </span>
        <div class="form-floating w-50">
          <input v-model="userData.username" class="form-control" type="text" name="username" id="registerName">
          <label for="registerName">Username</label>
        </div>
      </div>
      <div class="d-flex justify-content-center input-group">
        <span class="input-group-text w-25">Email: </span>
        <div class="form-floating">
          <input v-model="userData.email" class="form-control" type="email" name="email" id="registerEmail">
          <label for="registerEmail">Email address</label>
        </div>
      </div>
      <div class="d-flex justify-content-center input-group">
        <span class="input-group-text w-25">Confirm: </span>
        <div class="form-floating">
          <input v-model="userData.confirmEmail" class="form-control" type="email" name="emailconf" id="confirmEmail">
          <label for="confirmEmail">Confirm email </label>
        </div>
      </div>
      <div class="form-text">Must be a valid email address.</div>
    </div>
    <div class="col d-flex flex-column justify-content-center align-items-center mb-3">
      <div class="d-flex justify-content-center input-group">
        <span class="input-group-text w-25">Password: </span>
        <div class="form-floating">
          <input v-model="userData.password" class="form-control" type="password" name="password" id="registerPassword">
          <label for="registerPassword">Password </label>
        </div>
      </div>
      <div class="d-flex justify-content-center input-group">
        <span class="input-group-text w-25">Confirm: </span>
        <div class="form-floating">
          <input v-model="userData.confirmPassword" class="form-control" type="password" name="passconf" id="passconf">
          <label for="passconf">Confirm password </label>
        </div>
      </div>
      <div class="form-text">Password should use one digit and one special character.</div>
    </div>
    <div class="d-flex justify-content-center align-items-center input-group">
      <button class="btn btn-success mx-1 rounded" type="submit">Register</button>
      <RouterLink to="/"><button class="btn btn-danger mx-1 rounded" type="reset">Cancel</button></RouterLink>
    </div>
  </form>
</template>