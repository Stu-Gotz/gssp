import { defineStore } from "pinia";
import { useLocalStorage } from '@vueuse/core';

export const useUserStore = defineStore("userStore", {
  state: () => {
      {
      return {
        username: useLocalStorage('user', null),
        isLoggedIn: false,
        role: null,
        profileData: null,
        id: null,
      }
    }
  },
  actions: {
    setUserData(userData) {
      this.username = userData.username;
      this.isLoggedIn = true;
      this.id = userData.userId;
      this.role = userData.role;
      this.profileData = userData.profile;
    },
    logout() {
      this.username = null;
      this.isLoggedIn = false;
      this.role = null;
      this.profileData = null;
      this.id = null;
    },
  },
  getters: {
    getUsername(state) {
      return state.username
    },
    getUserRole(state) {
      return  state.username
    },
    getUserProfileData(state) {
      return state.profileData
    },
  },
  persist: true,
});
