import { createApp } from 'vue'
import { createPinia } from 'pinia'
import App from './App.vue'
import router from './router'
import zhCN from 'naive-ui/es/locale/zh-CN.mjs'
import dateZhCN from 'naive-ui/es/date-locale/zh-CN.mjs'

const app = createApp(App)
const pinia = createPinia()

app.use(pinia)
app.use(router)
app.mount('#app')
