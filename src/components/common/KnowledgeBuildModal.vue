<template>
  <div>
    <!-- 弹窗遮罩 -->
    <div
      v-show="isModalOpen"
      class="tw-fixed tw-inset-0 tw-bg-black tw-bg-opacity-70 tw-backdrop-blur-sm tw-flex tw-items-center tw-justify-center tw-transition-all tw-duration-300"
      style="z-index: 9999"
      @click="handleOverlayClick"
    >
      <div
        class="tw-bg-[var(--el-bg-color)] tw-rounded-2xl tw-p-8 tw-w-full tw-max-w-3xl tw-relative tw-transform tw-transition-all tw-duration-300 tw-shadow-2xl tw-flex tw-flex-col"
        :class="isModalOpen ? 'tw-scale-100 tw-translate-y-0' : 'tw-scale-75 tw-translate-y-12'"
        style="max-height: 90vh"
      >
        <!-- 关闭按钮 -->
        <button
          class="tw-absolute tw-top-5 tw-right-5 tw-bg-transparent tw-border-none tw-text-2xl tw-text-gray-400 dark:tw-text-gray-500 tw-cursor-pointer tw-w-10 tw-h-10 tw-rounded-full tw-flex tw-items-center tw-justify-center tw-transition-all tw-duration-300 hover:tw-bg-gray-100 dark:hover:tw-bg-gray-700 hover:tw-text-gray-600 dark:hover:tw-text-gray-300 hover:tw-rotate-90"
          @click="closeModal"
        >
          ×
        </button>

        <!-- 弹窗头部 -->
        <div class="tw-text-center tw-mb-4 tw-flex-shrink-0">
          <h2 class="tw-text-3xl tw-text-gray-800 dark:tw-text-gray-100 tw-font-bold">
            {{ t('knowledgeBase.buildTitle') }}
          </h2>
        </div>

        <!-- 总体进度 (处理中或完成后显示) -->
        <transition name="slide-fade tw-bg-gray-200 dark:tw-bg-gray-700">
          <div v-if="isProcessing || isFinished" class="tw-mb-4 tw-flex-shrink-0">
            <div class="tw-flex tw-justify-between tw-items-center tw-mb-2">
              <p class="tw-text-sm tw-text-gray-600 dark:tw-text-gray-300">
                {{ t('knowledgeBase.overallProgress') }} : {{ Math.round(overallProgress) }}%
              </p>
              <p v-if="isProcessing && formattedRemainingTime" class="tw-text-xs tw-text-blue-600 dark:tw-text-blue-400 tw-font-medium">
                {{ t('knowledgeBase.estimatedTime') }}: {{ formattedRemainingTime }}
              </p>
            </div>
            <div class="tw-w-full tw-rounded-full tw-h-2.5">
              <div
                class="tw-bg-blue-600 tw-h-2.5 tw-rounded-full tw-transition-all tw-duration-500"
                :style="{ width: `${overallProgress}%` }"
              ></div>
            </div>
          </div>
        </transition>

        <!-- 文件处理内容: 容器高度限制为约6个项目 -->
        <div
          class="custom-scrollbar tw-flex-grow tw-overflow-y-auto tw-pr-2 tw-space-y-2 tw-text-gray-200 dark:tw-text-gray-700"
          style="max-height: 450px"
        >
          <!-- 新增：加载状态 -->
          <div v-if="isLoadingFiles" class="tw-text-center tw-py-10">
            <span class="tw-text-gray-400">{{ t('knowledgeBase.loadingFileList') }} ...</span>
          </div>

          <!-- 文件列表 (用 v-else-if 包裹) -->
          <div v-else-if="files.length > 0">
            <div
              v-for="file in files"
              :key="file.id"
              class="tw-rounded-lg tw-p-3 tw-shadow-sm tw-border tw-transition-all tw-duration-300"
              :class="
                (isProcessing || isFinished)
                  ? getStatusInfo(file.status).borderClass
                  : 'tw-text-gray-200 dark:tw-text-gray-700'
              "
            >
              <div class="tw-flex tw-items-center tw-gap-3">
                <!-- 1. 左侧图标区域 -->
                <div
                  class="tw-relative tw-w-6 tw-h-6 tw-flex tw-items-center tw-justify-center tw-flex-shrink-0"
                >
                  <!-- 处理前：通用图标 -->
                  <transition name="fade">
                    <component
                      v-if="!isProcessing && !isFinished"
                      :is="FileText"
                      class="tw-w-5 tw-h-5 tw-text-gray-400 dark:tw-text-gray-500"
                    />
                  </transition>
                  <!-- 处理后：状态图标 -->
                  <transition name="fade">
                    <component
                      v-if="isProcessing || isFinished"
                      :is="getStatusInfo(file.status).icon"
                      class="tw-w-5 tw-h-5 tw-absolute"
                      :class="[
                        { 'processing-icon': file.status === 'processing' },
                        getStatusInfo(file.status).colorClass
                      ]"
                    />
                  </transition>
                </div>

                <!-- 2. 右侧信息区域 -->
                <div class="tw-flex-grow tw-min-w-0">
                  <!-- 文件名和状态文本行 -->
                  <div
                    class="tw-flex tw-justify-between tw-items-baseline tw-text-gray-700 dark:tw-text-white"
                  >
                    <span class="tw-font-medium 0 tw-truncate" :title="file.name">{{
                      file.name
                    }}</span>
                    <transition name="fade ">
                      <span
                        v-if="isProcessing || isFinished"
                        class="tw-text-xs tw-font-semibold tw-flex-shrink-0 tw-ml-2"
                        :class="getStatusInfo(file.status).colorClass"
                        >{{ getStatusInfo(file.status).text }}</span
                      >
                    </transition>
                  </div>

                  <!-- 详细信息和进度条的容器 -->
                  <transition name="slide-fade ">
                    <div v-if="isProcessing || isFinished" class="tw-mt-1">
                      <!-- 详细消息 -->
                      <p
                        class="tw-text-xs tw-truncate"
                        :class="
                          file.status === 'error'
                            ? 'tw-text-red-500'
                            : 'tw-text-gray-500 dark:tw-text-gray-400'
                        "
                      >
                        {{ file.message }}
                      </p>
                      <!-- 进度条 -->
                      <div
                        v-if="file.status === 'processing' || file.status === 'error'"
                        class="tw-mt-2 tw-w-full tw-rounded-full tw-h-1.5"
                      >
                        <div
                          class="tw-h-1.5 tw-rounded-full tw-transition-all tw-duration-500"
                          :class="getStatusInfo(file.status).progressClass"
                          :style="{ width: `${file.progress}%` }"
                        ></div>
                      </div>
                    </div>
                  </transition>
                </div>
              </div>
            </div>
          </div>

          <!-- 新增：空状态 -->
          <div v-else class="tw-text-center tw-py-10">
            <span class="tw-text-gray-400"
              >{{ t('knowledgeBase.noFilesAvailable') }}
            </span>
          </div>
        </div>

        <!-- 底部区域 -->
        <div
          class="tw-flex-shrink-0 tw-pt-4 tw-mt-4 tw-border-t tw-border-gray-200 dark:tw-border-gray-700"
        >
          <!-- 统计信息 (处理中或完成后显示) -->
          <transition name="fade">
            <div v-if="isProcessing || isFinished" class="tw-flex tw-justify-center tw-space-x-4 sm:tw-space-x-6 tw-mb-6">
              <div class="tw-text-center">
                <div class="tw-text-lg tw-font-semibold tw-text-green-600 dark:tw-text-green-400">
                  {{ completedCount }}
                </div>
                <div class="tw-text-xs tw-text-gray-500 dark:tw-text-gray-400">{{ t('status.completed') }}</div>
              </div>
              <div class="tw-text-center">
                <div class="tw-text-lg tw-font-semibold tw-text-blue-600 dark:tw-text-blue-400">
                  {{ processingCount }}
                </div>
                <div class="tw-text-xs tw-text-gray-500 dark:tw-text-gray-400">{{ t('status.inProgress') }}</div>
              </div>
              <div class="tw-text-center">
                <div class="tw-text-lg tw-font-semibold tw-text-red-600 dark:tw-text-red-400">
                  {{ failedCount }}
                </div>
                <div class="tw-text-xs tw-text-gray-500 dark:tw-text-gray-400">{{ t('status.failed') }}</div>
              </div>
              <div class="tw-text-center">
                <div class="tw-text-lg tw-font-semibold tw-text-yellow-600 dark:tw-text-yellow-400">
                  {{ emptyFileCount }}
                </div>
                <div class="tw-text-xs tw-text-gray-500 dark:tw-text-gray-400">{{ t('status.emptyFile') }}</div>
              </div>
              <div class="tw-text-center">
                <div class="tw-text-lg tw-font-semibold tw-text-gray-600 dark:tw-text-gray-400">
                  {{ waitingCount }}
                </div>
                <div class="tw-text-xs tw-text-gray-500 dark:tw-text-gray-400">{{ t('status.pending') }}</div>
              </div>
            </div>
          </transition>

          <!-- 开始按钮 (仅在未开始且未完成时显示) -->
          <div v-if="!isProcessing && !isFinished && files.length > 0" class="tw-text-center">
            <el-button 
              type="primary" 
              @click="startProcessing()" 
              :loading="isStarting" 
              size="large"
            >
              {{ t('knowledgeBase.startBuild', { count: files.length }) }}
            </el-button>
          </div>
          
           <!-- 完成后的关闭按钮 (仅在完成后显示，替代原来的逻辑以实现位置分离) -->
           <div v-if="isFinished" class="tw-text-center">
            <el-button 
              type="success" 
              @click="closeModal()" 
              size="large"
            >
              {{ t('knowledgeBase.buildCompleted') }}
            </el-button>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onUnmounted, watch } from 'vue'
