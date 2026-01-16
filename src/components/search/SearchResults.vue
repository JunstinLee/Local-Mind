<!-- components/search/SearchResults.vue -->
<template>
  <div class="search-mode tw-w-full tw-max-w-4xl tw-mx-auto tw-space-y-6 tw-pb-6">
    <div class="search-results">
      <!-- 加载状态 -->
      <div v-if="searchStore.isSearching" class="tw-text-center tw-py-12">
        <div
          class="tw-bg-white dark:tw-bg-gray-800 tw-rounded-xl tw-shadow-lg tw-border tw-border-gray-200 dark:tw-border-gray-900 tw-p-8 tw-inline-block"
        >
          <Loader2
            class="tw-w-8 tw-h-8 tw-animate-spin tw-mx-auto tw-text-blue-600 dark:tw-text-blue-400 tw-mb-4"
          />
          <p class="tw-text-gray-600 dark:tw-text-gray-300">{{ t('search.searching') }}</p>
        </div>
      </div>

      <!-- 结果展示 -->
      <div v-else-if="searchStore.searchResults.length > 0">
        <!-- 搜索元信息 -->
        <div
          class="tw-flex tw-items-center tw-justify-between tw-text-sm tw-text-gray-600 dark:tw-text-gray-400 tw-px-2"
        >
          <div class="tw-flex tw-items-center tw-space-x-4">
            <span
              >{{ t('search.foundResults', { count: searchStore.searchResults.length }) }}
            </span>
          </div>
          <div class="tw-flex tw-items-center tw-text-gray-500">
            <Clock class="tw-w-4 tw-h-4 tw-mr-1" />
            <span>{{ t('time.justNow') }} </span>
          </div>
        </div>

        <!-- 语义搜索说明 -->
        <div class="tw-text-xs tw-text-gray-500 dark:tw-text-gray-400 tw-px-2 tw-mt-1">
          <Info class="tw-w-3 tw-h-3 tw-inline tw-mr-1 tw-align-text-top" />
          {{ t('search.semanticHint') }}
        </div>

        <!-- 结果列表 -->
        <div class="tw-space-y-4">
          <ResultItem
            v-for="(result, index) in searchStore.searchResults"
            :key="index"
            :result="result"
            :style="{ animationDelay: `${index * 100}ms` }"
            class="tw-animate-fade-in-up"
          />
        </div>
      </div>

      <!-- 新增：筛选后无结果状态 -->
      <div
        v-else-if="searchStore.hasSearched && searchStore.noResultsDueToFilters"
        class="tw-text-center tw-py-12"
      >
        <div
          class="tw-bg-white dark:tw-bg-gray-800 tw-rounded-xl tw-shadow-lg tw-border tw-border-gray-200 dark:tw-border-gray-700 tw-p-8 tw-inline-block"
        >
          <FilterX
            class="tw-w-12 tw-h-12 tw-mx-auto tw-text-yellow-500 dark:tw-text-yellow-400 tw-mb-4"
          />
          <h3 class="tw-text-lg tw-font-semibold tw-text-gray-700 dark:tw-text-gray-200 tw-mb-2">
            {{ t('filter.noResults') }}
          </h3>
          <p class="tw-text-gray-500 dark:tw-text-gray-400 tw-mb-4">
            {{ t('filter.adjustPrompt') }}
          </p>
          <el-button type="primary" @click="searchStore.resetFilters" plain>
            <CircleX class="tw-w-4 tw-h-4 tw-mr-2" />
            {{ t('filter.clearAndRetry') }}
          </el-button>
        </div>
      </div>

      <!-- 修改：通用空结果状态 (已搜索但无结果) -->
      <div v-else-if="searchStore.hasSearched" class="tw-text-center tw-py-12">
        <div
          class="tw-bg-white dark:tw-bg-gray-800 tw-rounded-xl tw-shadow-lg tw-border tw-border-gray-200 dark:tw-border-gray-700 tw-p-8 tw-inline-block"
        >
          <Frown
            class="tw-w-12 tw-h-12 tw-mx-auto tw-text-gray-400 dark:tw-text-gray-500 tw-mb-4"
          />
          <h3 class="tw-text-lg tw-font-semibold tw-text-gray-700 dark:tw-text-gray-200 tw-mb-2">
            {{ t('search.noRelatedContent') }}
          </h3>
          <p class="tw-text-gray-500 dark:tw-text-gray-400">
            {{ t('search.tryAgain') }}
          </p>
        </div>
      </div>

      <!-- 原始空状态 (搜索前) -->
      <div v-else class="tw-text-center tw-py-12">
        <div
          class="tw-bg-white dark:tw-bg-gray-800 tw-rounded-xl tw-shadow-lg tw-border tw-border-gray-200 dark:tw-border-gray-700 tw-p-8 tw-inline-block"
        >
          <Search
            class="tw-w-12 tw-h-12 tw-mx-auto tw-text-gray-400 dark:tw-text-gray-500 tw-mb-4"
          />
          <h3 class="tw-text-lg tw-font-semibold tw-text-gray-700 dark:tw-text-gray-200 tw-mb-2">
            {{ t('search.ready') }}
          </h3>
          <p class="tw-text-gray-500 dark:tw-text-gray-400">
            {{ t('search.prompt') }}
          </p>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { useSearchStore } from '@/stores/modules/search'
import ResultItem from './ResultItem.vue'
import { Loader2, Search, Clock, Info, FilterX, Frown } from 'lucide-vue-next'
import { useI18n } from 'vue-i18n'

const { t } = useI18n()

const searchStore = useSearchStore()
</script>

<style scoped>
@keyframes fadeInUp {
  from {
    opacity: 0;
    transform: translateY(20px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}

.tw-animate-fade-in-up {
  animation: fadeInUp 0.5s ease-out forwards;
  opacity: 0;
}
</style>
