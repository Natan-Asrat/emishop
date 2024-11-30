import './assets/main.css'

import { createApp } from 'vue'
import { createPinia } from 'pinia'

import App from './App.vue'
import router from './router'
import './registerServiceWorker'
import axios from "axios";
import { useUserStore } from './stores/user'

const app = createApp(App)

app.use(createPinia())
app.use(router)
axios.defaults.baseURL = import.meta.env.VITE_API_URL;

const userStore = useUserStore();
// Call initStore to initialize user data from localStorage
userStore.initStore();
app.mount('#app')