import { useFileStore } from '@/stores/modules/filestore'
import { useKnowledgeBaseBuilder } from '@/services/BuildBase.js'
import { loadUnvectorizedFileList } from '@/services/check'
import { tr } from 'element-plus/es/locales.mjs'
import { useI18n } from 'vue-i18n'
import { 
  FileText, 
  Check, 
  Loader2, 
  X, 
  TriangleAlert, 
  Clock 
} from 'lucide-vue-next'

// --- i18n ---
const { t } = useI18n()

// --- Props ---
const props = defineProps({
  // 用于从外部接收文件列表
  filesToProcess: {
    type: Array,
    default: () => [],
  },
})

// --- State Refs ---
const isModalOpen = ref(false)
const isLoadingFiles = ref(false)
const files = ref([]) // 持有每个文件状态的内部数组

// --- 集成构建服务 ---
// 从服务中获取所有状态和控制方法
const buildService = useKnowledgeBaseBuilder(files)
const {
  isProcessing,
  isFinished, // 新增：是否完成状态
  isStarting,
  overallProgress, // 使用服务提供的响应式总进度
  formattedRemainingTime,
  startBuildProcess: serviceStartBuildProcess, // 重命名以避免冲突
  resetState
} = buildService

// startProcessing 现在直接调用服务提供的函数
const startProcessing = async () => {
  await serviceStartBuildProcess()
  // 知识库构建完成后，我们需要等待处理完成才刷新数据
  // 由于 service 内部维护了 isProcessing 状态，我们可以监听该状态的变化来决定何时刷新
  // 或者简单地依赖用户关闭弹窗时的刷新（如果 resetState 不会自动刷新，可以在 watch isProcessing 中处理）
}

