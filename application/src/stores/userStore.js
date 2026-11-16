import { defineStore } from "pinia";
import { baseAPIUrl } from "../utils/utils.js";

export const useUserStore = defineStore("userStore", {
  state: () => ({
    user: {
      id: null,
      username: null,
      profileInfo: null,
      role: null,
      token: null,
      isLoggedIn: false,
      join_date: null
    }
  }),
  actions: {
    setUserData(userData) {
      this.user = userData;
      this.user.isLoggedIn = true;
    },
    logout() {
      this.user.username = null;
      this.user.isLoggedIn = false;
      this.user.role = null;
      this.user.profileInfo = null;
      this.user.id = null;
      this.user.token = null;
      this.user.join_date = null;
    },
    async saveTeam(team) {
      if (!this.user.isLoggedIn === true) {
        throw new Error("You do not have permission to do that, please login.")
      }

      if (this.user.profileInfo.teams & this.user.profileInfo.teams.length >= 5) {
        throw new Error("Maximum number of teams reached, please delete a team to save or choose one to overwrite.")
      }
      try {
        const body = {
          team: team
        }
        const options = {
          method: "POST",
          headers: {
            "Content-Type": "application/json",
            "Authorization": `Bearer ${this.user.token}`
          },
          body: JSON.stringify(body)
        }
        const res = await fetch(`${baseAPIUrl}/saveteam`, options);

        if (res.status === 200) {
          if (this.user.profileInfo.teams) {
            this.user.profileInfo.teams.push(team)
          } else {
            this.user.profileInfo.teams = [team]
          }
        }
      } catch (err) {
        console.log(err)
      };
    },
  },
  getters: {
    getUsername(state) {
      return state.user.username
    },
    getUserRole(state) {
      return state.user.role
    },
    getUserProfileData(state) {
      return state.user.profileInfo
    },
    getLoginStatus(state) {
      return state.user.isLoggedIn
    },
    getUserTeams(state) {
      return state.user.profileInfo.teams;
    },
    getUserJoinDate(state) {
      console.log(state)
      return state.user.join_date.split('T')[0];
    }
  },
  persist: true,
});
