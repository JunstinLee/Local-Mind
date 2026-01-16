<template>
  <!--
    This component uses a prop 'isRecursiveCall' to render in two modes:
    1. Wrapper Mode (isRecursiveCall: false): Renders the main container, header, and loading state. It then kicks off the recursion.
    2. Recursive Mode (isRecursiveCall: true): Renders only the list of files and folders.
  -->

  <!-- 1. Wrapper Mode: Render the full component with header and loading state -->
  <div
    v-if="!isRecursiveCall"
    class="tw-h-full tw-w-full tw-p-4 tw-rounded-lg tw-border tw-border-gray-200 dark:tw-border-gray-700 tw-bg-white dark:tw-bg-[#1e1e20] tw-flex tw-flex-col"
  >
    <!-- Header -->
    <div class="tw-flex tw-items-center tw-justify-between tw-pb-2">
      <h5
        class="tw-text-sm tw-font-medium tw-text-gray-700 dark:tw-text-gray-100 tw-transition-colors"
      >
        {{ t('document.fileListTitle') }}
      </h5>
      <span
        v-if="!isLoading"
        class="tw-text-xs tw-text-gray-500 dark:tw-text-gray-400 tw-transition-colors"
      >
        {{ totalFiles }} {{ t('document.files') }}
      </span>
    </div>

    <!-- Loading State -->
    <div v-if="isLoading" class="tw-flex-1 tw-flex tw-items-center tw-justify-center">
      <div v-loading="true" :element-loading-text="t('document.loadingText')">
        <div class="tw-h-20 tw-w-full"></div>
      </div>
    </div>

    <!-- Tree Content: Kicks off the recursion -->
    <div v-else class="tw-flex-1 tw-space-y-1 tw-min-h-0 tw-overflow-y-auto custom-scrollbar">
      <FileTree :treeData="treeData" :isRecursiveCall="true" />
    </div>
  </div>

  <!-- 2. Recursive Mode: Render only the list for recursive calls -->
  <div v-else class="tw-w-full">
    <div v-for="item in treeData" :key="item.id" class="tw-group">
      <!-- Folder -->
      <div v-if="item.type === 'folder'">
        <div
          class="tw-flex tw-items-center tw-px-2 tw-py-1.5 tw-rounded hover:tw-bg-gray-100 dark:tw-bg-[#1e1e20] tw-cursor-pointer tw-transition-colors"
          @click="toggleFolder(item.id)"
        >
          <ChevronRight
            v-if="!isExpanded(item.id)"
            class="tw-w-3 tw-h-3 tw-mr-1 tw-text-gray-400"
          />
          <ChevronDown v-else class="tw-w-3 tw-h-3 tw-mr-1 tw-text-gray-400" />
          <Folder class="tw-w-4 tw-h-4 tw-mr-2 tw-text-blue-500" />
          <span class="tw-text-sm tw-text-gray-700 dark:tw-text-gray-100 tw-transition-colors">
            {{ item.name }}
          </span>
          <span class="tw-ml-auto tw-text-xs tw-text-gray-400 tw-transition-colors">
            {{ item.file_count }}
          </span>
        </div>

        <!-- Recursive rendering for children -->
        <div
          v-if="isExpanded(item.id) && item.children && item.children.length > 0"
          class="tw-ml-4 tw-pl-3 tw-border-l tw-border-gray-200 dark:tw-border-gray-700"
        >
          <FileTree :treeData="item.children" :isRecursiveCall="true" />
        </div>
      </div>

      <!-- File -->
      <div
        v-else
        class="tw-flex tw-items-center tw-px-2 tw-py-1.5 tw-rounded hover:tw-bg-gray-100 dark:hover:tw-bg-gray-700 tw-cursor-pointer tw-transition-colors"
      >
        <File :class="getFileIcon(item.name)" class="tw-w-4 tw-h-4 tw-mr-2" />
        <span class="tw-text-sm tw-text-gray-600 dark:tw-text-gray-100 tw-transition-colors">
          {{ item.name }}
        </span>
        <span class="tw-ml-auto tw-text-xs tw-text-gray-400 tw-transition-colors">
          {{ item.size }}
        </span>
      </div>
    </div>
  </div>
</template>

<!-- This script block is added to name the component for recursion -->
<script>
export default {
  name: 'FileTree',
}
</script>

<script setup>
import { ref, computed } from 'vue'
import { File, Folder, ChevronRight, ChevronDown } from 'lucide-vue-next'
import { useI18n } from 'vue-i18n'

const { t } = useI18n()

// 1. Define props, including the new isRecursiveCall prop
const props = defineProps({
  treeData: {
    type: Array,
    default: () => [],
  },
  isLoading: {
    type: Boolean,
    default: false,
  },
  isRecursiveCall: {
    type: Boolean,
    default: false,
  },
})

// 2. Local state for file data removed - using props.treeData directly
// 3. Watcher removed

// 4. Folder expansion state (remains local to each instance)
const expandedFolders = ref(new Set())

// 5. UI logic
const totalFiles = computed(() => {
  if (props.isRecursiveCall) return 0 // Only top-level should compute total
  let count = 0
  props.treeData.forEach((item) => {
    if (item.type === 'file') {
      count++
    } else if (item.type === 'folder') {
      count += item.file_count
    }
  })
  return count
})

const toggleFolder = (folderId) => {
  const newExpanded = new Set(expandedFolders.value)
  if (newExpanded.has(folderId)) {
    newExpanded.delete(folderId)
  } else {
    newExpanded.add(folderId)
  }
  expandedFolders.value = newExpanded
}

const isExpanded = (folderId) => {
  return expandedFolders.value.has(folderId)
}

const getFileIcon = (fileName) => {
  const ext = fileName.split('.').pop()?.toLowerCase()
  switch (ext) {
    case 'md':
      return 'tw-text-blue-500'
    case 'pdf':
      return 'tw-text-red-500'
    case 'docx':
    case 'doc':
      return 'tw-text-blue-600'
    case 'sql':
      return 'tw-text-orange-500'
    case 'png':
    case 'jpg':
    case 'jpeg':
      return 'tw-text-green-500'
    case 'txt':
      return 'tw-text-gray-500'
    default:
      return 'tw-text-gray-400'
  }
}
</script>
