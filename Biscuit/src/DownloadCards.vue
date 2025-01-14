<template>
  <!-- 下载器卡片布局 -->
  <div class="cards">
    <!-- 输入链接卡片 -->
    <div class="card">
      <h3>Enter Download Link</h3>
      <input v-model="downloadLink" placeholder="Enter download link" class="input-box" />
      <p class="card-description">Paste your download link above to get started.</p>
    </div>

    <!-- 下载方式和按钮卡片 -->
    <div class="card">
      <div class="card-content">
        <div class="card-left">
          <h3>Choose Download Method</h3>
          <div class="toggle-button-group">
            <button
              :class="{ active: downloadMethod === 'left' }"
              @click="downloadMethod = 'left'"
            >
              下载单曲
            </button>
            <button
              :class="{ active: downloadMethod === 'right' }"
              @click="downloadMethod = 'right'"
            >
              下载用户全部歌曲
            </button>
            <span
              class="toggle-slider"
              :style="{ left: downloadMethod === 'left' ? '0%' : '50%' }"
            ></span>
          </div>

          <!-- 下载按钮 -->
          <button
            @click="handleDownload"
            class="download-button"
            :disabled="isDownloading"
          >
            <span class="icon">⬇️</span>
            {{ isDownloading ? "Downloading..." : "Download" }}
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
</template>

<script setup lang="ts">
import { ref } from "vue";
import { ElMessage } from "element-plus";
import { invoke } from "@tauri-apps/api/core";
import { listen } from "@tauri-apps/api/event";
// 下载链接和方式
const downloadLink = ref("");
const downloadMethod = ref("left");

const total_count = ref(1);
// 下载进度
const downloadProgress = ref(0); // 进度值（0-100）
const isDownloading = ref(false); // 是否正在下载

// 处理下载逻辑
async function handleDownload() {
  if (!downloadLink.value) {
    ElMessage.error("Please enter a download link."); // 提示用户输入下载链接
    return;
  }

  downloadProgress.value = 0; // 重置进度

  try {
    // 根据下载方式调用不同的后端函数
    if (downloadMethod.value === "left") {
      await download_single_song(downloadLink.value); // 调用下载单曲函数
    } else {
      await download_all_songs(downloadLink.value); // 调用下载全部歌曲函数
    }
  } catch (error) {
    console.error("Download failed:", error);
    ElMessage.error("Download failed. Please try again."); // 下载失败提示
  } finally {
    isDownloading.value = false; // 结束下载状态
  }
}

async function download_single_song(link: string, cookie?: string) {
  try {
    // 调用后端 API 下载单曲
    await invoke("download_single_song", { url: link, cookie: cookie });
  } catch (error) {
    console.error("Error downloading song:", error);
  }
}

async function download_all_songs(link: string, cookie?: string) {
  try {
    // 调用后端 API 下载全部歌曲
    await invoke("download_all_songs", { url: link, cookie: cookie });
  } catch (error) {
    console.error("Error downloading songs:", error);
    // 这里可以显示错误提示
  }
}

// 监听后端发送的事件
listen("download-started", () => {
  ElMessage.success("Download start!"); // 下载完成提示
  isDownloading.value = true;
});
listen("download_success", () => {
  ElMessage.success("Download complete!"); // 下载完成提示
  isDownloading.value = false;
});
listen("download_index", (event: { payload: number }) => {
  downloadProgress.value = Math.round((event.payload / total_count.value) * 100);
});

listen("total_count", (event: { payload: number }) => {
  console.log(`Total songs to download: ${event.payload}`);
  total_count.value = event.payload;
});
</script>

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
</style>
