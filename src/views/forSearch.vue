<!-- views/forSearch.vue -->
<template>
  <div
    class="search-mode tw-min-h-full tw-bg-gradient-to-br tw-duration-300 tw-overflow-y-auto tw-h-screen"
  >
    <div class="tw-container tw-mx-auto">
      <!-- 内容区域包裹层, 提供统一背景 -->
      <div>
        <div class="tw-p-3 sm:tw-p-6 tw-space-y-12">
          <!-- 综合搜索控制面板 -->
          <SearchControlPanel />

          <!-- 搜索结果 -->
          <SearchResults />
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import SearchControlPanel from '@/components/search/SearchControlPanel.vue'
import SearchResults from '@/components/search/SearchResults.vue'
</script>

<style scoped>
/*
  全局深度选择器，用于修复 Element Plus 组件在暗色模式下的样式问题。
  这些样式仅在此视图加载时应用。
*/
.dark .search-view-container {
  /* el-select 下拉菜单 */
  --el-select-dropdown-bg-color: theme('colors.gray.800');
  --el-select-dropdown-border-color: theme('colors.gray.700');
}

.dark .el-select-dropdown__item {
  color: theme('colors.gray.700');
}

.dark .el-select-dropdown__item.hover,
.dark .el-select-dropdown__item:hover {
  background-color: theme('colors.gray.700');
  color: theme('colors.gray.100');
}

.dark .el-select-dropdown__item.selected {
  background-color: theme('colors.blue.900/30');
  color: theme('colors.blue.300');
  font-weight: 600;
}

/* el-input 和 el-textarea */
.dark .el-input__wrapper,
.dark .el-textarea__inner {
  background-color: theme('colors.gray.700/50') !important;
  border-color: theme('colors.gray.600/50') !important;
  color: theme('colors.gray.100') !important;
  box-shadow: 0 1px 2px 0 rgba(0, 0, 0, 0.2) !important;
}

.dark .el-input__wrapper.is-focus,
.dark .el-textarea__inner:focus {
  border-color: theme('colors.blue.500') !important;
  box-shadow: 0 0 0 1px theme('colors.blue.500') !important;
}

.dark .el-input__inner::placeholder,
.dark .el-textarea__inner::placeholder {
  color: theme('colors.gray.400') !important;
}

/* el-popper (用于下拉菜单) */
.dark .el-popper {
  border-color: theme('colors.gray.700') !important;
  background-color: theme('colors.gray.800') !important;
}

.dark .el-popper .el-popper__arrow::before {
  background: theme('colors.gray.800') !important;
  border-color: theme('colors.gray.700') !important;
}
</style>
