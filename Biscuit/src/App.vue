<script setup lang="ts">
import TopRightButtons from './TopRightButtons.vue'; // 引入右上角按钮组件
import TitleWithLogo from './TitleWithLogo.vue'; // 引入标题和 Logo 组件
import { ref } from 'vue';
import { ElMessage } from 'element-plus';

// 下载链接和方式
const downloadLink = ref("");
const downloadMethod = ref("Method 1");

// 下载进度
const downloadProgress = ref(0); // 进度值（0-100）
const isDownloading = ref(false); // 是否正在下载

// 模拟下载
function startDownload() {
  if (!downloadLink.value) {
    ElMessage.warning('Please enter a download link.'); // 使用 ElMessage 提示
    return;
  }

  isDownloading.value = true;
  downloadProgress.value = 0;

  const interval = setInterval(() => {
    if (downloadProgress.value < 100) {
      downloadProgress.value += 10; // 每次增加 10%
    } else {
      clearInterval(interval);
      isDownloading.value = false;
      ElMessage.success('Download complete!'); // 使用 ElMessage 提示
    }
  }, 500); // 每 500ms 更新一次进度
}
</script>

<template>
  <main class="container">
    <!-- 右上角按钮区域 -->
    <TopRightButtons />

    <!-- 标题和 Logo -->
    <TitleWithLogo />

    <!-- 下载器卡片布局 -->
    <div class="cards">
      <!-- 输入链接卡片 -->
      <div class="card">
        <h3>Enter Download Link</h3>
        <input 
          v-model="downloadLink" 
          placeholder="Enter download link" 
          class="input-box" 
        />
        <p class="card-description">Paste your download link above to get started.</p>
      </div>

      <!-- 下载方式和按钮卡片 -->
      <div class="card">
        <div class="card-content">
          <div class="card-left">
            <h3>Choose Download Method</h3>
            <div class="toggle-button-group">
              <button 
                :class="{'active': downloadMethod === 'Method 1'}" 
                @click="downloadMethod = 'Method 1'"
              >
                下载单曲
              </button>
              <button 
                :class="{'active': downloadMethod === 'Method 2'}" 
                @click="downloadMethod = 'Method 2'"
              >
                下载用户全部歌曲
              </button>
              <span class="toggle-slider" :style="{'left': downloadMethod === 'Method 1' ? '0%' : '50%'}"></span>
            </div>

            <!-- 下载按钮 -->
            <button @click="startDownload" class="download-button" :disabled="isDownloading">
              <span class="icon">⬇️</span> 
              {{ isDownloading ? 'Downloading...' : 'Download' }}
            </button>
          </div>

          <!-- 环形进度条 -->
          <div class="card-right">
            <el-progress 
              type="circle" 
              :percentage="downloadProgress" 
              :status="downloadProgress === 100 ? 'success' : ''" 
            />
          </div>
        </div>
      </div>
    </div>

    <!-- 底部信息栏 -->
    <footer class="footer">
      <p>© 2025 J0hNnY1ee. All rights reserved.</p>
    </footer>
  </main>
</template>

<style scoped>
.cards {
  display: flex;
  flex-direction: column;
  gap: 20px;
  align-items: center;
  margin-top: 40px; /* 增加顶部间距 */
}

.card {
  width: 80%;
  padding: 20px;
  background-color: var(--card-bg-color);
  color: var(--card-text-color);
  border-radius: 10px;
  box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
  transition: transform 0.3s, box-shadow 0.3s;
}

.card:hover {
  transform: translateY(-5px); /* 悬停时卡片上移 */
  box-shadow: 0 8px 16px rgba(0, 0, 0, 0.2); /* 悬停时阴影加深 */
}

.input-box {
  width: 97%;
  height: 35px;
  padding: 10px;
  font-size: 16px;
  border: 1px solid var(--card-text-color);
  border-radius: 8px;
  background-color: var(--input-bg-color);
  color: var(--input-text-color);
  transition: background-color 0.3s, color 0.3s, border-color 0.3s;
}

.toggle-button-group {
  position: relative;
  display: flex;
  width: 80%; /* 调整为下载按钮的 80% */
  max-width: 400px; /* 限制最大宽度 */
  background-color: var(--input-bg-color);
  border-radius: 8px;
  overflow: hidden;
  height: 40px;
  margin-top: 10px;
  box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1); /* 添加阴影效果 */
}

.toggle-button-group button {
  flex: 1;
  border: none;
  background: none;
  padding: 10px 0;
  font-size: 16px;
  color: var(--card-text-color);
  cursor: pointer;
  z-index: 2;
  transition: background-color 0.3s, color 0.3s;
}

.toggle-button-group button.active {
  font-weight: bold;
}

.toggle-slider {
  position: absolute;
  top: 0;
  bottom: 0;
  width: 50%;
  background-color: var(--button-bg-color);
  transition: left 0.3s;
  z-index: 1;
  border-radius: 8px;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.2); /* 滑块阴影效果 */
}

.download-button {
  padding: 10px 20px;
  font-size: 16px;
  color: var(--button-text-color);
  background-color: var(--button-bg-color); /* 浅紫色 */
  border: 2px solid var(--button-border-color); /* 浅紫色边框 */
  border-radius: 8px;
  cursor: pointer;
  transition: background-color 0.3s, color 0.3s, box-shadow 0.3s, border-color 0.3s;
  margin-top: 10px;
  box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1); /* 阴影效果 */
}

.download-button:hover {
  background-color: var(--button-hover-bg-color); /* 悬停时稍深的紫色 */
  border-color: var(--button-hover-border-color); /* 悬停时稍深的紫色边框 */
  box-shadow: 0 6px 8px rgba(0, 0, 0, 0.2); /* 悬停时阴影加深 */
}

/* 卡片内容布局 */
.card-content {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.card-left {
  flex: 1;
  margin-right: 20px; /* 与右侧进度条的间距 */
}

.card-right {
  flex-shrink: 0;
}

/* 环形进度条样式 */
.el-progress--circle {
  margin-left: 20px; /* 与左侧内容的间距 */
}

/* 卡片描述文字 */
.card-description {
  margin-top: 10px;
  font-size: 14px;
  color: var(--card-text-color);
  opacity: 0.8; /* 降低透明度 */
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
@import url('https://fonts.googleapis.com/css2?family=Pacifico&display=swap');

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