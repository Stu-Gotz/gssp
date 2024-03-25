//default Vue CSS files.
import './assets/main.css';

// Import Vue & Pinia.
import { createApp, watch } from 'vue';
import { createPinia } from 'pinia';
import piniaPluginPersistedState from "pinia-plugin-persistedstate";
// Import Bootstrap SCSS files
import './scss/styles.scss';

// Import all of Bootstrap's JS
import * as bootstrap from 'bootstrap';

import App from './App.vue';
import router from './router';

const app = createApp(App);
const pinia = createPinia();
watch(
    pinia.state,(state) => {
        localStorage.setItem("user", JSON.stringify(state.userName));
    },
    {
        deep: true
    }
);

pinia.use(piniaPluginPersistedState);
app.use(pinia);

app.use(router);

app.mount('#app');