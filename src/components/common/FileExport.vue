<template>
  <el-dialog
    v-model="isModalOpen"
    title="文件导出"
    width="800"
    :before-close="closeModal"
    align-center
    top="5vh"
    :close-on-click-modal="false"
  >
    <div class="tw-space-y-6">
      <!-- 文件选择区域 -->
      <div
        class="tw-p-4 tw-rounded-lg tw-border tw-bg-white dark:tw-bg-gray-800 tw-border-gray-200 dark:tw-border-gray-700"
      >
        <h4 class="tw-font-medium tw-mb-4 tw-text-gray-800 dark:tw-text-gray-100">
          选择文件或文件夹
        </h4>
        <div class="tw-flex tw-gap-4 tw-mb-4">
          <el-button type="primary" @click="selectFiles" :disabled="isExporting" class="tw-flex-1">
            <FileText class="tw-w-4 tw-h-4 tw-mr-2" />
            选择文件
          </el-button>
          <el-button type="primary" @click="selectFolder" :disabled="isExporting" class="tw-flex-1">
            <Folder class="tw-w-4 tw-h-4 tw-mr-2" />
            选择文件夹
          </el-button>
        </div>

        <!-- 文件统计信息 -->
        <div
          v-if="selectedItems.length > 0"
          class="tw-bg-blue-50 dark:tw-bg-blue-900/20 tw-border tw-border-blue-200 dark:tw-border-blue-700 tw-rounded-lg tw-p-4 tw-mb-4"
        >
          <div class="tw-flex tw-items-center tw-justify-between tw-mb-2">
            <span
              class="tw-text-blue-800 dark:tw-text-blue-200 tw-font-semibold tw-flex tw-items-center tw-gap-2"
            >
              <BarChart3 class="tw-w-4 tw-h-4" />
              导出统计
            </span>
            <el-button
              size="small"
              type="danger"
              plain
              @click="clearSelection"
              :disabled="isExporting"
            >
              清空选择
            </el-button>
          </div>
          <div class="tw-grid tw-grid-cols-2 tw-gap-4">
            <div class="tw-text-center">
              <div class="tw-text-2xl tw-font-bold tw-text-blue-600 dark:tw-text-blue-400">
                {{ totalFiles }}
              </div>
              <div class="tw-text-sm tw-text-blue-700 dark:tw-text-blue-300">文件数量</div>
            </div>
            <div class="tw-text-center">
              <div class="tw-text-2xl tw-font-bold tw-text-green-600 dark:tw-text-green-400">
                {{ formatFileSize(totalSize) }}
              </div>
              <div class="tw-text-sm tw-text-green-700 dark:tw-text-green-300">总大小</div>
            </div>
          </div>
        </div>

        <!-- 选中的文件列表 -->
        <div
          v-if="selectedItems.length > 0"
          class="file-list-container custom-scrollbar"
          :class="{ scrollable: selectedItems.length > 4 }"
        >
          <div class="tw-space-y-2">
            <div
              v-for="(item, index) in selectedItems"
              :key="index"
              class="tw-flex tw-items-center tw-justify-between tw-p-3 tw-bg-gray-50 dark:tw-bg-gray-700 tw-rounded-lg tw-border tw-border-gray-200 dark:tw-border-gray-600 tw-transition-all tw-duration-300 hover:tw-bg-gray-100 dark:hover:tw-bg-gray-600"
            >
              <div class="tw-flex tw-items-center tw-flex-1">
                <span class="tw-text-lg tw-mr-3">
                  {{ item.type === 'folder' ? '📁' : getFileIcon(item.name) }}
                </span>
                <div class="tw-flex-1 tw-text-left">
                  <div
                    class="tw-font-semibold tw-text-gray-800 dark:tw-text-gray-100 tw-text-sm tw-mb-1"
                  >
                    {{ item.name }}
                  </div>
                  <div class="tw-text-gray-600 dark:tw-text-gray-400 tw-text-xs">
                    {{
                      item.type === 'folder'
                        ? `文件夹 (${item.fileCount} 个文件)`
                        : formatFileSize(item.size)
                    }}
                  </div>
                </div>
              </div>
              <el-button
                size="small"
                type="danger"
                circle
                @click="removeItem(index)"
                :disabled="isExporting"
              >
                <X class="tw-w-3 tw-h-3" />
              </el-button>
            </div>
          </div>
        </div>
      </div>

      <!-- 导出选项 -->
      <div
        v-if="selectedItems.length > 0"
        class="tw-p-4 tw-rounded-lg tw-border tw-bg-white dark:tw-bg-gray-800 tw-border-gray-200 dark:tw-border-gray-700"
      >
        <h4 class="tw-font-medium tw-mb-4 tw-text-gray-800 dark:tw-text-gray-100">导出设置</h4>

        <div class="tw-mb-4">
          <label
            class="tw-block tw-text-sm tw-font-medium tw-text-gray-700 dark:tw-text-gray-300 tw-mb-2"
          >
            导出格式
          </label>
          <el-select
            v-model="exportFormat"
            placeholder="选择导出格式"
            class="tw-w-full"
            :disabled="isExporting"
          >
            <el-option label="ZIP 压缩包" value="zip"></el-option>
            <el-option label="TAR 归档" value="tar"></el-option>
            <el-option label="RAR 压缩包" value="rar"></el-option>
          </el-select>
        </div>

        <div class="tw-mb-4">
          <label
            class="tw-block tw-text-sm tw-font-medium tw-text-gray-700 dark:tw-text-gray-300 tw-mb-2"
          >
            导出文件名
          </label>
          <el-input v-model="exportFileName" placeholder="输入导出文件名" :disabled="isExporting">
            <template #suffix>
              <span class="tw-text-gray-500">.{{ exportFormat }}</span>
            </template>
          </el-input>
        </div>
      </div>

      <!-- 进度条 -->
      <div
        v-if="isExporting"
        class="tw-p-4 tw-rounded-lg tw-border tw-bg-white dark:tw-bg-gray-800 tw-border-gray-200 dark:tw-border-gray-700"
      >
        <div class="tw-flex tw-items-center tw-justify-between tw-mb-2">
          <span class="tw-text-sm tw-font-medium tw-text-gray-700 dark:tw-text-gray-300">
            导出进度
          </span>
          <span class="tw-text-sm tw-text-gray-600 dark:tw-text-gray-400">
            {{ Math.round(exportProgress) }}%
          </span>
        </div>
        <el-progress
          :percentage="exportProgress"
          :stroke-width="8"
          :show-text="false"
          class="tw-mb-2"
        ></el-progress>
        <div class="tw-text-center tw-text-sm tw-text-gray-600 dark:tw-text-gray-400">
          {{ exportStatus }}
        </div>
      </div>
    </div>

    <template #footer>
      <div class="tw-flex tw-gap-4 tw-justify-end">
        <el-button @click="closeModal" :disabled="isExporting"> 取消 </el-button>
        <el-button
          type="primary"
          @click="startExport"
          :disabled="selectedItems.length === 0 || isExporting"
          :loading="isExporting"
        >
          {{ isExporting ? '导出中...' : '开始导出' }}
        </el-button>
      </div>
    </template>

    <!-- 隐藏的文件输入 -->
    <input type="file" ref="fileInput" multiple class="tw-hidden" @change="handleFileSelect" />
    <input
      type="file"
      ref="folderInput"
      webkitdirectory
      class="tw-hidden"
      @change="handleFolderSelect"
    />
  </el-dialog>
