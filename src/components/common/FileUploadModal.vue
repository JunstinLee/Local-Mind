<template>
  <div>
    <!-- 弹窗遮罩 -->
    <div
      v-show="isModalOpen"
      class="tw-fixed tw-inset-0 tw-backdrop-blur-sm tw-flex tw-items-center tw-justify-center tw-transition-all tw-duration-300"
      style="z-index: 9999"
      @click="handleOverlayClick"
    >
      <div
        class="tw-bg-[var(--el-bg-color)] tw-rounded-2xl tw-p-10 tw-w-full tw-max-w-lg tw-relative tw-transform tw-transition-all tw-duration-300 tw-shadow-2xl"
        :class="isModalOpen ? 'tw-scale-100 tw-translate-y-0' : 'tw-scale-75 tw-translate-y-12'"
      >
        <!-- 关闭按钮 -->
        <button
          class="tw-absolute tw-top-5 tw-right-5 tw-bg-transparent tw-border-none tw-text-2xl tw-text-gray-400 dark:tw-text-gray-500 tw-cursor-pointer tw-w-10 tw-h-10 tw-rounded-full tw-flex tw-items-center tw-justify-center tw-transition-all tw-duration-300 hover:tw-bg-gray-100 dark:hover:tw-bg-gray-700 hover:tw-text-gray-600 dark:hover:tw-text-gray-300 hover:tw-rotate-90"
          @click="closeModal"
        >
          ×
        </button>

        <!-- 弹窗头部 -->
        <div class="tw-text-center tw-mb-8">
          <h2 class="tw-text-3xl tw-text-gray-800 dark:tw-text-gray-100 tw-mb-3 tw-font-bold">
            {{ t('upload.title') }}
          </h2>
          <p class="tw-text-gray-600 dark:tw-text-gray-400 tw-text-base"></p>
        </div>

        <!-- 上传区域 -->
        <div
          class="tw-border-4 tw-border-dashed tw-border-gray-300 dark:tw-border-gray-600 tw-rounded-2xl tw-py-8 tw-px-5 tw-text-center tw-cursor-pointer tw-transition-all tw-duration-300 tw-bg-[var(--el-bg-color)] tw-relative tw-mb-5 hover:tw-border-indigo-500 hover:tw--translate-y-1"
          :class="{
            'tw-border-indigo-500 tw-bg-gradient-to-br tw-from-indigo-50 tw-to-blue-50 dark:tw-from-gray-600 dark:tw-to-gray-700 tw-scale-105':
              isDragOver,
          }"
          @dragover.prevent="handleDragOver"
          @dragleave.prevent="handleDragLeave"
          @drop.prevent="handleDrop"
        >
          <!-- 空状态显示 -->
          <div v-if="selectedFiles.length === 0">
            <span class="tw-text-5xl tw-text-indigo-500 tw-mb-5 tw-block">📤</span>
            <div class="tw-text-lg tw-text-gray-800 dark:tw-text-gray-100 tw-mb-3 tw-font-semibold">
              {{ t('upload.dragDrop') }}
            </div>
            <div class="tw-text-gray-600 dark:tw-text-gray-400 tw-text-sm tw-mb-5">
              {{ t('upload.clickSelect') }}
            </div>
            <div class="tw-flex tw-justify-center tw-gap-4">
              <button class="select-button" @click.stop="selectFiles">
                {{ t('upload.selectFiles') }}
              </button>
              <button class="select-button" @click.stop="selectFolder">
                {{ t('upload.selectFolder') }}
              </button>
            </div>
          </div>

          <!-- 有文件时显示文件列表 -->
          <div v-else>
            <div class="tw-text-lg tw-text-gray-800 dark:tw-text-gray-100 tw-mb-4 tw-font-semibold">
              {{ t('upload.filesSelected', { count: selectedFiles.length }) }}
            </div>

            <!-- 文件列表 -->
            <div
              class="file-list-container tw-mb-4"
              :class="{ scrollable: selectedFiles.length > 3 }"
            >
              <div class="tw-space-y-3">
                <div
                  v-for="(file, index) in selectedFiles"
                  :key="index"
                  class="file-list-item tw-flex tw-items-center tw-justify-between tw-p-3 tw-bg-white dark:tw-bg-gray-800 tw-rounded-xl tw-border tw-border-gray-200 dark:tw-border-gray-600 tw-transition-all tw-duration-300 hover:tw-bg-gray-50 dark:hover:tw-bg-gray-700 hover:tw-translate-x-1"
                >
                  <div class="tw-flex tw-items-center tw-flex-1 tw-min-w-0">
                    <span class="tw-text-lg tw-mr-3 tw-text-indigo-500">{{
                      getFileIcon(file.name)
                    }}</span>
                    <div class="tw-flex-1 tw-text-left tw-truncate">
                      <div
                        class="tw-font-semibold tw-text-gray-800 dark:tw-text-gray-100 tw-text-sm tw-mb-1 tw-truncate"
                      >
                        {{ file.webkitRelativePath || file.name }}
                      </div>
                      <div class="tw-text-gray-600 dark:tw-text-gray-400 tw-text-xs">
                        {{ formatFileSize(file.size) }}
                      </div>
                    </div>
                  </div>
                  <button
                    class="tw-bg-red-500 tw-text-white tw-border-none tw-rounded-full tw-w-7 tw-h-7 tw-cursor-pointer tw-flex tw-items-center tw-justify-center tw-transition-all tw-duration-300 tw-text-sm hover:tw-bg-red-600 hover:tw-scale-110 tw-flex-shrink-0"
                    @click.stop="removeFile(index)"
                  >
                    ×
                  </button>
                </div>
              </div>
            </div>

            <!-- 添加更多按钮 -->
            <div class="tw-flex tw-justify-center tw-gap-4">
              <button class="select-button" @click.stop="selectFiles">
                {{ t('upload.selectFiles') }}
              </button>
              <button class="select-button" @click.stop="selectFolder">
                {{ t('upload.selectFolder') }}
              </button>
            </div>
          </div>

          <!-- 隐藏的 input 元素 -->
          <input
            type="file"
            class="tw-hidden"
            ref="fileInput"
            multiple
            accept=".txt,.md,.log,.docx,.html,.pptx,.pdf"
            @change="handleFileSelect"
          />
          <input
            type="file"
            class="tw-hidden"
            ref="folderInput"
            multiple
            webkitdirectory
            @change="handleFolderSelect"
          />
        </div>

        <!-- 进度条 -->
        <div
          class="tw-w-full tw-h-2 tw-bg-gray-200 dark:tw-bg-gray-600 tw-rounded-full tw-overflow-hidden tw-mt-3"
          :style="{ display: showProgress ? 'block' : 'none' }"
        >
          <div
            class="tw-h-full tw-bg-gradient-to-r tw-from-indigo-500 tw-to-purple-600 tw-transition-all tw-duration-300 tw-rounded-full"
            :style="{ width: progress + '%' }"
          ></div>
        </div>

        <!-- 弹窗底部 -->
        <div class="tw-flex tw-gap-4 tw-justify-center tw-mt-8">
          <button
            class="tw-py-3 tw-px-6 tw-border-none tw-rounded-lg tw-text-sm tw-font-semibold tw-cursor-pointer tw-transition-all tw-duration-300 tw-uppercase tw-tracking-wide tw-bg-gray-500 tw-text-white hover:tw-bg-gray-600 hover:tw--translate-y-1"
            @click="closeModal"
          >
            {{ t('upload.cancel') }}
          </button>
          <button
            class="confirm-button"
            :disabled="selectedFiles.length === 0 || isUploading"
            @click="uploadFiles"
          >
            {{ isUploading ? t('upload.uploading') : t('upload.start') }}
          </button>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted, onBeforeUnmount } from 'vue'
