<!-- components/search/SearchFilters.vue -->
<template class="tw-bg-white dark:tw-bg-gray-900">
  <!-- Main container with Flexbox layout -->
  <div
    class="tw-flex tw-flex-wrap tw-items-center tw-justify-between tw-gap-x-8 tw-gap-y-2 tw-bg-white dark:tw-bg-gray-900 tw-p-1"
  >
    <label class="tw-text-[20px] tw-font-semibold tw-flex tw-items-center tw-mr-4"
      >{{ t('filter.title') }}:</label
    >
    <!-- File Type Filter -->
    <div class="filter-item md:tw-w-40">
      <el-select
        v-model="searchStore.selectedFilters.fileType"
        multiple
        collapse-tags
        :max-collapse-tags="2"
        :placeholder="t('filter.fileType')"
        class="filter-select"
      >
        <el-option v-for="type in fileTypes" :key="type" :label="type" :value="type" />
      </el-select>
    </div>

    <!-- Time Range Filter (Existing) -->
    <div class="filter-item md:tw-w-32">
      <el-select
        v-model="searchStore.selectedFilters.dateRange"
        :placeholder="t('filter.timeRange')"
        class="filter-select"
        clearable
      >
        <el-option :label="t('time.allTime')" value="all" />
        <el-option :label="t('time.today')" value="today" />
        <el-option :label="t('time.thisWeek')" value="week" />
        <el-option :label="t('time.thisMonth')" value="month" />
        <el-option :label="t('time.thisYear')" value="year" />
      </el-select>
    </div>

    <!-- Modification Time Filter (New) -->
    <div class="filter-item md:tw-w-32">
      <el-select
        v-model="searchStore.selectedFilters.modifiedDate"
        :placeholder="t('filter.lastUpdate')"
        class="filter-select"
        clearable
      >
        <el-option :label="t('time.anyTime')" value="any" />
        <el-option :label="t('time.within24h')" value="day" />
        <el-option :label="t('time.withinWeek')" value="week" />
        <el-option :label="t('time.withinMonth')" value="month" />
      </el-select>
    </div>

    <!-- File Size Filter (New) -->
    <div class="filter-item md:tw-w-32">
      <el-select
        v-model="searchStore.selectedFilters.fileSize"
        :placeholder="t('filter.fileSize')"
        class="filter-select md:tw-w-100"
        clearable
      >
        <el-option :label="t('common.anySize')" value="any" />
        <el-option label="&lt;1MB" value="s" />
        <el-option label="1MB - 10MB" value="m" />
        <el-option label="&gt; 10MB" value="l" />
      </el-select>
    </div>

    <!-- Relevance Score Filter -->

    <!-- Exclude Keywords Filter -->

    <!-- Reset Button -->
    <el-button @click="resetAllFilters" type="danger" plain>
      <CircleX class="tw-w-5 tw-h-5 tw-mr-2" />
      {{ t('filter.reset') }}
    </el-button>
  </div>
</template>

<script setup>
import { useSearchStore } from '@/stores/modules/search'
import { CircleX } from 'lucide-vue-next'
import { useI18n } from 'vue-i18n'

import { ref } from 'vue'

const { t } = useI18n()

const searchStore = useSearchStore()
const fileTypes = ref(['LOG', 'DOCX', 'TXT', 'MD'])

// 完全重置所有筛选条件的函数
const resetAllFilters = () => {
  // 使用 store 中的 resetFilters 方法来重置筛选条件
  searchStore.resetFilters()

  // 触发搜索以应用重置后的筛选条件
  if (searchStore.searchQuery.trim()) {
    searchStore.performSearch()
  }
}
</script>
