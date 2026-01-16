<!-- components/search/ResultItem.vue -->
<template>
  <div
    class="result-item tw-bg-white dark:tw-bg-gray-800 tw-p-5 tw-rounded-lg tw-shadow-sm tw-border tw-border-gray-200 dark:tw-border-gray-700 hover:tw-shadow-md dark:hover:tw-shadow-lg hover:tw-border-blue-300 dark:hover:tw-border-blue-500 hover:-tw-translate-y-1 tw-transition-all tw-duration-300 tw-cursor-pointer"
  >
    <!-- 头部：文件名和相关性分数 -->
    <div class="tw-flex tw-items-center tw-justify-between tw-mb-3">
      <div class="tw-flex tw-items-center tw-gap-3 tw-min-w-0">
        <BookOpen class="tw-w-5 tw-h-5 tw-text-blue-600 dark:tw-text-blue-400 tw-flex-shrink-0" />
        <h3
          class="tw-font-semibold tw-text-gray-800 dark:tw-text-gray-100 tw-truncate"
          :title="result.source_file"
        >
          {{ fileName }}
        </h3>
      </div>
      <div
        v-if="result.relevance_score"
        class="tw-flex tw-items-center tw-gap-1 tw-flex-shrink-0 tw-pl-4"
      >
        <Star class="tw-w-4 tw-h-4 tw-text-yellow-500 dark:tw-text-yellow-400" />
        <span class="tw-text-sm tw-font-medium tw-text-gray-700 dark:tw-text-gray-200">
          {{ (result.relevance_score * 100).toFixed(1) }}%
        </span>
      </div>
    </div>

    <!-- 内容预览 -->
    <div
      class="tw-text-gray-600 dark:tw-text-gray-300 tw-text-sm tw-leading-relaxed tw-prose dark:tw-prose-invert max-w-none prose-p:tw-my-1 prose-p:tw-leading-snug"
    >
      <div
        class="line-clamp-3"
        v-html="highlightedContent"
      ></div>
    </div>
    
    <!-- 来源信息 -->
    <div class="tw-mt-2 tw-pt-2 tw-border-t tw-border-gray-200 dark:tw-border-gray-700">
      <p class="tw-text-xs tw-text-gray-500 dark:tw-text-gray-400">
        {{ t('search.source') }}: {{ result.source_file }}
      </p>
    </div>
  </div>
</template>

<script setup>
import { computed } from 'vue'
import { useI18n } from 'vue-i18n'
import { BookOpen, Star } from 'lucide-vue-next'

const { t } = useI18n()

const props = defineProps({
  result: {
    type: Object,
    required: true,
    default: () => ({
      source_file: 'Unknown Document.md',
      heading_trail: 'Introduction -> Overview',
      content: 'This is a sample content snippet. <mark>Highlighting</mark> shows important keywords found in the document.',
      relevance_score: 0.95,
    }),
  },
})

// 提取文件名（不包含路径）
const fileName = computed(() => {
  if (!props.result.source_file) return 'Unknown Document.md'
  // 使用正则表达式匹配路径中的文件名部分，兼容正斜杠和反斜杠
  const pathParts = props.result.source_file.replace(/\\/g, '/').split('/')
  return pathParts[pathParts.length - 1]
})

// 创建带样式的高亮内容
const highlightedContent = computed(() => {
  if (!props.result.content) return ''
  return props.result.content.replace(
    /<mark>(.*?)<\/mark>/g,
    `<mark class="tw-bg-yellow-200 dark:tw-bg-yellow-600/40 tw-px-1 tw-py-0.5 tw-rounded tw-text-gray-900 dark:tw-text-yellow-100 tw-font-medium">$1</mark>`
  )
})
</script>

<style scoped>
/* 文本截断 */
.line-clamp-3 {
  display: -webkit-box;
  -webkit-line-clamp: 3;
  -webkit-box-orient: vertical;
  overflow: hidden;
}

/* 增强 prose 样式以适应暗色模式 */
.dark .tw-prose-invert {
  --tw-prose-body: theme('colors.gray.300');
  --tw-prose-headings: theme('colors.gray.100');
  --tw-prose-lead: theme('colors.gray.400');
  --tw-prose-links: theme('colors.blue.400');
  --tw-prose-bold: theme('colors.white');
  --tw-prose-counters: theme('colors.gray.400');
  --tw-prose-bullets: theme('colors.gray.500');
  --tw-prose-hr: theme('colors.gray.700');
  --tw-prose-quotes: theme('colors.gray.200');
  --tw-prose-quote-borders: theme('colors.gray.600');
  --tw-prose-captions: theme('colors.gray.400');
  --tw-prose-code: theme('colors.pink.300');
  --tw-prose-pre-code: theme('colors.gray.300');
  --tw-prose-pre-bg: theme('colors.gray.800');
  --tw-prose-th-borders: theme('colors.gray.600');
  --tw-prose-td-borders: theme('colors.gray.700');
}

/* 来源信息样式 */
.tw-border-t {
  border-top-width: 1px;
}
</style>