</template>

<script setup>
import { ref, computed, onMounted, onBeforeUnmount } from 'vue'
import { FileText, Folder, BarChart3, X } from 'lucide-vue-next'
import { ElMessage } from 'element-plus'

// 响应式数据
const isModalOpen = ref(false)
const selectedItems = ref([])
const exportFormat = ref('zip')
const exportFileName = ref('export')
const isExporting = ref(false)
const exportProgress = ref(0)
const exportStatus = ref('')

// 文件输入引用
const fileInput = ref(null)
const folderInput = ref(null)

// 计算属性
const totalFiles = computed(() => {
  return selectedItems.value.reduce((total, item) => {
    return total + (item.type === 'folder' ? item.fileCount : 1)
  }, 0)
})

const totalSize = computed(() => {
  return selectedItems.value.reduce((total, item) => {
    return total + item.size
  }, 0)
})

// 方法
const openModal = () => {
  isModalOpen.value = true
}

const closeModal = () => {
  isModalOpen.value = false
  resetModal()
}

const resetModal = () => {
  selectedItems.value = []
  exportFormat.value = 'zip'
  exportFileName.value = 'export'
  isExporting.value = false
  exportProgress.value = 0
  exportStatus.value = ''
}

const selectFiles = () => {
  fileInput.value?.click()
}

const selectFolder = () => {
  folderInput.value?.click()
}

const handleFileSelect = (event) => {
  const files = Array.from(event.target.files)
  files.forEach((file) => {
    if (!selectedItems.value.some((item) => item.name === file.name && item.size === file.size)) {
      selectedItems.value.push({
        name: file.name,
        size: file.size,
        type: 'file',
        file: file,
      })
    }
  })
  event.target.value = ''
}

const handleFolderSelect = (event) => {
  const files = Array.from(event.target.files)
  if (files.length === 0) return

  const folderPath = files[0].webkitRelativePath
  const folderName = folderPath.split('/')[0]
  const totalSize = files.reduce((sum, file) => sum + file.size, 0)

  if (!selectedItems.value.some((item) => item.name === folderName && item.type === 'folder')) {
    selectedItems.value.push({
      name: folderName,
      size: totalSize,
      type: 'folder',
      fileCount: files.length,
      files: files,
    })
  }
  event.target.value = ''
}

const removeItem = (index) => {
  selectedItems.value.splice(index, 1)
}

const clearSelection = () => {
  selectedItems.value = []
}

