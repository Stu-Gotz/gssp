import { defineStore } from 'pinia'
import { apiGet } from '../utils/utils.js'


export const useStatStore = defineStore('statStore', {
  state: () => ({
    current: null,
    previous: null,
    older: null,
    loading: false,
    error: null,
    trends: null,
  }),
  actions: {
    async setTier(era, tier) {
      this.tier = tier;
      this.loading = true;
      this.error = null;

      try {
        const results = await apiGet(`/${era}/${tier}`);
        this[era] = results.data;
      } catch (err) {
        this.error = err.message
      } finally {
        this.loading = false;
      }
    },
    async getCompare(tier) {
      this.loading = true;
      try {
        const results = await apiGet(`/compare/${tier}`);
        this.trends = results.data;
      } catch (err) {
        this.error = err.message;
      } finally {
        this.loading = false;
      }
    },
    getters: {
      getCurrent(state) {
        return state.current;
      },
      getPrevious(state) {
        return state.previous;
      },
      getOlder(state) {
        return state.older;
      }
    },
    persist: true,
  }
})