import { uploadFileBatch, UPLOAD_PATHS } from '@/services/api.js'
import { useI18n } from 'vue-i18n'

// --- i18n ---
const { t } = useI18n()

// 响应式状态
const isModalOpen = ref(false)
const isDragOver = ref(false)
const selectedFiles = ref([])
const showProgress = ref(false)
const progress = ref(0)
const isUploading = ref(false)
const fileInput = ref(null)
const folderInput = ref(null) // 新增: 文件夹输入的ref
// 'files' 代表文件上传, 'folders' 代表文件夹上传
const uploadType = ref('files')
// 定义组件将发出的事件
const emit = defineEmits(['upload-completed'])

// --- 方法定义 ---

// 打开/关闭弹窗
const openModal = () => {
  console.log('方法调用：openModal')
  isModalOpen.value = true
  document.body.style.overflow = 'hidden'
  console.log('状态更新：isModalOpen = true')
}

const closeModal = () => {
  console.log('方法调用：closeModal')
  if (isUploading.value) {
    console.warn('警告：上传中，关闭弹窗操作被阻止。')
    return // 上传时不允许关闭
  }
  isModalOpen.value = false
  document.body.style.overflow = 'auto'
  resetModal()
  console.log('状态更新：isModalOpen = false')
}

// 重置状态
const resetModal = () => {
  console.log('方法调用：resetModal')
  selectedFiles.value = []
  showProgress.value = false
  progress.value = 0
  isUploading.value = false
  console.log('状态已重置。selectedFiles 列表已清空。')
}

