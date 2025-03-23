import { createApp } from 'vue'
import './style.css'
import 'uno.css'
import App from './App.vue'
import Antd from 'ant-design-vue';
import 'ant-design-vue/dist/antd.css';
import 'pretty-checkbox/src/pretty-checkbox.scss';
// 或使用编译后的 CSS
// import 'pretty-checkbox/dist/pretty-checkbox.min.css';


const app = createApp(App)

app.use(Antd)
app.mount('#app')
