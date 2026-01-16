<template>
  <div v-if="showModal" class="modal-overlay">
    <div class="modal-content">
      <div class="modal-header">
        <img src="/logo.png" alt="Logo" class="logo-image" />
        <h2 class="modal-title">{{ t('common.loadingDetail.title') }}</h2>
      </div>
      <div class="modal-body">
        <div class="status-item">
          <i
            :class="
              status.model_loaded ? 'el-icon-circle-check filled' : 'el-icon-loading rotating'
            "
            class="status-icon"
          ></i>
          <span
            >{{ t('common.loadingDetail.model_loaded') }}:
            {{
              status.model_loaded
                ? t('common.loadingDetail.completed')
                : t('common.loadingDetail.loading')
            }}</span
          >
        </div>
        <div class="status-item">
          <i
            :class="
              status.chroma_db_initialized
                ? 'el-icon-circle-check filled'
                : 'el-icon-loading rotating'
            "
            class="status-icon"
          ></i>
          <span
            >{{ t('common.loadingDetail.chroma_db_initialized') }}:
            {{
              status.chroma_db_initialized
                ? t('common.loadingDetail.completed')
                : t('common.loadingDetail.initializing')
            }}</span
          >
        </div>
        <div class="status-item">
          <i
            :class="
              status.search_service_initialized
                ? 'el-icon-circle-check filled'
                : 'el-icon-loading rotating'
            "
            class="status-icon"
          ></i>
          <span
            >{{ t('common.loadingDetail.search_service_initialized') }}:
            {{
              status.search_service_initialized
                ? t('common.loadingDetail.completed')
                : t('common.loadingDetail.initializing')
            }}</span
          >
        </div>

        <!-- 进度条 -->
        <el-progress
          :percentage="calculateProgress()"
          :status="status.status === 'ready' ? 'success' : ''"
          :stroke-width="20"
          class="progress-bar"
        />
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted, onUnmounted, watch } from 'vue'
import { ElProgress } from 'element-plus'
import { getStatus } from '@/api/status'
import { useI18n } from 'vue-i18n' // 引入 useI18n

const { t } = useI18n() // 使用 useI18n

// 定义 props
const props = defineProps({
  modelValue: {
    type: Boolean,
    default: false,
  },
})

// 定义 emits
const emit = defineEmits(['update:modelValue', 'backendReady'])

// 响应式数据
const showModal = ref(props.modelValue)
const status = ref({
  model_loaded: false,
  chroma_db_initialized: false,
  search_service_initialized: false,
  status: 'loading', // 'loading', 'ready', 'error'
})

// 检查间隔ID和超时ID
let checkInterval = null
let timeoutId = null

// 计算进度
const calculateProgress = () => {
  const totalSteps = 3
  let completedSteps = 0

  if (status.value.model_loaded) completedSteps++
  if (status.value.chroma_db_initialized) completedSteps++
  if (status.value.search_service_initialized) completedSteps++

  return Math.round((completedSteps / totalSteps) * 100)
}

// 获取后端状态
const fetchBackendStatus = async () => {
  try {
    const result = await getStatus()
    status.value = result

    // 如果后端已准备好，停止检查并发出事件
    if (result.status === 'ready') {
      clearInterval(checkInterval)
      clearTimeout(timeoutId) // 清除超时定时器
      emit('backendReady')
    }
  } catch (error) {
    console.error('获取后端状态失败:', error)
    // 保持弹窗显示，继续尝试获取状态
  }
}

// 关闭弹窗
const closeModal = () => {
  showModal.value = false
  emit('update:modelValue', false)
  if (checkInterval) {
    clearInterval(checkInterval)
  }
  if (timeoutId) {
    clearTimeout(timeoutId)
  }
}

// 监听 props 变化
watch(
  () => props.modelValue,
  (newValue) => {
    showModal.value = newValue
    if (newValue) {
      // 开始定期检查后端状态
      checkInterval = setInterval(fetchBackendStatus, 1000)
      // 设置超时，无论状态如何都会关闭弹窗（例如30秒后）
      timeoutId = setTimeout(() => {
        clearInterval(checkInterval)
        closeModal()
      }, 3000) // 3秒后自动关闭
      // 立即获取一次状态
      fetchBackendStatus()
    } else {
      // 关闭定时器
      if (checkInterval) {
        clearInterval(checkInterval)
      }
      if (timeoutId) {
        clearTimeout(timeoutId)
      }
    }
  },
)

// 组件挂载时开始检查
onMounted(() => {
  if (showModal.value) {
    checkInterval = setInterval(fetchBackendStatus, 1000)
    // 设置超时，无论状态如何都会关闭弹窗（例如30秒后）
    timeoutId = setTimeout(() => {
      clearInterval(checkInterval)
      closeModal()
    }, 3000) // 3秒后自动关闭
    fetchBackendStatus()
  }
})

// 组件卸载时清理
onUnmounted(() => {
  if (checkInterval) {
    clearInterval(checkInterval)
  }
  if (timeoutId) {
    clearTimeout(timeoutId)
  }
})
</script>

<style scoped>
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

.icon-large {
  font-size: 2rem;
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
</style>
