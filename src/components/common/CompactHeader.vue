<!-- components/common/CompactHeader.vue -->
<!--
  合并后的紧凑头部组件，整合了原 forHeader.vue 和 TabContainer.vue 的功能
  主要改进：
  1. 将标题和导航标签整合在同一行，减少垂直空间占用
  2. 将操作按钮放置在右上角，与标题和标签在同一水平线上
  3. 调整内边距和间距，使整体布局更紧凑
  4. 使用小尺寸按钮减少占用空间
-->
<template>
  <!-- 头部容器，使用较窄的垂直内边距 (tw-py-3 代替原来的 tw-py-4) -->
  <header class="tw-px-2" style="z-index: 8000">
    <!-- 主要内容容器，使用 flex 布局实现左右对齐 -->
    <div class="tw-flex tw-items-center tw-justify-between">
      <!-- 左侧区域：Logo、标题和导航标签 -->
      <div class="tw-flex tw-items-center tw-gap-6">
        <!-- Logo -->
        <img src="/logo.png" alt="Logo" class="tw-h-10 tw-w-auto" />

        <!-- 标题，使用较小的字体大小 (tw-text-xl 代替原来的 tw-text-2xl) -->
        <h1 class="tw-text-2xl tw-font-bold">{{ t('header.title') }}</h1>

        <!-- 导航标签容器 -->
        <nav class="tw-flex tw-space-x-6">
          <!-- 使用 v-for 循环渲染标签 -->
          <router-link
            v-for="tab in tabs"
            :key="tab.id"
            :to="`/${tab.id}`"
            custom
            v-slot="{ href, navigate, isActive }"
          >
            <!-- 标签链接，使用较小的垂直内边距 (tw-py-2 代替原来的 tw-py-4) -->
            <a
              :href="href"
              @click="navigate"
              :class="[
                'tw-flex tw-items-center tw-gap-1.5 tw-px-3 tw-py-4 tw-font-medium tw-text-base tw-transition-all tw-duration-200 tw-rounded-md tw-whitespace-nowrap',
                isActive
                  ? 'tw-text-blue-600 dark:tw-text-blue-400' // 激活状态的样式
                  : 'tw-text-gray-500 hover:tw-text-gray-900 hover:tw-bg-gray-200 dark:tw-text-gray-400 dark:hover:tw-text-gray-100 dark:hover:tw-bg-gray-700', // 默认状态的样式
              ]"
            >
              <!-- 标签图标，使用较小的尺寸 (tw-w-4 tw-h-4) -->
              <component :is="tab.icon" class="tw-w-5 tw-h-5" />
              <!-- 标签文字 -->
              <span>{{ tab.name }}</span>
            </a>
          </router-link>
        </nav>
      </div>

      <!-- 右侧区域：操作按钮 -->
      <div class="tw-flex tw-items-center tw-gap-2">
        <!-- 文件上传按钮，使用小尺寸 -->
        <el-button @click="openFileUpload" size="default" class="header-button">
          <Upload class="tw-w-5 tw-h-5 tw-mr-1" />
          {{ t('header.uploadFiles') }}
        </el-button>

        <!-- 知识库构建按钮，使用小尺寸 -->
        <el-button @click="openFileHandle" size="default" class="header-button">
          <BookKey class="tw-w-5 tw-h-5 tw-mr-1" />
          {{ t('header.buildBase') }}
        </el-button>

        <!-- 主题切换按钮，使用小尺寸 -->
        <el-button
          text
          @click="uiStore.toggleTheme"
          :title="t('header.toggleTheme')"
          size="default"
        >
          <Moon v-if="uiStore.isDarkMode" class="tw-w-6 tw-h-6" />
          <Sun v-else class="tw-w-6 tw-h-6" />
        </el-button>

        <!-- 设置按钮，使用小尺寸 -->
        <el-button
          text
          @click="uiStore.showSettingsModal"
          :title="t('header.settings')"
          size="default"
        >
          <Settings class="tw-w-6 tw-h-6" />
        </el-button>
      </div>
    </div>

    <!-- 文件上传弹窗组件 -->
    <FileUploadModal ref="fileUploadModal" @upload-completed="handleUploadFinished" />

    <!-- 知识库构建进度弹窗组件 -->
    <KnowledgeBuildModal ref="knowledgeBuildModal" />
  </header>
</template>

<script setup>
// 导入必要的 Vue 功能
import { ref, computed } from 'vue'
import { useI18n } from 'vue-i18n'

// 导入状态管理
import { useUiStore } from '@/stores/modules/ui'
import { useFileStore } from '@/stores/modules/filestore'

// 导入图标组件
import { Upload, Moon, Sun, BookKey, Settings } from 'lucide-vue-next'
import { Database, Search, MessageSquare } from 'lucide-vue-next'

// 导入模态框组件
import FileUploadModal from './FileUploadModal.vue'
import KnowledgeBuildModal from './KnowledgeBuildModal.vue'

const { t } = useI18n()

// 初始化状态管理
const uiStore = useUiStore()
const fileStore = useFileStore()

// 模态框引用
const fileUploadModal = ref(null)
const knowledgeBuildModal = ref(null)

// 使用计算属性创建响应式的标签配置
const tabs = computed(() => [
  { id: 'traditional', name: t('header.docs'), icon: Database },
  { id: 'search', name: t('header.search'), icon: Search },
  { id: 'qa', name: t('header.qa'), icon: MessageSquare },
])

// 打开文件上传弹窗的方法
const openFileUpload = () => {
  fileUploadModal.value.openModal()
}

// 打开知识库构建进度弹窗的方法
const openFileHandle = () => {
  knowledgeBuildModal.value.openModal()
}

// 处理文件上传完成事件的方法
const handleUploadFinished = (uploadResult) => {
  console.log(
    '✅ [CompactHeader] Upload finished event received. Calling fileStore to update state.',
  )
  fileStore.setUploadData(uploadResult)

  // +++ 触发全局通知 +++
  if (uploadResult.success) {
    uiStore.showNotification({
      message: t('notification.uploadSuccess'),
      type: 'success',
    })
  } else {
    uiStore.showNotification({
      message: t('notification.uploadFailed', { error: uploadResult.error || '未知错误' }),
      type: 'error',
    })
  }
}
</script>
