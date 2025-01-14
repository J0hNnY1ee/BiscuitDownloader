<script setup lang="ts">
import TopRightButtons from "./TopRightButtons.vue"; // 引入右上角按钮组件
import TitleWithLogo from "./TitleWithLogo.vue"; // 引入标题和 Logo 组件
import DownloadCards from "./DownloadCards.vue"; // 引入下载卡片组件
const particlesLoaded = (container: any) => {
  console.log("Particles container loaded", container);
};
</script>

<template>
  <div id="app">
    <vue-particles
      id="tsparticles"
      @particles-loaded="particlesLoaded"
      url="http://foo.bar/particles.json"
    />

    <vue-particles
      id="tsparticles"
      @particles-loaded="particlesLoaded"
      :options="{
        background: {
          color: {
            value: 'transparent',
          },
        },
        fpsLimit: 120,
        interactivity: {
          events: {
            onClick: {
              enable: true,
              mode: 'push',
            },
            onHover: {
              enable: true,
              mode: 'repulse',
            },
          },
          modes: {
            bubble: {
              distance: 100,
              duration: 2,
              opacity: 0.8,
              size: 40,
            },
            push: {
              quantity: 4,
            },
            repulse: {
              distance: 150,
              duration: 0.4,
            },
          },
        },
        particles: {
          color: {
            value: '#808080',
          },
          links: {
            color: '#808080',
            distance: 150,
            enable: true,
            opacity: 0.5,
            width: 1,
          },
          move: {
            direction: 'none',
            enable: true,
            outModes: 'bounce',
            random: false,
            speed: 6,
            straight: false,
          },
          number: {
            density: {
              enable: true,
            },
            value: 200,
          },
          opacity: {
            value: 0.5,
          },
          shape: {
            type: 'circle',
          },
          size: {
            value: { min: 1, max: 5 },
          },
        },
        detectRetina: true,
      }"
    />
  </div>
  <main class="container">
    <!-- 右上角按钮区域 -->
    <TopRightButtons />

    <!-- 标题和 Logo -->
    <TitleWithLogo />

    <!-- 下载卡片组件 -->
    <DownloadCards />

    <!-- 底部信息栏 -->
    <footer class="footer">
      <p>© 2025 J0hNnY1ee. All rights reserved.</p>
    </footer>
  </main>
</template>

<style scoped>
#tsparticles {
  position: fixed; /* 固定定位 */
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  z-index: -1; /* 将粒子效果置于页面内容之后 */
}

/* 底部信息栏 */
.footer {
  margin-top: 40px;
  padding: 20px;
  text-align: center;
  font-size: 14px;
  color: var(--card-text-color);
  opacity: 0.8; /* 降低透明度 */
}
</style>

<style>
/* 引入 Google Fonts */
@import url("https://fonts.googleapis.com/css2?family=Pacifico&display=swap");

:root {
  font-family: Inter, Avenir, Helvetica, Arial, sans-serif;
  font-size: 16px;
  line-height: 24px;
  font-weight: 400;

  --card-bg-color: #ffffff;
  --card-text-color: #0f0f0f;
  --input-bg-color: #ffffff;
  --input-text-color: #0f0f0f;
  --button-bg-color: #a78bfa; /* 浅紫色 */
  --button-text-color: #ffffff; /* 按钮文字颜色 */
  --button-border-color: #8b5cf6; /* 浅紫色边框 */
  --button-hover-bg-color: #8b5cf6; /* 悬停时稍深的紫色 */
  --button-hover-border-color: #7c3aed; /* 悬停时稍深的紫色边框 */

  color: #0f0f0f;
  background: linear-gradient(135deg, #f6f6f6, #e0e0e0); /* 浅色背景渐变 */
}

.dark {
  --card-bg-color: #1e1e1e;
  --card-text-color: #f6f6f6;
  --input-bg-color: #1e1e1e;
  --input-text-color: #f6f6f6;
  --button-bg-color: #7c3aed; /* 深色主题下的浅紫色 */
  --button-text-color: #ffffff; /* 按钮文字颜色 */
  --button-border-color: #6d28d9; /* 深色主题下的浅紫色边框 */
  --button-hover-bg-color: #6d28d9; /* 悬停时稍深的紫色 */
  --button-hover-border-color: #5b21b6; /* 悬停时稍深的紫色边框 */

  color: #f6f6f6;
  background: linear-gradient(135deg, #2f2f2f, #1e1e1e); /* 深色背景渐变 */
}
</style>