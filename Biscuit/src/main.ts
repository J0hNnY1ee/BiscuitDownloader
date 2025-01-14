import { createApp } from 'vue';
import { ElButton, ElIcon, ElInput, ElRow, ElCol } from 'element-plus'; // 按需导入
import 'element-plus/dist/index.css'; // 引入样式
import App from './App.vue';
import Particles from "@tsparticles/vue3";
import { loadSlim } from "@tsparticles/slim";




const app = createApp(App);

// 按需注册组件
app.use(ElButton);
app.use(ElIcon);
app.use(ElInput);
app.use(ElRow);
app.use(ElCol);
app.use(Particles, {
    init: async engine => {
      // await loadFull(engine); // you can load the full tsParticles library from "tsparticles" if you need it
      await loadSlim(engine); // or you can load the slim version from "@tsparticles/slim" if don't need Shapes or Animations
    },
  });



app.mount('#app');

