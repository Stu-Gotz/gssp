import { defineStore } from "pinia";
import { useUserStore } from "./userStore";

const userStore = useUserStore();

const baseUrl = "http://127.0.0.1:5500/apiv1";
export const useAuthStore = defineStore("authStore", {
  state: () => ({
    token: null,
  }),
  actions: {
    async loginUser(loginForm) {
      try {
        const headers = {
          method: "POST",
          headers: {
            "Content-Type": "application/json",
          },
          body: JSON.stringify(loginForm),
        };
        const res = await fetch(`${baseUrl}/login`, headers);
        if (res.status === 200) {
          const data = await res.json();

          this.token = data.token;
          //set userStore data so it can be accessed through the profile.
          userStore.setUserData({username: data.username, role: data.role, profile: data.userProfile, userId: data.mongo_id})

          return true;
        } else {
          console.log("Unable to login.");
        }
      } catch (err) {
        
        console.log(err.message);
        return false;
      }
    },
    async registerUser(registerForm) {
      try {
        const headers = {
          method: "POST",
          headers: {
            "Content-Type": "application/json",
          },
          body: JSON.stringify(registerForm),
        };
        const res = await fetch(`${baseUrl}/register`, headers);
        console.log(res)
        if (res.status === 201) {
          console.log("Successful registration");
          const data = await res.json();
          //login user after registration, saves user clicks
          this.loginUser({username: registerForm.username, password: registerForm.password});
          return true;
        } else {
          console.log("Unable to register user");
        }
      } catch (err) {
        console.log(err.message);
        return false;
      }
    },
  },
});