// 文件和文件夹选择
const selectFiles = () => {
  console.log('方法调用：selectFiles。正在触发文件输入框点击事件。')
  fileInput.value?.click()
}

const selectFolder = () => {
  console.log('方法调用：selectFolder。正在触发文件夹输入框点击事件。')
  folderInput.value?.click()
}

const handleFileSelect = (event) => {
  // 更新上传类型
  uploadType.value = 'files'
  // [修正] 调用正确的方法名 addFilesToList
  addFilesToList(event.target.files)
  // 重置 input 以便可以再次选择相同的文件
  event.target.value = ''
}

// 用户点击 "选择文件夹" 按钮
const handleFolderSelect = (event) => {
  // 更新上传类型
  uploadType.value = 'folders'
  // [修正] 调用正确的方法名 addFilesToList
  addFilesToList(event.target.files)
  event.target.value = ''
}

// 文件列表操作
const addFilesToList = (files) => {
  console.log('方法调用：addFilesToList')
  const newFiles = Array.from(files)
  console.log(`接收到 ${newFiles.length} 个文件。当前已选择文件数：${selectedFiles.value.length}`)

  newFiles.forEach((file) => {
    // 使用相对路径或文件名作为唯一标识符
    const uniqueIdentifier = file.webkitRelativePath || file.name
    if (file.size > 10 * 1024 * 1024) {
      console.error(
        `文件 "${uniqueIdentifier}" 被拒绝：文件大小 (${(file.size / 1024 / 1024).toFixed(2)}MB) 超过 10MB 限制。`,
      )
      alert(`文件 "${uniqueIdentifier}" 超过10MB限制`)
      return
    }
    // 检查唯一标识符和大小
    if (
      !selectedFiles.value.some(
        (f) => (f.webkitRelativePath || f.name) === uniqueIdentifier && f.size === file.size,
      )
    ) {
      selectedFiles.value.push(file)
      console.log(`文件已添加："${uniqueIdentifier}" (${formatFileSize(file.size)})`)
    } else {
      console.warn(`文件 "${uniqueIdentifier}" 被拒绝：已存在于列表中。`)
    }
  })
  console.log(`更新后已选择文件数：${selectedFiles.value.length}`)
}

const removeFile = (index) => {
  const file = selectedFiles.value[index]
  const uniqueIdentifier = file?.webkitRelativePath || file?.name
  selectedFiles.value.splice(index, 1)
  console.log(
    `文件已移除："${uniqueIdentifier}"，索引为 ${index}。剩余文件数：${selectedFiles.value.length}`,
  )
}

// 核心上传逻辑
// 修改 uploadFiles 方法中的 uploadFileBatch 调用
const uploadFiles = async () => {
  console.log('方法调用：uploadFiles')
  if (selectedFiles.value.length === 0) {
    console.warn('上传终止：没有文件被选中。')
    return
  }

  isUploading.value = true
  showProgress.value = true
  progress.value = 0
  console.log('上传开始。isUploading = true, showProgress = true。')

  try {
    // +++ 动态决定目标文件夹 +++
    const destinationFolder =
      uploadType.value === 'folders'
        ? UPLOAD_PATHS.folders // '.'
        : UPLOAD_PATHS.files // './forRubbables'

    console.log(`🚀 Starting upload. Type: ${uploadType.value}, Destination: ${destinationFolder}`)

    const response = await uploadFileBatch(selectedFiles.value, {
      destinationFolder, // 使用我们动态决定的路径
      saveInfo: true,
      onUploadProgress: (progressEvent) => {
        if (progressEvent.total) {
          progress.value = Math.round((progressEvent.loaded * 100) / progressEvent.total)
        }
      },
    })

    const backendResponse = response.data
    console.log('上传完成。已接收到后端响应：', backendResponse)

    if (backendResponse.success) {
      console.log('后端报告上传成功。正在触发 "upload-completed" 事件。')
      emit('upload-completed', {
        success: true,
        newTree: backendResponse.new_tree,
        newFileList: backendResponse.new_file_list,
      })
    } else {
      console.error('后端报告上传失败。', backendResponse)
      throw new Error(backendResponse.message || '后端报告上传失败')
    }
  } catch (error) {
    console.error('上传过程中发生错误：', error.message)
    console.error('完整的错误对象：', error)
    emit('upload-completed', {
      success: false,
      error: error.message,
    })
  } finally {
    console.log('上传过程结束。正在启动清理计时器...')
    setTimeout(() => {
      isUploading.value = false
      closeModal()
      console.log('清理完成。弹窗已关闭。')
    }, 1500)
  }
}

