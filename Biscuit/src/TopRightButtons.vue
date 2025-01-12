<script setup lang="ts">
import { useDark, useToggle } from '@vueuse/core';
import { Sunny, Moon } from '@element-plus/icons-vue'; // 按需导入 Element Plus 图标
import { Icon } from '@iconify/vue'; // 按需导入 Iconify 组件
import { open } from '@tauri-apps/plugin-shell'; // 导入 Tauri 的 open 方法


// 深色模式
const isDark = useDark(); // 自动检测系统主题
const toggleDark = useToggle(isDark); // 切换深色模式

// 打开 GitHub 链接
async function openGithub() {
  try {
    // 使用 Tauri 的 open 方法打开链接
    await open('https://github.com/J0hNnY1ee/BiscuitDownloader');
    console.log('GitHub link opened successfully');
  } catch (err) {
    console.error('Failed to open GitHub link:', err);
  }
}
// 打开邮件客户端
async function sendEmail() {
  const email = 'j0h1eenny@gmail.com'; // 替换为你的目标邮箱地址
  const subject = 'I Miss You'; // 邮件主题
  const body = ''; // 邮件正文
  const mailtoLink = `mailto:${email}?subject=${encodeURIComponent(subject)}&body=${encodeURIComponent(body)}`;
  try {
    await open(mailtoLink);
    console.log('Email client opened successfully');
  } catch (err) {
    console.error('Failed to open email client:', err);
  }
}
</script>

<template>
  <div class="top-right-buttons">
    <!-- GitHub 链接图标 -->
    <el-button class="github-button" @click="openGithub">
      <Icon icon="mdi:github" width="20" height="20" />
    </el-button>

    <!-- Email 图标 -->
    <el-button class="email-button" @click="sendEmail">
      <Icon icon="mdi:email" width="20" height="20" />
    </el-button>

    <!-- 切换深色模式的按钮 -->
    <el-button class="toggle-dark-button" @click="toggleDark()">
      <el-icon :size="20"><Sunny v-if="!isDark" /><Moon v-else /></el-icon>
    </el-button>
  </div>
</template>

<style scoped>
.top-right-buttons {
  position: absolute;
  top: 16px;
  right: 16px;
  display: flex;
  gap: 8px; /* 按钮之间的间距 */
}

.github-button,
.email-button,
.toggle-dark-button {
  border: none; /* 移除边框 */
  background: none; /* 移除背景 */
  padding: 0; /* 移除内边距 */
  min-width: auto; /* 移除最小宽度 */
  box-shadow: none; /* 移除阴影 */
  width: 32px; /* 固定宽度 */
  height: 32px; /* 固定高度 */
  border-radius: 8px; /* 圆角 */
  display: flex;
  align-items: center;
  justify-content: center;
  cursor: pointer;
  color: inherit; /* 继承父元素颜色 */
}

.github-button:hover,
.email-button:hover,
.toggle-dark-button:hover {
  opacity: 0.8; /* 悬停时降低透明度 */
}

.github-button:active,
.email-button:active,
.toggle-dark-button:active {
  background-color: rgba(0, 0, 0, 0.1); /* 按下时显示圆角正方形背景 */
}
</style>