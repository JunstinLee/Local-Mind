<template>
  <div 
    ref="scrollContainer"
    class="main-content custom-scrollbar"
    v-infinite-scroll="loadMoreDocuments"
    :infinite-scroll-disabled="noMore || isLoading"
    :infinite-scroll-distance="50"
  >
    <!-- 内容头部 -->
    <div class="content-header">
      <h2>{{ title || defaultTitle }} ({{ documents.length }})</h2>
      <div class="header-actions"></div>
    </div>

    <!-- 加载状态 -->
    <div
      v-if="isLoading"
      class="loading-state"
      v-loading="true"
      :element-loading-text="t('document.loadingText')"
      element-loading-background="transparent"
    >
      <div class="tw-h-32"></div>
    </div>

    <!-- 文档列表 -->
    <div v-else-if="documents.length > 0" class="document-list">
      <div
        v-for="(doc, index) in visibleDocuments"
        :key="doc.path || index"
        class="document-item group"
      >
        <!-- 文档标题 -->
        <div class="result-title">
          <span class="title-text">{{ doc.name }}</span>

          <!-- 操作按钮 -->
          <div
            class="document-actions opacity-0 group-hover:opacity-100 transition-opacity duration-200"
          >
            <el-dropdown trigger="click" @command="(cmd) => handleCommand(cmd, doc)">
              <el-button type="text" size="small" class="more-btn">
                <i class="el-icon-more"></i>
              </el-button>
              <template #dropdown>
                <el-dropdown-menu class="dropdown-menu">
                  <el-dropdown-item command="detail" class="dropdown-item">
                    <i class="el-icon-view mr-2"></i>{{ t('document.detail') }}
                  </el-dropdown-item>
                  <el-dropdown-item command="delete" divided class="dropdown-item delete-item">
                    <i class="el-icon-delete mr-2"></i>{{ t('document.delete') }}
                  </el-dropdown-item>
                </el-dropdown-menu>
              </template>
            </el-dropdown>
          </div>
        </div>

        <!-- 文档元信息 -->
        <div class="document-meta">
          <span class="meta-item"> 📅 {{ formatDate(doc.modified_date) }} </span>
          <span class="meta-separator">|</span>
          <span class="meta-item"> 📦 {{ formatSize(doc.size) }} </span>
          <span class="meta-separator">|</span>
          <span class="meta-item path-item"> 📍 {{ doc.path }} </span>
        </div>
      </div>

      <!-- 底部加载状态 -->
      <div v-if="documents.length > visibleLimit" class="tw-text-center tw-py-4 tw-text-gray-400 tw-text-xs">
         <span v-if="!noMore">{{ t('common.loading', '加载中...') }}</span>
         <span v-else>{{ t('common.noMore', '没有更多了') }}</span>
      </div>
    </div>

    <!-- 空状态 -->
    <div v-else class="empty-state">
      <el-empty :description="t('document.noDocuments')">
        <p class="tw-text-sm tw-text-gray-500">
          {{ t('document.adjustOrImport') }}
        </p>
      </el-empty>
    </div>
  </div>
</template>

<script setup>
import { ElMessage, ElMessageBox } from 'element-plus'
import { useI18n } from 'vue-i18n'
import { computed, ref, watch, onActivated, onDeactivated, nextTick } from 'vue'

const { t } = useI18n()

// 1. 修改Props定义，使其更符合从父组件接收数据的模式
const props = defineProps({
  title: {
    type: String,
    default: '',
  },
  documents: {
    type: Array,
    default: () => [], // 提供一个默认的空数组
  },
  isLoading: {
    type: Boolean,
    default: false,
  },
})

// 设置默认标题
const defaultTitle = computed(() => t('document.listTitleDefault'))

// 2. 移除本地数据管理，直接使用props

// 3. 格式化方法
const formatDate = (dateString) => {
  if (!dateString) return 'N/A'
  const date = new Date(dateString)
  return date.toLocaleString('zh-CN', {
    year: 'numeric',
    month: '2-digit',
    day: '2-digit',
    hour: '2-digit',
    minute: '2-digit',
  })
}

