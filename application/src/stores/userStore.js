import { defineStore } from "pinia";
import { useLocalStorage } from '@vueuse/core';
import { baseAPIUrl } from "../utils/utils";

export const useUserStore = defineStore("userStore", {
  state: () => ({
      user: {}
  }),
  actions: {
    setUserData(userData) {
      
      this.user = userData;
      this.user.isLoggedIn = true;

      console.log(this.user)
    },
    logout() {
      this.user.username = null;
      this.user.isLoggedIn = false;
      this.user.role = null;
      this.user.profileInfo = null;
      this.user.id = null;
    },
    async saveTeam(team) {
      if(this.user.profileInfo.teams){
        this.user.profileInfo.teams.push(team)
      } else {
        this.user.profileInfo.teams = [team]
      }
      try {
        const body = {
          id: this.user.mongo_id,
          username: this.user.username,
          team: team
        }
        const headers = {
          method: "POST",
          headers: {
            "Content-Type": "application/json",
          },
          body: JSON.stringify(body)
        }
        const res = await fetch(`${baseAPIUrl}/saveteam`, headers);
        if(res.status===200){
          console.log("Team has been saved.")
        }
      }catch(err){
        console.log(err)
      };
    },
  },
  getters: {
    getUsername(state) {
      return state.user.username
    },
    getUserRole(state) {
      return  state.user.role
    },
    getUserProfileData(state) {
      return state.user.profileData
    },
    getLoginStatus(state) {
      return state.user.isLoggedIn
    },
    getUserTeams(state) {
      return state.user.profileInfo.teams;
    }
  },
  persist: true,
});