// 监听处理状态，当处理从 true 变为 false 时（且不是因为取消），刷新列表
const fileStore = useFileStore()

watch(isProcessing, (newValue, oldValue) => {
    if (oldValue === true && newValue === false) {
        // 处理完成
        fileStore.markNeedsRefresh()
    }
})

// --- Computed Properties for Statistics (UI统计部分保持不变) ---
const completedCount = computed(() => files.value.filter((f) => f.status === 'completed').length)
const processingCount = computed(() => files.value.filter((f) => f.status === 'processing').length)
const waitingCount = computed(() => files.value.filter((f) => f.status === 'waiting').length)
const failedCount = computed(() => files.value.filter((f) => f.status === 'error').length)
const emptyFileCount = computed(() => files.value.filter((f) => f.status === 'empty_file').length)

// --- UI Helpers (样式函数保持不变) ---
const getStatusInfo = (status) => {
  switch (status) {
    case 'completed':
      return {
        icon: Check,
        text: t('status.completed'),
        colorClass: 'tw-text-green-600 dark:tw-text-green-400',
        progressClass: 'tw-bg-green-500 dark:tw-bg-green-600',
        borderClass: 'tw-border-green-200 dark:tw-border-green-700',
      }
    case 'processing':
      return {
        icon: Loader2,
        text: t('status.inProgress'),
        colorClass: 'tw-text-blue-600 dark:tw-text-blue-400',
        progressClass: 'tw-bg-blue-500 dark:tw-bg-blue-600',
        borderClass: 'tw-border-blue-200 dark:tw-border-blue-700',
      }
    case 'error':
      return {
        icon: X,
        text: t('status.failed'),
        colorClass: 'tw-text-red-600 dark:tw-text-red-400',
        progressClass: 'tw-bg-red-500 dark:tw-bg-red-600',
        borderClass: 'tw-border-red-300 dark:tw-border-red-700',
      }
    case 'empty_file': // 新增空文件状态
      return {
        icon: TriangleAlert,
        text: t('status.emptyFile'),
        colorClass: 'tw-text-yellow-600 dark:tw-text-yellow-400',
        progressClass: 'tw-bg-yellow-500 dark:tw-bg-yellow-600',
        borderClass: 'tw-border-yellow-300 dark:tw-border-yellow-600',
      }
    default: // waiting
      return {
        icon: Clock,
        text: t('status.pending'),
        colorClass: 'tw-text-gray-600 dark:tw-text-gray-400',
        progressClass: 'tw-bg-gray-400 dark:tw-bg-gray-500',
        borderClass: 'tw-border-gray-200 dark:tw-border-gray-700',
      }
  }
}

