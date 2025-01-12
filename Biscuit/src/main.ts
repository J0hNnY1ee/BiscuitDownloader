import { createApp } from 'vue';
import { ElButton, ElIcon, ElInput, ElRow, ElCol } from 'element-plus'; // 按需导入
import 'element-plus/dist/index.css'; // 引入样式
import App from './App.vue';

const app = createApp(App);

// 按需注册组件
app.use(ElButton);
app.use(ElIcon);
app.use(ElInput);
app.use(ElRow);
app.use(ElCol);

app.mount('#app');