// 拖拽事件
const handleDragOver = (event) => {
  console.log('拖拽事件：dragover')
  event.preventDefault()
  isDragOver.value = true
}

const handleDragLeave = (event) => {
  console.log('拖拽事件：dragleave')
  event.preventDefault()
  isDragOver.value = false
}

const handleDrop = (event) => {
  event.preventDefault()
  isDragging.value = false
  const files = event.dataTransfer.files
  if (files.length > 0) {
    // 判断拖拽类型并更新状态
    // 如果至少有一个文件包含相对路径，我们就认为是文件夹上传
    const isFolderDrop = Array.from(files).some((file) => file.webkitRelativePath)
    uploadType.value = isFolderDrop ? 'folders' : 'files'

    // [修正] 调用正确的方法名 addFilesToList
    addFilesToList(files)
  }
}

// 遮罩和键盘事件
const handleOverlayClick = (event) => {
  if (event.target === event.currentTarget) {
    console.log('事件：点击了遮罩层。正在关闭弹窗。')
    closeModal()
  }
}

const handleKeyDown = (event) => {
  if (event.key === 'Escape' && isModalOpen.value) {
    console.log('键盘事件：按下 Esc 键。正在关闭弹窗。')
    closeModal()
  }
}

// 生命周期钩子
onMounted(() => {
  console.log('组件已挂载。正在添加键盘事件监听器。')
  document.addEventListener('keydown', handleKeyDown)
})

onBeforeUnmount(() => {
  console.log('组件即将卸载。正在移除键盘事件监听器。')
  document.removeEventListener('keydown', handleKeyDown)
})

// 暴露给父组件的方法
defineExpose({ openModal })

// --- 辅助函数 ---
const formatFileSize = (bytes) => {
  if (bytes === 0) return '0 B'
  const k = 1024
  const sizes = ['B', 'KB', 'MB', 'GB']
  const i = Math.floor(Math.log(bytes) / Math.log(k))
  return parseFloat((bytes / Math.pow(k, i)).toFixed(2)) + ' ' + sizes[i]
}

const getFileIcon = (fileName) => {
  const extension = fileName.split('.').pop().toLowerCase()
  const iconMap = {
    pdf: '📄',
    doc: '📝',
    docx: '📝',
    jpg: '🖼️',
    jpeg: '🖼️',
    png: '🖼️',
    gif: '🖼️',
    zip: '📦',
    rar: '📦',
    txt: '📄',
    default: '📁',
  }
  return iconMap[extension] || iconMap['default']
}
</script>

<style scoped>
/* 文件列表容器样式 */
.file-list-container {
  max-height: none;
  overflow: visible;
  transition: all 0.3s ease;
}

.file-list-container.scrollable {
  max-height: 240px; /* 约3个文件项的高度 (每个约80px) */
  overflow-y: auto;
  padding-right: 4px;
}

/* 透明滚动条样式 */
.file-list-container.scrollable::-webkit-scrollbar {
  width: 6px;
}

.file-list-container.scrollable::-webkit-scrollbar-track {
  background: transparent;
  border-radius: 3px;
}

.file-list-container.scrollable::-webkit-scrollbar-thumb {
  background: rgba(156, 163, 175, 0.3);
  border-radius: 3px;
  transition: background 0.3s ease;
}

.file-list-container.scrollable::-webkit-scrollbar-thumb:hover {
  background: rgba(156, 163, 175, 0.5);
}