// --- Modal Control (集成新服务的控制方法) ---
const openModal = async () => {
  isModalOpen.value = true
  document.body.style.overflow = 'hidden'
  resetState()

  isLoadingFiles.value = true
  files.value = []
  try {
    const response = await loadUnvectorizedFileList({
      basePath: '.',
      filters: {},
      sortBy: 'name',
      sortOrder: 'asc',
      timestamp: Date.now(),
    })
    if (response.data && response.data.files) {
      files.value = response.data.files.map((file) => ({
        id: file.path,
        name: file.name,
        path: file.path,
        size: file.size,
        modified_date: file.modified_date,
        status: 'waiting',
        progress: 0,
        message: t('status.pending'),
      }))
    } else {
      files.value = []
    }
  } catch (error) {
    console.error('Failed to load unvectorized files for knowledge build:', error)
    files.value = []
  } finally {
    isLoadingFiles.value = false
  }
}

const closeModal = () => {
  isModalOpen.value = false
  document.body.style.overflow = 'auto'
  resetState() // 关闭时也重置状态，停止任何可能的动画
}

const handleOverlayClick = (event) => {
  if (event.target === event.currentTarget) {
    closeModal()
  }
}

onUnmounted(() => {
  // 组件销毁时确保重置
  resetState()
})

// --- Expose to Parent ---
defineExpose({ openModal })
</script>

<style>
/* 非scoped样式，用于全局修改滚动条和定义动画 */

/* --- Custom Scrollbar --- */
.custom-scrollbar::-webkit-scrollbar {
  width: 8px;
  height: 8px;
}
.custom-scrollbar::-webkit-scrollbar-track {
  background-color: rgba(0, 0, 0, 0.05);
  border-radius: 10px;
}
.dark .custom-scrollbar::-webkit-scrollbar-track {
  background-color: rgba(255, 255, 255, 0.05);
}
.custom-scrollbar::-webkit-scrollbar-thumb {
  background-color: rgba(0, 0, 0, 0.2);
  border-radius: 10px;
  border: 2px solid transparent;
  background-clip: content-box;
}
.dark .custom-scrollbar::-webkit-scrollbar-thumb {
  background-color: rgba(255, 255, 255, 0.2);
}
.custom-scrollbar::-webkit-scrollbar-thumb:hover {
  background-color: rgba(0, 0, 0, 0.3);
}
.dark .custom-scrollbar::-webkit-scrollbar-thumb:hover {
  background-color: rgba(255, 255, 255, 0.3);
}

/* --- Animations --- */
@keyframes spin {
  from {
    transform: rotate(0deg);
  }
  to {
    transform: rotate(360deg);
  }
}
.processing-icon {
  animation: spin 1.5s linear infinite;
}

/* --- Vue Transitions --- */
.fade-enter-active,
.fade-leave-active {
  transition: opacity 0.3s ease;
}
.fade-enter-from,
.fade-leave-to {
  opacity: 0;
}

.slide-fade-enter-active {
  transition: all 0.3s ease-out;
}
.slide-fade-leave-active {
  transition: all 0.2s cubic-bezier(1, 0.5, 0.8, 1);
}
.slide-fade-enter-from,
.slide-fade-leave-to {
  transform: translateY(-10px);
  opacity: 0;
}
</style>
