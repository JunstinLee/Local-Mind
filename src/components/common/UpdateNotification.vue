<template>
  <transition name="fade">
    <div v-if="show" class="update-notification fixed top-4 right-4 z-50 max-w-md">
      <el-card class="shadow-lg border-l-4 border-l-blue-500" :body-style="{ padding: '20px' }">
        <!-- 标题和关闭按钮 -->
        <div class="flex justify-between items-start mb-3">
          <div class="flex items-center">
            <el-icon class="text-blue-500 mr-2"><Bell /></el-icon>
            <h3 class="text-lg font-semibold text-gray-800 dark:text-gray-100">
              {{ t('update.title') }}
            </h3>
          </div>
          <button
            @click="closeNotification"
            class="text-gray-400 hover:text-gray-600 dark:hover:text-gray-200 transition-colors"
          >
            <el-icon><Close /></el-icon>
          </button>
        </div>

        <!-- 更新内容 -->
        <div v-if="updateInfo.hasUpdate" class="space-y-3">
          <!-- 版本信息 -->
          <div class="bg-blue-50 dark:bg-blue-900/20 rounded-lg p-3">
            <div class="flex justify-between items-center">
              <div>
                <p class="text-sm text-gray-600 dark:text-gray-300">
                  {{ t('update.currentVersion') }}:
                  <span class="font-medium">{{ currentVersion }}</span>
                </p>
                <p class="text-sm text-green-600 dark:text-green-400 font-medium">
                  {{ t('update.newVersion') }}:
                  <span class="font-semibold">{{ updateInfo.latestVersion }}</span>
                </p>
              </div>
              <el-tag type="success" size="large">
                {{ t('update.available') }}
              </el-tag>
            </div>
          </div>

          <!-- 发布日期 -->
          <div v-if="updateInfo.publishedAt" class="text-xs text-gray-500 dark:text-gray-400">
            {{ t('update.publishedAt') }}: {{ formatDate(updateInfo.publishedAt) }}
          </div>

          <!-- 更新名称 -->
          <div v-if="updateInfo.name" class="text-sm font-medium text-gray-700 dark:text-gray-300">
            {{ updateInfo.name }}
          </div>

          <!-- 更新说明 -->
          <div
            v-if="updateInfo.notes"
            class="bg-gray-50 dark:bg-gray-800/50 rounded-lg p-3 max-h-40 overflow-y-auto"
          >
            <h4 class="text-sm font-medium text-gray-700 dark:text-gray-300 mb-2">
              {{ t('update.releaseNotes') }}
            </h4>
            <div class="prose prose-sm max-w-none text-gray-600 dark:text-gray-400">
              <div v-html="formatReleaseNotes(updateInfo.notes)"></div>
            </div>
          </div>

          <!-- 操作按钮 -->
          <div class="flex gap-2 pt-2">
            <el-button type="primary" size="small" @click="goToUpdatePage" :icon="Download">
              {{ t('update.download') }}
            </el-button>
            <el-button size="small" @click="closeNotification">
              {{ t('update.close') }}
            </el-button>
          </div>
        </div>

        <!-- 无更新 -->
        <div v-else class="text-center py-4">
          <el-icon class="text-green-500 text-2xl mb-2"><Check /></el-icon>
          <p class="text-gray-600 dark:text-gray-400">
            {{ t('update.latest') }}
          </p>
          <el-button size="small" @click="checkUpdates" :loading="checking" class="mt-2">
            {{ t('update.checkAgain') }}
          </el-button>
        </div>
      </el-card>
    </div>
  </transition>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import { useI18n } from 'vue-i18n'
import { Bell, Close, Download, Check } from '@element-plus/icons-vue'
import { ElMessage } from 'element-plus'
import { marked } from 'marked'
import DOMPurify from 'dompurify'

// Props
const props = defineProps({
  // 当前版本号
  currentVersion: {
    type: String,
    default: '1.0.0',
  },
  // 自动检查更新的间隔时间（毫秒），0表示不自动检查
  autoCheckInterval: {
    type: Number,
    default: 0,
  },
  // 是否显示组件
  visible: {
    type: Boolean,
    default: false,
  },
})

