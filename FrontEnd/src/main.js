import { createApp } from 'vue'
import App from './App.vue'
import router from './routers'
import 'bootstrap/dist/css/bootstrap.css'
import {BootstrapVue, IconsPlugin} from 'bootstrap'
createApp(App).use(router).mount('#app');
import 'bootstrap/dist/js/bootstrap.js'