const formatSize = (bytes) => {
  if (bytes === 0) return '0 B'
  const k = 1024
  const sizes = ['B', 'KB', 'MB', 'GB', 'TB']
  const i = Math.floor(Math.log(bytes) / Math.log(k))
  return parseFloat((bytes / Math.pow(k, i)).toFixed(2)) + ' ' + sizes[i]
}

// 4. 事件处理方法 (简化)
const handleNewDocument = () => {
  ElMessage.info('请从外部导入文件。')
}

const handleCommand = (command, doc) => {
  switch (command) {
    case 'detail':
      ElMessageBox.alert(`<pre>${JSON.stringify(doc, null, 2)}</pre>`, '文件详情', {
        dangerouslyUseHTMLString: true,
        confirmButtonText: '关闭',
      })
      break
    case 'delete':
      ElMessageBox.confirm(`确定要删除文档 "${doc.name}" 吗？`, '删除确认', {
        confirmButtonText: '确定',
        cancelButtonText: '取消',
        type: 'warning',
      })
        .then(() => {
          // 注意：这里只是示意，实际的删除操作需要调用API并通知父组件刷新列表
          ElMessage.success('删除操作（仅为示例）')
        })
        .catch(() => {
          ElMessage.info('已取消删除')
        })
      break
  }
}

// 5. 分页/无限加载与状态保持逻辑
const PAGE_SIZE = 20
const MAX_KEEP_ALIVE_ITEMS = 500 // 防御性阈值
const visibleLimit = ref(PAGE_SIZE)
const scrollContainer = ref(null)
const scrollTop = ref(0) // 记录滚动位置

// 是否没有更多数据了
const noMore = computed(() => visibleLimit.value >= props.documents.length)

// 计算当前显示的文档列表
const visibleDocuments = computed(() => {
  return props.documents.slice(0, visibleLimit.value)
})

// 加载更多
const loadMoreDocuments = () => {
  if (noMore.value) return
  visibleLimit.value += PAGE_SIZE
}

// 智能监听文档列表变化
watch(
  () => props.documents,
  (newDocs, oldDocs) => {
    // 仅当列表长度发生实质变化时才重置
    // 防抖动：如果长度没变（大概率是KeepAlive恢复），就不重置，保持当前浏览位置
    if (newDocs.length !== oldDocs?.length) {
       visibleLimit.value = PAGE_SIZE
    }
  },
)

// --- KeepAlive 生命周期钩子 ---

onDeactivated(() => {
  // 1. 记录离开时的滚动位置
  if (scrollContainer.value) {
    scrollTop.value = scrollContainer.value.scrollTop
  }
  
  // 2. 防御性重置：防止内存无限膨胀
  if (visibleLimit.value > MAX_KEEP_ALIVE_ITEMS) {
    visibleLimit.value = MAX_KEEP_ALIVE_ITEMS
    // 重置后，滚动位置可能不再有效（因为内容变短了），这是一种权衡
    // 这里选择归零或者保留（如果保留可能会因为内容变短而自动顶上去）
  }
})

onActivated(() => {
  // 恢复滚动位置
  nextTick(() => {
    if (scrollContainer.value) {
      scrollContainer.value.scrollTop = scrollTop.value
    }
  })
})
</script>

<style scoped>
.main-content {
  @apply tw-h-full  dark:tw-bg-gray-800 tw-overflow-y-auto tw-transition-colors tw-duration-200 tw-p-6;
}

.loading-state {
  @apply tw-h-full tw-flex tw-items-center tw-justify-center;
}

.path-item {
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
  max-width: 300px; /* 根据需要调整 */
}

/* ...保留所有原有样式... */

html.dark .main-content {
  background-color: #1e1e20 !important; /* gray-800 */
}

.content-header {
  @apply tw-flex tw-justify-between tw-items-center tw-mb-6 tw-bg-gray-50 tw-p-4 tw-rounded-lg tw-transition-colors tw-duration-200;
}

html.dark .content-header {
  background-color: #1e1e20 !important; /* gray-700 */
}

.content-header h2 {
  @apply tw-text-xl tw-font-semibold tw-text-gray-800 tw-m-0 tw-transition-colors tw-duration-200;
}

html.dark .content-header h2 {
  color: rgb(243 244 246) !important; /* gray-100 */
}

