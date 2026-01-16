<!-- components/traditional/TraditionalFilter.vue -->
<template>
  <div
    class="tw-px-4 tw-py-b-3 tw-py-2 tw-rounded-lg tw-border tw-border-gray-200 dark:tw-border-gray-700 tw-bg-white dark:tw-bg-[#1e1e20]"
  >
    <div class="tw-flex tw-flex-col tw-gap-1">
      <div class="tw-flex tw-items-center tw-justify-between">
        <h4 class="tw-font-medium tw-flex tw-items-center tw-gap-2">
          <Filter class="tw-w-4 tw-h-4" />
          {{ t('filter.title') }}
        </h4>
        <button
          @click="openModal"
          class="tw-p-1 tw-rounded hover:tw-bg-gray-100 dark:tw-bg-[#1e1e20] tw-transition-colors tw-cursor-pointer"
          :title="t('filter.settings')"
        >
          <span style="font-size: 16px">🔧</span>
        </button>
      </div>

      <!-- 显示已选筛选项 -->
      <div class="tw-flex tw-flex-wrap tw-gap-2">
        <!-- 显示已选的关键词 -->
        <el-tag
          v-if="currentFilters.searchTerm"
          closable
          @close="clearSearchTerm"
          type="primary"
          size="default"
        >
          {{ t('filter.keywords') }} : {{ currentFilters.searchTerm }}
        </el-tag>

        <!-- 显示已选的文件类型 -->
        <el-tag
          v-for="type in currentFilters.fileTypes"
          :key="type"
          closable
          @close="removeFileType(type)"
          type="success"
          size="default"
        >
          {{ t('filter.fileType') }} : {{ type }}
        </el-tag>
      </div>

      <!-- 弹窗 -->
      <el-dialog
        v-model="isModalVisible"
        :title="t('filter.settings')"
        width="600px"
        align-center
        :close-on-click-modal="false"
        style="background-color: var(--el-bg-color)"
      >
        <div class="tw-space-y-6">
          <!-- 搜索关键词 -->
          <div>
            <label
              class="tw-block tw-text-sm tw-font-medium tw-mb-3 tw-text-gray-900 dark:tw-text-gray-100"
            >
              {{ t('filter.keywords') }}
            </label>
            <el-input
              v-model="currentFilters.searchTerm"
              :placeholder="t('filter.keywordsPlaceholder')"
              size="large"
              style="background-color: #e6e8eb !important"
            />
          </div>

          <!-- 文件类型筛选 -->
          <div>
            <label
              class="tw-block tw-text-sm tw-font-medium tw-mb-3 tw-text-gray-900 dark:tw-text-gray-100"
            >
              {{ t('filter.fileType') }}
            </label>
            <div class="tw-flex tw-flex-wrap tw-gap-2">
              <button
                v-for="type in availableFileTypes"
                :key="type"
                @click="toggleFileType(type)"
                :class="[
                  'tw-px-3 tw-py-1.5 tw-text-sm tw-rounded-full tw-border tw-transition-all tw-duration-200',
                  currentFilters.fileTypes.includes(type)
                    ? 'tw-bg-blue-600 tw-text-white tw-border-blue-600 tw-shadow-sm'
                    : 'tw-border-gray-300 tw-text-gray-700 hover:tw-bg-gray-50 dark:tw-border-gray-600 dark:tw-text-gray-300 dark:hover:tw-bg-gray-700',
                ]"
              >
                {{ type }}
              </button>
            </div>
          </div>

          <!-- 其他筛选（为简化，暂时移除，可根据需要加回） -->
        </div>

        <!-- 底部操作按钮 -->
        <template #footer>
          <div class="tw-flex tw-justify-end tw-gap-3">
            <el-button @click="resetFilters" size="large"> {{ t('filter.reset') }} </el-button>
            <el-button type="primary" @click="applyFilters" size="large">
              {{ t('filter.apply') }}
            </el-button>
          </div>
        </template>
      </el-dialog>
    </div>
  </div>
</template>

<script setup>
import { Filter } from 'lucide-vue-next'
import { ref } from 'vue'
import { storeToRefs } from 'pinia'
import { useFileStore } from '@/stores/modules/filestore'
import { useI18n } from 'vue-i18n'

const { t } = useI18n()

// 定义组件要发出的事件
const emit = defineEmits(['filters-changed'])

const fileStore = useFileStore()
const { currentFilters } = storeToRefs(fileStore)

const availableFileTypes = ref(['.pdf', '.docx', '.txt', '.md', '.pdf', '.pptx'])
const isModalVisible = ref(false)

const openModal = () => {
  isModalVisible.value = true
}

// 切换文件类型选择
const toggleFileType = (type) => {
  const index = currentFilters.value.fileTypes.indexOf(type)
  let newFileTypes
  if (index === -1) {
    newFileTypes = [...currentFilters.value.fileTypes, type]
  } else {
    newFileTypes = currentFilters.value.fileTypes.filter((t) => t !== type)
  }
  fileStore.updateFilters({ fileTypes: newFileTypes })
}

const resetFilters = () => {
  fileStore.resetFilters()
  // 重置后也立即应用
  applyFilters()
}

// 清除关键词
const clearSearchTerm = () => {
  fileStore.updateFilters({ searchTerm: '' })
  applyFilters()
}

// 移除文件类型筛选
const removeFileType = (type) => {
  const newFileTypes = currentFilters.value.fileTypes.filter((t) => t !== type)
  fileStore.updateFilters({ fileTypes: newFileTypes })
  applyFilters()
}

const applyFilters = () => {
  // 通过emit将当前筛选条件发送给父组件
  emit('filters-changed', {
    searchTerm: currentFilters.value.searchTerm,
    fileTypes: currentFilters.value.fileTypes,
  })
}
</script>

<style scoped>
/* 样式保持不变 */
button span {
  display: inline-block;
  line-height: 1;
}
:deep(.el-dialog) {
  border-radius: 8px;
}
:deep(.el-dialog__header) {
  margin-right: 0;
  padding: 20px 24px;
  border-bottom: none;
}
:deep(.el-dialog__title) {
  font-size: 18px;
  font-weight: 600;
}
:deep(.el-dialog__body) {
  padding: 24px;
}
:deep(.el-dialog__footer) {
  padding: 16px 24px;
  border-top: none;
}

/* 已选筛选项标签样式 */
:deep(.el-tag) {
  margin-top: 4px;
  margin-bottom: 4px;
}
</style>