// Emits
const emit = defineEmits(['update:visible', 'update-checked'])

// i18n
const { t } = useI18n()

// 响应式状态
const show = ref(props.visible)
const updateInfo = ref({
  hasUpdate: false,
  latestVersion: '',
  url: '',
  notes: '',
  name: '',
  publishedAt: null,
})
const checking = ref(false)

// 计算属性
const formattedUpdateInfo = computed(() => {
  return {
    ...updateInfo.value,
    currentVersion: props.currentVersion,
  }
})

// 方法
/**
 * 检查更新
 */
const checkUpdates = async () => {
  try {
    checking.value = true
    const { checkForUpdate } = await import('@/services/updateService')
    const result = await checkForUpdate()
    updateInfo.value = result
    emit('update-checked', result)

    // 如果有更新，显示通知
    if (result.hasUpdate) {
      show.value = true
    }
  } catch (error) {
    console.error('检查更新失败:', error)
    ElMessage.error({
      message: t('update.error'),
      duration: 5000,
    })
  } finally {
    checking.value = false
  }
}

/**
 * 关闭通知
 */
const closeNotification = () => {
  show.value = false
  emit('update:visible', false)
}

/**
 * 跳转到更新页面
 */
const goToUpdatePage = () => {
  if (updateInfo.value.url) {
    window.open(updateInfo.value.url, '_blank')
  }
}

/**
 * 格式化发布日期
 */
const formatDate = (dateString) => {
  try {
    return new Date(dateString).toLocaleDateString(undefined, {
      year: 'numeric',
      month: 'long',
      day: 'numeric',
      hour: '2-digit',
      minute: '2-digit',
    })
  } catch {
    return dateString
  }
}

/**
 * 格式化更新说明
 */
const formatReleaseNotes = (notes) => {
  if (!notes) return ''

  // 使用marked解析Markdown
  const html = marked.parse(notes)

  // 使用DOMPurify清理XSS
  return DOMPurify.sanitize(html)
}

// 生命周期钩子
onMounted(() => {
  // 如果设置为可见，立即显示
  if (props.visible) {
    show.value = true
  }

  // 如果设置了自动检查间隔，启动定时检查
  if (props.autoCheckInterval > 0) {
    // 首次加载时立即检查一次
    checkUpdates()

    // 设置定时检查
    const intervalId = setInterval(checkUpdates, props.autoCheckInterval)

    // 组件卸载时清除定时器
    onUnmounted(() => {
      clearInterval(intervalId)
    })
  }
})

// 监听props变化
watch(
  () => props.visible,
  (newValue) => {
    show.value = newValue
  },
)

watch(
  () => props.currentVersion,
  () => {
    // 版本号变化时重新检查更新
    if (props.autoCheckInterval > 0) {
      checkUpdates()
    }
  },
  { immediate: false },
)
</script>

<style scoped>
.update-notification {
  animation: slideIn 0.3s ease-out;
}

/* 自定义滚动条 */
.update-notification ::-webkit-scrollbar {
  width: 6px;
}

.update-notification ::-webkit-scrollbar-track {
  background: rgba(0, 0, 0, 0.1);
  border-radius: 3px;
}

.update-notification ::-webkit-scrollbar-thumb {
  background: rgba(0, 0, 0, 0.2);
  border-radius: 3px;
}

.update-notification ::-webkit-scrollbar-thumb:hover {
  background: rgba(0, 0, 0, 0.3);
}

/* 动画 */
@keyframes slideIn {
  from {
    transform: translateX(100%);
    opacity: 0;
  }
  to {
    transform: translateX(0);
    opacity: 1;
  }
}

.fade-enter-active,
.fade-leave-active {
  transition: all 0.3s ease;
}

.fade-enter-from,
.fade-leave-to {
  transform: translateX(100%);
  opacity: 0;
}
</style>
