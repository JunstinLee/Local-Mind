<template>
  <!-- 只有当 showModal 为 true 时才渲染遮罩，起到阻断作用 -->
  <div v-if="showModal" class="modal-overlay">
    <div class="modal-content">
      <!-- 关闭按钮 -->
      <button class="close-button" @click="handleClose" title="关闭">
        <X :size="20" />
      </button>
      
      <div class="modal-header">
        <img src="/logo.png" alt="Logo" class="logo-image" />
        <h3 class="modal-title">正在检查嵌入模型...</h3>
      </div>
      
      <div class="modal-body">
        <!-- 状态项：模型 -->
        <div class="status-item">
          <i 
            :class="status.model_loaded ? 'el-icon-circle-check filled' : 'el-icon-loading rotating'" 
            class="status-icon"
          ></i>
          <span>嵌入模型: {{ status.model_loaded ? '已就绪' : '加载中...' }}</span>
        </div>
        
        <!-- 进度条 - 不确定模式，6秒后消失 -->
        <el-progress 
          v-if="!isReady && showProgressBar" 
          :percentage="100" 
          status="warning"
          :indeterminate="true"
          :duration="3"
          class="progress-bar"
        />
      </div>
      
      <div class="modal-footer">
        <p class="hint-text">首次加载可能需要较长时间，请耐心等待。</p>
        <p class="settings-hint">
          <i class="el-icon-warning"></i>
          如果长时间未加载，请前往 <strong>设置界面</strong> 下载并配置嵌入模型。
        </p>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted, onUnmounted, computed } from 'vue'
import { getStatus } from '@/api/status'
import { X } from 'lucide-vue-next'

const emit = defineEmits(['ready', 'close'])

const showModal = ref(false)
const showProgressBar = ref(true)
const status = ref({
  model_loaded: false
})

let checkInterval = null
let progressBarTimer = null

const isReady = computed(() => {
  return status.value.model_loaded
})

const checkStatus = async () => {
  try {
    const res = await getStatus()
    status.value = res
    
    if (res.model_loaded) {
      // 已就绪
      if (showModal.value) {
        // 如果之前是打开的，稍微延迟关闭以展示已就绪状态（可选）
        setTimeout(() => {
          showModal.value = false
          emit('ready')
        }, 500)
      } else {
        // 如果从未打开过弹窗，直接触发 ready
        emit('ready')
      }
      stopPolling()
    } else {
      // 未就绪，强制显示弹窗
      showModal.value = true
    }
  } catch (e) {
    console.error("Status check failed", e)
    // 发生错误时也显示弹窗，继续轮询
    showModal.value = true
  }
}

const startPolling = () => {
  // 立即检查一次
  checkStatus()
  // 开启轮询
  if (!checkInterval) {
    checkInterval = setInterval(checkStatus, 2000)
  }
}

const stopPolling = () => {
  if (checkInterval) {
    clearInterval(checkInterval)
    checkInterval = null
  }
}

// 关闭弹窗
const handleClose = () => {
  showModal.value = false
  stopPolling()
  if (progressBarTimer) {
    clearTimeout(progressBarTimer)
    progressBarTimer = null
  }
  emit('close')
}

// 6秒后隐藏进度条
const startProgressBarTimer = () => {
  if (progressBarTimer) {
    clearTimeout(progressBarTimer)
  }
  progressBarTimer = setTimeout(() => {
    showProgressBar.value = false
  }, 6000)
}

onMounted(() => {
  startPolling()
  startProgressBarTimer()
})

onUnmounted(() => {
  stopPolling()
  if (progressBarTimer) {
    clearTimeout(progressBarTimer)
    progressBarTimer = null
  }
})
</script>

<style scoped>
/* 复用 LoadingProgressModal.vue 的样式 */
.modal-overlay {
  position: fixed;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background-color: rgba(0, 0, 0, 0.5);
  display: flex;
  justify-content: center;
  align-items: center;
  z-index: 9999;
}

.modal-content {
  background: white;
  background-color: white;
  border-radius: 8px;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.15);
  width: 500px;
  max-width: 90vw;
  padding: 20px;
  text-align: center;
  position: relative; /* 添加相对定位，使关闭按钮能够相对于弹窗定位 */
}

html.dark .modal-content {
  background-color: #27272a;
}

.modal-header {
  margin-bottom: 20px;
  display: flex;
  flex-direction: column;
  align-items: center;
}

.modal-title {
  display: block;
  font-size: 1rem;
  color: #333;
}

html.dark .modal-title {
  color: #e5e5e5;
}

.status-item {
  display: flex;
  align-items: center;
  justify-content: flex-start;
  margin: 15px 0;
  padding: 8px;
  text-align: left;
}

.status-icon {
  margin-right: 10px;
  font-size: 1.2rem;
}

.status-icon.filled {
  color: #67c23a;
}

.status-icon.rotating {
  animation: rotate 2s linear infinite;
}

@keyframes rotate {
  from {
    transform: rotate(0deg);
  }
  to {
    transform: rotate(360deg);
  }
}

.progress-bar {
  margin: 20px 0;
}

.logo-image {
  width: 80px;
  height: 80px;
  display: block;
  margin: 0 auto 15px auto;
}

.modal-footer {
  margin-top: 20px;
}

.hint-text {
  font-size: 0.9rem;
  color: #666;
}

html.dark .hint-text {
  color: #999;
}

.settings-hint {
  font-size: 0.9rem;
  color: #e6a23c;
  margin-top: 10px;
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 5px;
}

html.dark .settings-hint {
  color: #f0ad4e;
}

.settings-hint strong {
  color: #409eff;
  cursor: pointer;
}

html.dark .settings-hint strong {
  color: #66b1ff;
}

.close-button {
  position: absolute;
  top: 10px;
  right: 10px;
  background: transparent;
  border: none;
  width: 32px;
  height: 32px;
  font-size: 1.5rem;
  color: var(--el-text-color-primary);
  cursor: pointer;
  padding: 0;
  display: flex;
  align-items: center;
  justify-content: center;
  transition: opacity 0.3s;
  z-index: 10;
}

.close-button:hover {
  opacity: 0.6;
}
</style>
