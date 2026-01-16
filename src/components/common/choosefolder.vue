<template>
  <div class="folder-selector-container">
    <!-- 文件夹选择输入框 -->
    <div class="tw-mb-3">
      <input
        ref="folderInput"
        type="file"
        webkitdirectory
        multiple
        @change="handleFolderSelect"
        class="tw-hidden"
      />
      <button
        @click="openFolderDialog"
        class="tw-w-full tw-px-3 tw-py-2 tw-border tw-border-gray-200 dark:tw-border-gray-600 tw-rounded-lg tw-bg-white dark:tw-bg-gray-700 tw-text-left tw-flex tw-justify-between tw-items-center tw-transition-colors hover:tw-border-gray-300 dark:hover:tw-border-gray-500"
      >
        <span class="tw-text-gray-900 dark:tw-text-gray-100">
          {{ selectedFolderName || '选择文件夹' }}
        </span>
        <Folder class="tw-w-4 tw-h-4 tw-text-gray-500" />
      </button>
    </div>

    <!-- 文件夹信息显示 -->
    <div v-if="folderInfo.fileCount > 0" class="tw-text-sm tw-text-gray-600 dark:tw-text-gray-400">
      <p>已选择文件夹: {{ folderInfo.folderName }}</p>
      <p>包含文件: {{ folderInfo.fileCount }} 个</p>
      <p>总大小: {{ formatFileSize(folderInfo.totalSize) }}</p>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import { Folder } from 'lucide-vue-next'

// 文件夹选择相关
const folderInput = ref(null)
const selectedFolderName = ref('')
const selectedFiles = ref([])
const folderInfo = ref({
  folderName: '',
  fileCount: 0,
  totalSize: 0,
})

// 定义 emits
const emit = defineEmits(['folder-selected'])

// 打开文件夹选择对话框
const openFolderDialog = () => {
  folderInput.value?.click()
}

// 处理文件夹选择
const handleFolderSelect = (event) => {
  const files = Array.from(event.target.files)

  if (files.length === 0) return

  selectedFiles.value = files

  // 获取文件夹名称（从第一个文件的路径中提取）
  const firstFile = files[0]
  const pathParts = firstFile.webkitRelativePath.split('/')
  const folderName = pathParts[0]

  selectedFolderName.value = folderName

  // 计算文件夹信息
  const totalSize = files.reduce((sum, file) => sum + file.size, 0)

  folderInfo.value = {
    folderName,
    fileCount: files.length,
    totalSize,
  }

  // 发出事件，传递选择的文件信息
  emit('folder-selected', {
    folderName,
    files,
    fileCount: files.length,
    totalSize,
  })
}

// 格式化文件大小
const formatFileSize = (bytes) => {
  if (bytes === 0) return '0 B'

  const k = 1024
  const sizes = ['B', 'KB', 'MB', 'GB']
  const i = Math.floor(Math.log(bytes) / Math.log(k))

  return parseFloat((bytes / Math.pow(k, i)).toFixed(2)) + ' ' + sizes[i]
}
</script>


