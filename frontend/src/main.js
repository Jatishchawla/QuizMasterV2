import { createApp } from 'vue'
import './style.css'
import App from './App.vue'
import { router } from "./routes.js"



createApp(App).use(router).mount('#app')

// const app = new Vue({
//     el : "#app",
//     template:``,
//     data,
//     methods
// })