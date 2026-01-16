<!-- views/forTradition.vue -->
<template>
  <!-- 根容器：使用flexbox垂直布局，并占据父容器的全部可用高度 -->
  <div class="tw-h-full tw-flex tw-flex-col">
    <!-- 主网格区域：占据所有剩余空间(tw-flex-1)，并自身是一个grid布局。tw-min-h-0是防止内容溢出的关键。 -->
    <div class="tw-flex-1 tw-grid tw-grid-cols-1 lg:tw-grid-cols-4 tw-gap-6 tw-min-h-0">
      
      <!-- 左列：使用flexbox垂直布局，并强制其内容在内部消化溢出(tw-overflow-hidden) -->
      <div class="lg:tw-col-span-1 tw-flex tw-flex-col tw-space-y-4 tw-overflow-hidden">
        <!-- 筛选器：高度由自身内容决定 -->
        <TraditionalFilter @filters-changed="handleFiltersChange" />
        <!-- FileTree的容器：占据所有剩余空间(tw-flex-1)，tw-min-h-0防止自身被撑开 -->
        <div class="tw-flex-1 tw-min-h-0">
          <FileTree :tree-data="fileTree" :is-loading="isTreeLoading" />
        </div>
      </div>

      <!-- 右列：容器占据100%高度，并隐藏溢出 -->
      <div class="lg:tw-col-span-3 tw-h-full tw-overflow-hidden">
        <DocItem
          :documents="fileList"
          :is-loading="isListLoading"
          @new-document="openUploadModal"
        />
      </div>
    </div>

    <!-- 文件上传模态框 -->
    <FileUploadModal ref="uploadModal" @upload-completed="handleUploadSuccess" />
  </div>
</template>

<script setup>
import { onMounted, onActivated, ref } from 'vue'
import { storeToRefs } from 'pinia'
import { useFileStore } from '@/stores/modules/filestore'
import TraditionalFilter from '@/components/traditional/TraditionalFilter.vue'
import FileTree from '@/components/traditional/FileTree.vue'
import DocItem from '@/components/traditional/DocItem.vue'
import FileUploadModal from '@/components/common/FileUploadModal.vue' // 导入上传模态框组件
const uploadModal = ref(null)
const fileStore = useFileStore()
const { fileTree, isTreeLoading, fileList, isListLoading, needsRefresh, currentFilters } = storeToRefs(fileStore)

// 打开上传模态框的方法
const openUploadModal = () => {
  if (uploadModal.value) {
    uploadModal.value.openModal()
  }
}

// 处理上传成功后的回调
const handleUploadSuccess = (uploadResult) => {
  console.log('✅ [forTradition] handleUploadSuccess is now calling fileStore.setUploadData.')
  fileStore.setUploadData(uploadResult)
}
// 处理筛选条件变化的方法
const handleFiltersChange = (newFilters) => {
  fileStore.fetchFileList({ filters: newFilters })
}

// 在组件挂载后，获取初始数据
onMounted(() => {
  // 首次加载：只有当列表为空时才获取数据，或者强制初始化
  if (fileList.value.length === 0) {
    fileStore.fetchFileTree()
    fileStore.fetchFileList()
  }
})

// 当组件被激活时（例如从其他路由返回），只在需要刷新时才获取数据
onActivated(() => {
  // 核心逻辑：只有被标记为需要刷新时，才重新请求后端
  if (needsRefresh.value) {
    // 刷新时可能需要重新获取树和列表，视具体需求而定，这里保持与 filtersChange 一致的逻辑或者是全量刷新
    // 既然是 activated，通常检查是否需要更新列表
    fileStore.fetchFileList({ filters: currentFilters.value })
    // 如果树也需要刷新（比如有新文件夹），也可以加上 fetchFileTree
    // fileStore.fetchFileTree() 
    
    // 刷新完成后，重置标记由 store 内部处理(fetchFileList 成功后会设为 false)
  }
})
</script>
<style scoped>
/* 这一整块都是与滚动条相关的 */
.custom-scrollbar {
  /* 针对 Firefox 浏览器 */
  scrollbar-width: thin;
  scrollbar-color: #d1d5db #f3f4f6; /* 滚动条滑块颜色 和 轨道颜色 */
}

/* 针对 Webkit 内核的浏览器 (Chrome, Safari, Edge等) */
.custom-scrollbar::-webkit-scrollbar {
  width: 8px; /* 滚动条宽度 */
}

.custom-scrollbar::-webkit-scrollbar-track {
  background: #f3f4f6; /* 轨道背景色 */
  border-radius: 4px; /* 轨道圆角 */
}

.custom-scrollbar::-webkit-scrollbar-thumb {
  background-color: #d1d5db; /* 滑块背景色 */
  border-radius: 4px; /* 滑块圆角 */
  transition: background-color 0.2s ease; /* 鼠标悬浮时的颜色过渡效果 */
}

.custom-scrollbar::-webkit-scrollbar-thumb:hover {
  background-color: #9ca3af; /* 鼠标悬浮在滑块上时的颜色 */
}

/* 暗色模式下的滚动条样式 */
.dark .custom-scrollbar {
  /* 针对 Firefox 浏览器 */
  scrollbar-color: #4b5563 #374151;
}

.dark .custom-scrollbar::-webkit-scrollbar-track {
  background: #374151; /* 暗色模式轨道背景色 */
}

.dark .custom-scrollbar::-webkit-scrollbar-thumb {
  background-color: #4b5563; /* 暗色模式滑块背景色 */
}

.dark .custom-scrollbar::-webkit-scrollbar-thumb:hover {
  background-color: #6b7280; /* 暗色模式鼠标悬浮在滑块上时的颜色 */
}
</style>
