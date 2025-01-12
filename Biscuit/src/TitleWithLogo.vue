<script setup lang="ts">
import { ref } from "vue";
import { ElMessage } from "element-plus";

// 旋转速度
const spinSpeed = ref(2); // 初始速度为 2s

// 点击次数
const clickCount = ref(0); // 使用 ref 记录点击次数

// 处理图标点击事件
function handleIconClick() {
  spinSpeed.value = Math.max(0.1, spinSpeed.value - 0.2); // 每次点击减少 0.2s，最小为 0.1s
  clickCount.value += 1; // 点击次数加 1

  // 根据点击次数显示不同的消息
  if (clickCount.value === 1) {
    ElMessage({
      message: "你第一次点击了饼干，饼干开始加速！🍪",
      type: "success",
      duration: 5000, // 3 秒后消失
    });
  } else if (clickCount.value === 5) {
    ElMessage({
      message: "饼干转的好快！! 🍪🍪",
      type: "warning",
      duration: 5000,
    });
  } else if (clickCount.value === 10) {
    ElMessage({
      message: "不能再快了！！！🍪🍪🍪🍪",
      type: "warning",
      duration: 5000,
    });
  } else if (clickCount.value === 15) {
    ElMessage({
      message: "别点了，饼干要晕了！！！🍪🍪🍪🍪",
      type: "warning",
      duration: 5000,
    });
  } else if (clickCount.value === 24) {
    ElMessage({
      message: "那你点吧！！！🍪🍪🍪🍪",
      type: "warning",
      duration: 5000,
    });
  } else if (clickCount.value === 102) {
    ElMessage({
      message: "你不会还在点吧？🍪🍪🍪🍪",
      type: "warning",
      duration: 5000,
    });
  } else if (clickCount.value === 204) {
    ElMessage({
      message: "你是不是在试图用点击次数打破宇宙纪录？🍪🍪🍪🍪",
      type: "warning",
      duration: 5000,
    });
  } else if (clickCount.value === 300) {
    ElMessage({
      message: "你的手指是不是已经进化成了‘点击机器人’？🍪🍪🍪🍪",
      type: "warning",
      duration: 5000,
    });
  } else if (clickCount.value === 411) {
    ElMessage({
      message: "你已经点了411次，你好能坚持！🍪🍪🍪🍪",
      type: "warning",
      duration: 5000,
    });
  } else if (clickCount.value === 512) {
    ElMessage({
      message: "你的手指是不是已经变成了‘点击永动机’？🍪🍪🍪🍪",
      type: "warning",
      duration: 5000,
    });
  } else if (clickCount.value === 640) {
    ElMessage({
      message: "你是不是在试图用点击次数拯救世界？🍪🍪🍪🍪",
      type: "warning",
      duration: 5000,
    });
  } else if (clickCount.value === 720) {
    ElMessage({
      message: "你发现了隐藏的彩蛋，获得一枚勋章！🍪🍪🍪🍪",
      type: "warning",
      duration: 5000,
    });
  } else if (clickCount.value === 800) {
    ElMessage({
      message: "你解锁了隐藏成就：点击达人！🍪🍪🍪🍪",
      type: "warning",
      duration: 5000,
    });
  } else if (clickCount.value === 900) {
    ElMessage({
      message: "你解锁了隐藏成就：点击大师！🍪🍪🍪🍪",
      type: "warning",
      duration: 5000,
    });
  } else if (clickCount.value === 1023) {
    ElMessage({
      message: "难道，你也在期待这一刻？🍪🍪🍪🍪",
      type: "warning",
      duration: 10000,
    });
  } else if (clickCount.value >= 1024) {
    ElMessage({
      message: "♥️饼干真的很喜欢你♥️",
      type: "success",
      duration: 5000,
    });
  } else {
    ElMessage({
      message: `你点击了饼干`,
      type: "info",
      duration: 1000,
      grouping: true,
    });
  }
}
</script>

<template>
  <h1 class="title">
    <!-- 点击次数卡片 -->
    <div class="click-count-card" v-if="clickCount > 0">
      {{ clickCount >= 1024 ? '🍪♥️👸' : `Clicks: ${clickCount}` }}
    </div>

    <!-- 饼干图标和标题 -->
    <span
      class="icon spin"
      @click="handleIconClick"
      :style="{ animationDuration: `${spinSpeed}s` }"
      >🍪</span
    >
    <!-- 动态绑定 animationDuration -->
    BiscuitDownloader
  </h1>
</template>

<style scoped>
/* 标题样式 */
.title {
  font-family: "Pacifico", cursive, sans-serif; /* 使用艺术字体 */
  font-size: 3rem; /* 调整字体大小 */
  color: var(--card-text-color); /* 使用主题颜色 */
  text-align: center; /* 居中 */
  margin: 40px 0 20px 0; /* 调整间距：上 40px，下 20px */
  display: flex; /* 使用 flex 布局 */
  align-items: center; /* 垂直居中 */
  justify-content: center; /* 水平居中 */
  position: relative; /* 相对定位 */
}

.title .icon {
  margin-right: 10px; /* 图标与文字间距 */
  cursor: pointer; /* 鼠标悬停时显示为手型 */
  font-size: 3rem; /* 调整图标大小 */
  color: #000; /* 确保图标颜色 */
}

/* 点击次数卡片样式 */
.click-count-card {
  position: absolute; /* 绝对定位 */
  left: 20px; /* 距离左侧 20px */
  top: 50%; /* 垂直居中 */
  transform: translateY(-50%); /* 垂直居中 */
  background-color: var(--card-bg-color); /* 背景颜色 */
  color: var(--card-text-color); /* 文字颜色 */
  padding: 8px 16px; /* 内边距 */
  border-radius: 8px; /* 圆角 */
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1); /* 阴影 */
  font-size: 1rem; /* 字体大小 */
  font-weight: bold; /* 字体加粗 */
  border: 1px solid var(--button-border-color); /* 边框 */
}

/* 旋转动画 */
@keyframes spin {
  0% {
    transform: rotate(0deg);
  }
  100% {
    transform: rotate(360deg);
  }
}

.icon.spin {
  display: inline-block; /* 确保图标是内联元素 */
  animation: spin linear infinite; /* 确保动画属性正确 */
  user-select: none; /* 禁用文本选择 */
  transform-origin: center; /* 确保旋转中心为图标中心 */
}
</style>
