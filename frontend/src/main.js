// import './assets/main.css'

import { createApp } from 'vue'
import { createPinia } from 'pinia'

import App from './App.vue'
import router from './router'
import piniaPluginPersistedstate from 'pinia-plugin-persistedstate'



import axios from 'axios'

// axios 기본 URL 설정
axios.defaults.baseURL = 'http://localhost:8000/api'; 




const app = createApp(App)

const pinia = createPinia()
pinia.use(piniaPluginPersistedstate)

// app.use(createPinia())
app.use(pinia)
app.use(router)

app.mount('#app')