const startExport = async () => {
  if (selectedItems.value.length === 0) return

  isExporting.value = true
  exportProgress.value = 0
  exportStatus.value = '准备导出...'

  try {
    const steps = [
      { progress: 20, status: '正在压缩文件...' },
      { progress: 50, status: '正在处理文件夹...' },
      { progress: 80, status: '正在生成压缩包...' },
      { progress: 100, status: '导出完成！' },
    ]

    for (const step of steps) {
      await simulateProgress(step.progress, step.status)
      await new Promise((resolve) => setTimeout(resolve, 800))
    }

    downloadExportFile()

    setTimeout(() => {
      ElMessage.success('文件导出成功！')
      closeModal()
    }, 1000)
  } catch (error) {
    ElMessage.error('导出失败：' + error.message)
    isExporting.value = false
  }
}

const simulateProgress = (targetProgress, status) => {
  return new Promise((resolve) => {
    const interval = setInterval(() => {
      if (exportProgress.value < targetProgress) {
        exportProgress.value += 2
        exportStatus.value = status
      } else {
        clearInterval(interval)
        resolve()
      }
    }, 50)
  })
}

const downloadExportFile = () => {
  const fileName = `${exportFileName.value}.${exportFormat.value}`
  const content = `导出文件: ${fileName}\n文件数量: ${totalFiles.value}\n总大小: ${formatFileSize(totalSize.value)}`
  const blob = new Blob([content], { type: 'text/plain' })

  const url = URL.createObjectURL(blob)
  const a = document.createElement('a')
  a.href = url
  a.download = fileName
  document.body.appendChild(a)
  a.click()
  document.body.removeChild(a)
  URL.revokeObjectURL(url)
}

const formatFileSize = (bytes) => {
  if (bytes === 0) return '0 B'
  const k = 1024
  const sizes = ['B', 'KB', 'MB', 'GB', 'TB']
  const i = Math.floor(Math.log(bytes) / Math.log(k))
  return parseFloat((bytes / Math.pow(k, i)).toFixed(2)) + ' ' + sizes[i]
}

const getFileIcon = (fileName) => {
  const extension = fileName.split('.').pop().toLowerCase()
  const iconMap = {
    pdf: '📄',
    doc: '📝',
    docx: '📝',
    txt: '📄',
    jpg: '🖼️',
    jpeg: '🖼️',
    png: '🖼️',
    gif: '🖼️',
    svg: '🖼️',
    mp4: '🎥',
    avi: '🎥',
    mp3: '🎵',
    wav: '🎵',
    zip: '📦',
    rar: '📦',
    tar: '📦',
    js: '📜',
    ts: '📜',
    vue: '💚',
    html: '🌐',
    css: '🎨',
    json: '📋',
    xml: '📋',
    default: '📄',
  }
  return iconMap[extension] || iconMap['default']
}

const handleKeyDown = (event) => {
  if (event.key === 'Escape' && isModalOpen.value && !isExporting.value) {
    closeModal()
  }
}

// 生命周期
onMounted(() => {
  document.addEventListener('keydown', handleKeyDown)
})

onBeforeUnmount(() => {
  document.removeEventListener('keydown', handleKeyDown)
})

// 暴露方法给父组件
defineExpose({
  openModal,
})
</script>

<style scoped>
.custom-scrollbar {
  scrollbar-width: thin;
  scrollbar-color: #d1d5db #f3f4f6;
}

.custom-scrollbar::-webkit-scrollbar {
  width: 8px;
}

.custom-scrollbar::-webkit-scrollbar-track {
  background: #f3f4f6;
  border-radius: 4px;
}

.custom-scrollbar::-webkit-scrollbar-thumb {
  background-color: #d1d5db;
  border-radius: 4px;
  transition: background-color 0.2s ease;
}

.custom-scrollbar::-webkit-scrollbar-thumb:hover {
  background-color: #9ca3af;
}

/* 暗色模式下的滚动条样式 */
.dark .custom-scrollbar {
  scrollbar-color: #4b5563 #374151;
}

.dark .custom-scrollbar::-webkit-scrollbar-track {
  background: #374151;
}

.dark .custom-scrollbar::-webkit-scrollbar-thumb {
  background-color: #4b5563;
}

.dark .custom-scrollbar::-webkit-scrollbar-thumb:hover {
  background-color: #6b7280;
}

/* 文件列表容器样式 */
.file-list-container {
  max-height: none;
  overflow: visible;
  transition: all 0.3s ease;
}

.file-list-container.scrollable {
  max-height: 300px;
  overflow-y: auto;
  padding-right: 4px;
}

/* 响应式设计 */
@media (max-width: 768px) {
  .tw-grid-cols-2 {
    grid-template-columns: 1fr !important;
  }

  .tw-flex-1 {
    flex: none !important;
    width: 100% !important;
    margin-bottom: 0.5rem !important;
  }

  .file-list-container.scrollable {
    max-height: 250px;
  }
}
</style>