.header-actions {
  @apply tw-flex tw-space-x-3 tw-flex-wrap tw-gap-2;
}

.btn {
  @apply tw-px-4 tw-py-2 tw-rounded-md tw-font-medium tw-transition-all tw-duration-200 tw-text-sm;
}

.btn-primary {
  @apply tw-bg-blue-600 dark:tw-bg-blue-700 tw-text-white hover:tw-bg-blue-700 dark:hover:tw-bg-blue-600 tw-border-0 tw-shadow-sm hover:tw-shadow-md;
}

.document-list {
  @apply tw-space-y-4;
}

.document-item {
  @apply tw-bg-gray-50 tw-p-5 tw-rounded-lg tw-shadow-sm tw-border tw-border-gray-200 hover:tw-bg-gray-100 hover:tw-shadow-md tw-transition-all tw-duration-200 tw-cursor-pointer tw-relative;
}

html.dark .document-item {
  background-color: rgb(55 65 81) !important; /* gray-700 */
  border-color: rgb(75 85 99) !important; /* gray-600 */
  box-shadow: 0 1px 3px 0 rgba(0, 0, 0, 0.3) !important;
}

html.dark .document-item:hover {
  background-color: rgb(75 85 99) !important; /* gray-600 */
  box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.4) !important;
}

.document-item:hover {
  @apply tw-border-blue-300 dark:tw-border-blue-600 tw-transform tw-scale-[1.01];
}

.document-item.selected {
  @apply tw-border-blue-500 dark:tw-border-blue-400 tw-bg-blue-50 dark:tw-bg-blue-900/20 tw-shadow-md dark:tw-shadow-blue-900/20;
}

.result-title {
  @apply tw-flex tw-items-center tw-justify-between tw-mb-3 tw-gap-3;
}

.title-text {
  @apply tw-text-lg tw-font-semibold tw-text-gray-900 hover:tw-text-blue-600 tw-transition-colors tw-duration-200 tw-flex-1 tw-min-w-0;
}

html.dark .title-text {
  color: rgb(243 244 246) !important; /* gray-100 */
}

html.dark .title-text:hover {
  color: rgb(96 165 250) !important; /* blue-400 */
}

.document-actions {
  @apply tw-flex tw-items-center tw-flex-shrink-0;
}

.result-snippet {
  @apply tw-text-gray-600 tw-text-sm tw-leading-6 tw-mb-3 tw-line-clamp-2 tw-transition-colors tw-duration-200;
}

html.dark .result-snippet {
  color: rgb(209 213 219) !important; /* gray-300 */
}

.document-meta {
  @apply tw-text-xs tw-text-gray-500 tw-flex tw-items-center tw-flex-wrap tw-gap-2 tw-transition-colors tw-duration-200;
}

html.dark .document-meta {
  color: rgb(156 163 175) !important; /* gray-400 */
}

.meta-item {
  @apply tw-flex tw-items-center tw-gap-1;
}

.meta-separator {
  @apply tw-mx-1 tw-text-gray-300 dark:tw-text-gray-600;
}

.empty-state {
  @apply tw-text-center tw-py-12 tw-text-gray-500 dark:tw-text-gray-400 tw-transition-colors tw-duration-200;
}

/* 响应式设计 */
@media (max-width: 768px) {
  .main-content {
    @apply tw-p-4;
  }

  .content-header {
    @apply tw-flex-col tw-space-y-3 tw-items-start;
  }

  .header-actions {
    @apply tw-w-full tw-justify-start;
  }

  .result-title {
    @apply tw-flex-col tw-items-start tw-space-y-2;
  }

  .document-actions {
    @apply tw-self-end;
  }

  .document-meta {
    @apply tw-flex-col tw-items-start tw-space-y-1;
  }
}

/* Element Plus 组件暗色模式适配 */
.more-btn {
  @apply tw-text-gray-500 dark:tw-text-gray-400 hover:tw-text-gray-700 dark:hover:tw-text-gray-200 tw-transition-colors tw-duration-200;
}

:deep(.el-dropdown-menu) {
  @apply tw-bg-gray-50 dark:tw-bg-gray-700 tw-border dark:tw-border-gray-700 tw-shadow-lg dark:tw-shadow-gray-900/50;
}

