<script setup lang="ts">
import { ref } from 'vue';
import TopRightButtons from "./TopRightButtons.vue";
import TitleWithLogo from "./TitleWithLogo.vue";
import DownloadCards from "./DownloadCards.vue";
import SprinkleFlowers from './SprinkleFlowers.vue';
import { listen } from "@tauri-apps/api/event";

const showSprinkleFlowers = ref(false);

const particlesLoaded = (container: any) => {
  console.log("Particles container loaded", container);
};

// 模拟一个事件监听函数
const listenToEvent = () => {
  showSprinkleFlowers.value = true; // 显示 SprinkleFlowers

  // 1 秒后开始淡出
  setTimeout(() => {
    showSprinkleFlowers.value = false; // 触发淡出效果
  }, 1000);
};


listen("download_success", () => {
  listenToEvent();
});
</script>

<template>
  <div>
    <!-- 使用 v-show 和过渡效果 -->
    <transition name="fade">
      <SprinkleFlowers v-show="showSprinkleFlowers"></SprinkleFlowers>
    </transition>
  </div>

  <div id="app">
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
              enable: false,
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
              quantity: 2,
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
            value: 300,
            limit: 200,
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
    <TopRightButtons />
    <TitleWithLogo />
    <DownloadCards />
    <footer class="footer">
      <p>© 2025 J0hNnY1ee. All rights reserved.</p>
    </footer>
  </main>
</template>

<style scoped>
#tsparticles {
  position: fixed;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  z-index: -1;
}

.footer {
  margin-top: 40px;
  padding: 20px;
  text-align: center;
  font-size: 14px;
  color: var(--card-text-color);
  opacity: 0.8;
}

/* 淡入淡出过渡效果 */
.fade-enter-active,
.fade-leave-active {
  transition: opacity 0.5s ease;
}

.fade-enter-from,
.fade-leave-to {
  opacity: 0;
}
</style>

<style>
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
  --button-bg-color: #a78bfa;
  --button-text-color: #ffffff;
  --button-border-color: #8b5cf6;
  --button-hover-bg-color: #8b5cf6;
  --button-hover-border-color: #7c3aed;

  color: #0f0f0f;
  background: linear-gradient(135deg, #f6f6f6, #e0e0e0);
}

.dark {
  --card-bg-color: #1e1e1e;
  --card-text-color: #f6f6f6;
  --input-bg-color: #1e1e1e;
  --input-text-color: #f6f6f6;
  --button-bg-color: #7c3aed;
  --button-text-color: #ffffff;
  --button-border-color: #6d28d9;
  --button-hover-bg-color: #6d28d9;
  --button-hover-border-color: #5b21b6;

  color: #f6f6f6;
  background: linear-gradient(135deg, #2f2f2f, #1e1e1e);
}
</style>