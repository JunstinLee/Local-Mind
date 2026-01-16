<!-- components/search/SearchControlPanel.vue -->
<template>
  <!-- 根容器：整个搜索控制面板 -->
  <div class="search-control-panel">
    <!-- 面板内容器：提供卡片式布局、背景和阴影 -->
    <div class="panel-container">
      <!-- 顶部区域：包含主搜索输入和快捷操作 -->
      <div class="top-section tw-bg-white dark:tw-bg-gray-900">
        <div class="tw-space-y-0">
          <!-- 主搜索输入区域 -->
          <div class="relative">
            <!-- 输入框和按钮的包裹容器 -->
            <div class="main-input-wrapper tw-bg-white dark:tw-bg-gray-900">
              <!-- 使用 flex 布局，允许文本域占据大部分空间 -->
              <div class="tw-flex-1 tw-relative tw-rounded-lg">
                <textarea
                  v-model="searchStore.searchQuery"
                  @keypress.enter.prevent="handleSearch"
                  :placeholder="t('search.aiPrompt')"
                  class="main-textarea tw-text-gray-900 dark:tw-text-gray-100"
                  rows="1"
                ></textarea>
                <!-- 主搜索按钮的容器，使用绝对定位放置在文本域右侧 -->
                <div class="main-search-button-container">
                  <el-button
                    type="primary"
                    @click="handleSearch"
                    :disabled="!searchStore.searchQuery.trim() || searchStore.isSearching"
                    :loading="searchStore.isSearching"
                    circle
                    size="large"
                    class="tw-w-14 tw-h-14 tw-shadow-lg"
                  >
                    <template #icon>
                      <Search class="tw-w-6 tw-h-6" />
                    </template>
                  </el-button>
                </div>
              </div>
            </div>
          </div>

          <!-- 快捷操作按钮区域 -->
          <div class="quick-actions tw-bg-white dark:tw-bg-gray-700">
            <!-- “搜索筛选”按钮已被删除 -->
            <!-- 其他未来的快捷操作可以放在这里 -->
          </div>
        </div>
      </div>

      <!-- 直接渲染 SearchFilters 组件，不再有 v-if -->
      <div
        class="tw-px-6 md:tw-px-2 tw-py-2 tw-bg-white dark:tw-bg-gray-900 tw-flex tw-justify-center tw-rounded-b-2xl"
      >
        <SearchFilters class="search-filters-custom" />
      </div>
    </div>
  </div>
</template>

<script setup>
import { useSearchStore } from '@/stores/modules/search'
import SearchFilters from './SearchFilters.vue'
import { Search } from 'lucide-vue-next'
import { useI18n } from 'vue-i18n'

const { t } = useI18n()

const searchStore = useSearchStore()

const handleSearch = () => {
  if (searchStore.searchQuery.trim() && !searchStore.isSearching) {
    searchStore.performSearch()
  }
}
</script>

<style scoped>
/* --- 现有样式：隐藏文本域滚动条 --- */
textarea::-webkit-scrollbar {
  display: none;
}
textarea {
  -ms-overflow-style: none; /* IE and Edge */
  scrollbar-width: none; /* Firefox */
}

/* 强制定义光标颜色以覆盖默认样式 */
.main-textarea {
  caret-color: #1f2937; /* gray-800 */
}
.dark .main-textarea {
  caret-color: #e5e7eb; /* gray-200 */
}

/* --- 新增样式：从模板中提取的组件样式 --- */

/* 主控制面板根容器 */
.search-control-panel {
  @apply tw-w-full tw-max-w-5xl tw-mx-auto  tw-rounded-lg;
  background-color: transparent;
}

/* 面板卡片样式，定义了背景和边框 */
.panel-container {
  @apply tw-transition-colors tw-duration-300 tw-rounded-2xl tw-overflow-hidden;
  border: 0;
  box-shadow: none;
  background-color: transparent;
}

/* 顶部区域，包含主输入框和操作按钮 */
.top-section {
  @apply tw-p-0 md:tw-p-4;
}

/* 主搜索输入框的外层包裹容器，定义了背景、圆角、阴影和过渡效果 */
.main-input-wrapper {
  @apply tw-relative tw-flex tw-items-center tw-bg-white dark:tw-bg-gray-900  dark:tw-border-gray-600 tw-rounded-lg tw-overflow-hidden tw-transition-colors tw-duration-200 tw-min-h-[60px];
}

/* 主搜索文本域样式 */
.main-textarea {
  @apply tw-w-full tw-px-2 tw-pr-20 tw-bg-transparent tw-border-none tw-outline-none tw-resize-none tw-text-lg tw-leading-tight tw-max-h-40;
}
/* 文本域的占位符颜色 */
.main-textarea::placeholder {
  @apply tw-text-gray-500;
}
/* 暗色模式下文本域的占位符颜色 */
.dark .main-textarea::placeholder {
  @apply tw-text-gray-400;
}

/* 主搜索按钮 (el-button) 的绝对定位容器 */
.main-search-button-container {
  @apply tw-absolute tw-right-4 tw-top-1/2 tw-transform -tw-translate-y-1/2;
}

/* 快捷操作按钮的 flex 容器 */
.quick-actions {
  @apply tw-flex tw-flex-wrap tw-items-center tw-justify-between tw-gap-4  tw-bg-white dark:tw-bg-gray-700;
}

/* 切换按钮 (高级设置/搜索筛选) 的基础样式 */
.toggle-button {
  @apply tw-flex tw-items-center tw-px-4 tw-py-2 tw-rounded-lg tw-border tw-transition-all tw-duration-200;
  /* 默认状态下的颜色 */
  @apply tw-bg-white dark:tw-bg-gray-700 tw-border-gray-300 dark:tw-border-gray-600 tw-text-gray-600 dark:tw-text-gray-300;
}
/* 鼠标悬浮时的背景色变化 */
.toggle-button:hover {
  @apply hover:tw-bg-gray-50 dark:hover:tw-bg-gray-600;
}

/* “高级设置”切换按钮的激活状态样式 */
.toggle-button.advanced--active {
  @apply tw-bg-blue-100 tw-border-blue-300 tw-text-blue-700 dark:tw-bg-blue-900/30 dark:tw-border-blue-700/50 dark:tw-text-blue-300;
}

/* “搜索筛选”切换按钮的激活状态样式 */
.toggle-button.filters--active {
  @apply tw-bg-purple-100 tw-border-purple-300 tw-text-purple-700 dark:tw-bg-purple-900/30 dark:tw-border-purple-700/50 dark:tw-text-purple-300;
}

/* 切换按钮内的下拉图标 */
.toggle-button-chevron {
  @apply tw-w-4 tw-h-4 tw-ml-2 tw-transition-transform tw-duration-200;
}
/* 图标的旋转状态 */
.toggle-button-chevron.rotated {
  @apply tw-rotate-180;
}
</style>