/* 暗色模式下的滚动条 */
@media (prefers-color-scheme: dark) {
  .file-list-container.scrollable::-webkit-scrollbar-thumb {
    background: rgba(209, 213, 219, 0.3);
  }

  .file-list-container.scrollable::-webkit-scrollbar-thumb:hover {
    background: rgba(209, 213, 219, 0.5);
  }
}

/* Firefox 滚动条样式 */
.file-list-container.scrollable {
  scrollbar-width: thin;
  scrollbar-color: rgba(156, 163, 175, 0.3) transparent;
}

@media (prefers-color-scheme: dark) {
  .file-list-container.scrollable {
    scrollbar-color: rgba(209, 213, 219, 0.3) transparent;
  }
}

/* 强制确保文件列表项的暗色模式样式 */
@media (prefers-color-scheme: dark) {
  .file-list-item {
    background-color: #374151 !important;
    border-color: #4b5563 !important;
    color: #f9fafb !important;
  }

  .file-list-item:hover {
    background-color: #4b5563 !important;
  }
}

/* 自定义选择按钮样式 (选择文件和选择文件夹) */
.select-button {
  background-color: #e5e7eb; /* gray-200 */
  color: #374047; /* gray-800 */
  border: 1px solid #d1d5db; /* gray-300 */
  padding: 0.75rem 2rem;
  border-radius: 9999px; /* full rounded */
  font-size: 0.875rem; /* sm */
  cursor: pointer;
  transition: all 0.3s ease;
  text-transform: uppercase;
  letter-spacing: 0.05em;
  font-weight: 600;
}

.select-button:hover {
  background-color: #d1d5db; /* gray-300 */
  border-color: #9ca3af; /* gray-400 */
  transform: translateY(-1px);
  box-shadow:
    0 4px 6px -1px rgba(0, 0, 0, 0.1),
    0 2px 4px -2px rgba(0, 0, 0, 0.1);
}

/* 暗色模式下的选择按钮样式 */
.dark .select-button {
  background-color: #4b5563; /* gray-600 */
  color: #e5e7eb; /* gray-200 */
  border-color: #4b5563; /* gray-600 */
}

.dark .select-button:hover {
  background-color: #374047; /* gray-700 */
  border-color: #6b7280; /* gray-500 */
}

/* 自定义确认按钮样式 (开始上传) */
.confirm-button {
  background-color: #e5e7eb; /* gray-200 */
  color: #374047; /* gray-800 */
  border: 1px solid #d1d5db; /* gray-300 */
  padding: 0.75rem 1.5rem;
  border-radius: 0.5rem; /* rounded-lg */
  font-size: 0.875rem; /* sm */
  font-weight: 600;
  text-transform: uppercase;
  letter-spacing: 0.025em;
  cursor: pointer;
  transition: all 0.3s ease;
}

.confirm-button:hover {
  background-color: #d1d5db; /* gray-300 */
  border-color: #9ca3af; /* gray-400 */
  transform: translateY(-1px);
  box-shadow:
    0 4px 6px -1px rgba(0, 0, 0, 0.1),
    0 2px 4px -2px rgba(0, 0, 0, 0.1);
}

.confirm-button:disabled {
  background-color: #e5e7eb; /* gray-400 */
  cursor: not-allowed;
  box-shadow: none;
  transform: none;
  border-color: #9ca3af; /* gray-400 */
}

/* 暗色模式下的确认按钮样式 */
.dark .confirm-button {
  background-color: #4b5563; /* gray-600 */
  color: #e5e7eb; /* gray-200 */
  border-color: #4b5563; /* gray-600 */
}

.dark .confirm-button:hover {
  background-color: #374047; /* gray-700 */
  border-color: #6b7280; /* gray-500 */
}

.dark .confirm-button:disabled {
  background-color: #4b5563; /* gray-600 */
  border-color: #4b5563; /* gray-600 */
  opacity: 0.6;
}

@media (max-width: 768px) {
  .tw-p-10 {
    padding: 2rem !important;
  }

  .tw-py-16 {
    padding-top: 2.5rem !important;
    padding-bottom: 2.5rem !important;
  }

  .tw-flex {
    flex-direction: column !important;
  }

  .tw-gap-4 > * {
    width: 100% !important;
    margin-bottom: 0.75rem !important;
  }

  /* 移动端滚动区域调整 */
  .file-list-container.scrollable {
    max-height: 200px;
  }
}
</style>