:deep(.el-dropdown-menu__item) {
  @apply tw-text-gray-700 dark:tw-text-gray-200 hover:tw-bg-gray-50 dark:hover:tw-bg-gray-700 tw-transition-colors tw-duration-200;
}

:deep(.el-dropdown-menu__item.is-divided) {
  @apply tw-border-t tw-border-gray-200 dark:tw-border-gray-600;
}

.delete-item {
  @apply tw-text-red-600 dark:tw-text-red-400;
}

:deep(.delete-item:hover) {
  @apply tw-bg-red-50 dark:tw-bg-red-900/20 tw-text-red-700 dark:tw-text-red-300;
}

/* Element Plus 标签暗色模式 */
:deep(.el-tag) {
  @apply tw-bg-blue-100 dark:tw-bg-blue-900/30 tw-text-blue-800 dark:tw-text-blue-200 tw-border-blue-200 dark:tw-border-blue-700/50 tw-transition-colors tw-duration-200;
}

/* Element Plus 复选框暗色模式 */
:deep(.el-checkbox) {
  @apply tw-transition-colors tw-duration-200;
}

:deep(.el-checkbox__input.is-checked .el-checkbox__inner) {
  @apply tw-bg-blue-600 dark:tw-bg-blue-500 tw-border-blue-600 dark:tw-border-blue-500;
}

:deep(.el-checkbox__inner) {
  @apply tw-border-gray-300 dark:tw-border-gray-600 tw-bg-white dark:tw-bg-gray-700;
}

:deep(.el-checkbox__label) {
  @apply tw-text-gray-700 dark:tw-text-gray-200;
}

/* Element Plus 空状态暗色模式 */
:deep(.el-empty) {
  @apply tw-text-gray-500 dark:tw-text-gray-400;
}

:deep(.el-empty__description) {
  @apply tw-text-gray-500 dark:tw-text-gray-400;
}

/* 文本截断 */
.line-clamp-2 {
  display: -webkit-box;
  -webkit-line-clamp: 2;
  -webkit-box-orient: vertical;
  overflow: hidden;
}

/* 增强的响应式设计 */
@media (max-width: 640px) {
  .main-content {
    @apply tw-p-2 tw-h-full;
    /* 确保在小屏幕下仍然保持在容器范围内 */
    max-height: 100%;
    overflow-y: auto;
  }

  .content-header {
    @apply tw-p-3 tw-mb-4;
  }

  .content-header h2 {
    @apply tw-text-lg tw-mb-2;
  }

  .header-actions {
    @apply tw-flex-col tw-w-full tw-space-x-0 tw-space-y-2;
  }

  .btn {
    @apply tw-w-full tw-justify-center tw-text-xs tw-py-2;
  }

  .document-item {
    @apply tw-p-3 tw-mb-3;
    /* 优化小屏幕下的间距 */
  }

  .title-text {
    @apply tw-text-base tw-pr-2 tw-leading-tight;
  }

  .result-snippet {
    @apply tw-text-xs tw-leading-relaxed;
  }

  .document-meta {
    @apply tw-text-xs tw-gap-1 tw-mt-2;
  }

  .meta-separator {
    @apply tw-hidden;
  }

  .meta-item {
    @apply tw-bg-gray-100 dark:tw-bg-gray-700 tw-px-2 tw-py-1 tw-rounded tw-text-xs;
  }

  /* 确保操作按钮在小屏幕下可见 */
  .document-actions {
    @apply tw-opacity-100;
  }
}

/* 动画增强 */
@keyframes fadeInUp {
  from {
    opacity: 0;
    transform: translateY(10px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}

.document-item {
  animation: fadeInUp 0.3s ease-out;
}

.document-item:nth-child(1) {
  animation-delay: 0.1s;
}
.document-item:nth-child(2) {
  animation-delay: 0.2s;
}
.document-item:nth-child(3) {
  animation-delay: 0.3s;
}
.document-item:nth-child(4) {
  animation-delay: 0.4s;
}
.document-item:nth-child(5) {
  animation-delay: 0.5s;
}
</style>
