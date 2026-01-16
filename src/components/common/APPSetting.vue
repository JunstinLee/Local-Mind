<template>
  <el-dialog
    v-model="uiStore.isSettingsModalVisible"
    :title="t('settings.title')"
    width="900"
    :before-close="uiStore.hideSettingsModal"
    align-center
    top="5vh"
    :close-on-click-modal="false"
  >
    <div class="tw-h-[400px] tw-max-h-[50vh] tw-overflow-hidden">
      <div class="tw-h-full tw-p-2 tw-overflow-y-auto custom-scrollbar dark:tw-bg-[#1e1e20]">
        <!-- 通用设置 -->
        <div>
          <div class="tw-flex tw-items-center tw-gap-2 tw-mb-6">
            <Brain class="tw-w-5 tw-h-5" />
            <h3 class="tw-text-lg tw-font-semibold">{{ t('settings.general') }}</h3>
          </div>

          <!-- 语言选择 -->
          <div class="tw-p-4 tw-rounded-lg tw-border tw-bg-transparent tw-border-gray-300 tw-mb-6">
            <h4 class="tw-font-medium tw-mb-3 tw-flex tw-items-center tw-gap-2">
              <MessageSquare class="tw-w-4 tw-h-4" />
              {{ t('settings.language') }}
            </h4>
            <div class="tw-flex tw-items-center tw-gap-4">
              <label class="tw-text-sm tw-text-gray-700 dark:tw-text-gray-100 tw-whitespace-nowrap"
                >{{ t('settings.selectLanguage') }}:</label
              >
              <el-select
                v-model="selectedLanguage"
                :placeholder="t('settings.pleaseSelectLanguage')"
                class="tw-w-40"
              >
                <el-option
                  v-for="lang in availableLanguages"
                  :key="lang.value"
                  :label="lang.label"
                  :value="lang.value"
                />
              </el-select>
              <!-- 新增：确定按钮 -->
              <el-button class="tw-ml-2" type="primary" @click="confirmLanguageChange">
                {{ t('settings.confirm') }}
              </el-button>
            </div>
          </div>
        </div>

        <!-- 显示具体信息 -->
        <div
          v-for="tab in TABS"
          :key="tab.id"
          class="tw-p-4 tw-rounded-lg tw-border tw-bg-transparent tw-border-gray-300 tw-mb-6 tw-mt-8"
        >
          <h4 class="tw-font-medium tw-mb-3 tw-flex tw-items-center tw-gap-2">
            <component :is="tab.icon" class="tw-w-4 tw-h-4" />
            {{ tab.name }}
          </h4>
          <div class="tw-space-y-3">
            <div
              v-for="model in documentsStore.models[tab.id]"
              :key="model.name"
              class="tw-flex tw-items-start tw-justify-between tw-py-1"
            >
              <div class="tw-flex-1">
                <div class="tw-flex tw-items-center tw-gap-2">
                  <div class="tw-font-medium tw-text-sm">{{ model.name }}</div>
                  <a
                    v-if="model.sourceUrl"
                    href="#"
                    @click.prevent="openExternalLink(model.sourceUrl)"
                    class="tw-text-xs tw-text-blue-500 hover:tw-text-blue-700 dark:tw-text-blue-400 dark:hover:tw-text-blue-300 tw-underline"
                  >
                    {{ t('settings.modelSourceFrom') }}
                  </a>
                </div>
                <div
                  v-if="model.supportedLanguages || model.parameters || model.contextLength"
                  class="tw-text-sm tw-text-gray-600 dark:tw-text-gray-100 tw-space-y-1 tw-mt-1"
                >
                  <div class="tw-flex tw-flex-wrap tw-gap-x-20">
                    <div v-if="model.Date" class="tw-mb-1">
                      {{ t('settings.releaseDate') }} : {{ model.Date }}
                    </div>

                    <div v-if="model.size" class="tw-mb-1">
                      {{ t('settings.size') }} :{{ model.size }}
                    </div>
                    <div v-if="model.parameters" class="tw-mb-1">
                      {{ t('settings.numParameters') }} : {{ model.parameters }}
                    </div>
                  </div>
                  <div class="tw-flex tw-flex-wrap tw-gap-x-20">
                    <div v-if="model.contextLength" class="tw-mb-1">
                      {{ t('settings.contextLength') }} : {{ model.contextLength }}
                    </div>
                    <div v-if="model.supportedLanguages" class="tw-mb-1">
                      {{ t('settings.supportedLanguages') }} : {{ model.supportedLanguages }}
                    </div>
                  </div>
                </div>
                <div v-if="model.status === 'downloading'" class="tw-mt-2">
                  <el-progress :percentage="model.progress" :format="() => `${model.progress}%`" />
                </div>
              </div>
              <div class="tw-ml-4 tw-flex tw-flex-col tw-justify-center">
                <!-- 状态一：已激活 -->
                <el-button v-if="model.status === 'active'" type="success" size="small" disabled>
                  <Check class="tw-w-3 tw-h-3 tw-mr-1" />
                  {{ t('settings.currentModel') }}
                </el-button>

                <!-- 状态二：已下载，可应用 -->
                <el-button
                  v-else-if="model.status === 'downloaded'"
                  type="primary"
                  size="small"
                  @click="documentsStore.handleModelAction(tab.id, model.name, 'activate')"
                >
                  <Database class="tw-w-3 tw-h-3 tw-mr-1" />
                  {{ t('settings.apply') }}
                </el-button>

                <!-- 状态三：下载中 -->
                <div v-else-if="model.status === 'downloading'">
                  <el-button type="info" size="small" disabled>
                    <Download class="tw-w-3 tw-h-3 tw-mr-1" />
                    {{ t('settings.downloading') }} {{ model.progress }}%
                  </el-button>
                </div>

                <!-- 状态四：未下载 -->
                <el-button
                  v-else
                  type="primary"
                  size="small"
                  plain
                  @click="documentsStore.handleModelAction(tab.id, model.name, 'download')"
                >
                  <Download class="tw-w-3 tw-h-3 tw-mr-1" />
                  {{ t('settings.download') }}
                </el-button>
              </div>
            </div>

            <!-- 显示 Hugging Face 缓存路径 -->
            <div
              class="tw-flex tw-items-center tw-text-sm tw-text-gray-600 dark:tw-text-gray-100 tw-gap-x-5"
            >
              <div class="tw-font-medium tw-mr-2">{{ t('settings.hfCachePath') }}:</div>
              <div class="tw-break-all tw-text-xs tw-flex-1">
                {{ hfCachePath || t('settings.downloading') }}
              </div>
            </div>
          </div>
        </div>
        <div class="tw-p-4 tw-rounded-lg tw-border tw-bg-transparent tw-border-gray-300 tw-mb-6 tw-mt-8">
          <div class="tw-flex tw-items-center tw-gap-4">
            <div class="tw-flex-1">
              <div class="tw-text-base tw-font-medium tw-text-gray-700 dark:tw-text-gray-100">
                {{ t('settings.clearData') }}
              </div>
            </div>
            <el-button
              type="danger"
              size="large"
              class="tw-px-8 tw-py-3 tw-text-base tw-font-semibold"
              :loading="clearingCache"
              @click="handleClearCache"
            >
              {{ t('settings.clearKnowledgeBaseCache') }}
            </el-button>
          </div>
        </div>
      </div>
    </div>
  </el-dialog>
</template>

<script setup>
import { useUiStore } from '@/stores/modules/ui'
import { useDocumentsStore } from '@/stores/modules/documents'
import { ref, reactive, onMounted, nextTick, computed } from 'vue'
import { Brain, Database, MessageSquare, Check, Download } from 'lucide-vue-next'
import { useI18n } from 'vue-i18n'
import axios from 'axios'
import { ElMessageBox, ElMessage } from 'element-plus'
import { clearKnowledgeBaseCache } from '@/api/settings'

const { t, locale } = useI18n() // 获取 locale 对象

// 按照qa.js的形式定义API客户端
const apiClient = axios.create({
  baseURL: import.meta.env.VITE_API_BASE_URL || '/api',
})

const uiStore = useUiStore()
const documentsStore = useDocumentsStore()

// 语言选择相关数据
const availableLanguages = reactive([
  { value: 'zh-CN', label: '简体中文' },
  { value: 'en-US', label: 'English (US)' },
  { value: 'en-UK', label: 'English (UK)' },
])

// 检测用户系统语言并设置默认语言
const getDefaultLanguage = () => {
  // 从 localStorage 获取之前保存的语言设置
  const savedLanguage = localStorage.getItem('locale')
  if (savedLanguage && availableLanguages.some((lang) => lang.value === savedLanguage)) {
    return savedLanguage
  }

  // 检测浏览器语言
  const browserLang = navigator.language || navigator.languages[0]

  // 查找匹配的语言
  for (const lang of availableLanguages) {
    if (browserLang.startsWith(lang.value.split('-')[0])) {
      // 比较语言代码的主要部分，如 'zh', 'en', 'fr'
      return lang.value
    }
  }

  // 如果没有匹配的语言，则默认为英文
  return 'en-US'
}

const selectedLanguage = ref(getDefaultLanguage()) // 默认为用户系统语言，否则为英文

// Hugging Face 缓存路径相关
const hfCachePath = ref('')
const hfCachePathLoading = ref(false)

// 清除知识库缓存相关
const clearingCache = ref(false)

// 模型标签配置
const TABS = computed(() => [
  { id: 'traditional', name: t('settings.embeddingModel'), icon: Database },
])

// 初始化模型数据
const initializeModelData = () => {}

// 在组件初始化时调用
initializeModelData()

// 获取 Hugging Face 缓存路径
const loadHfCachePath = async () => {
  hfCachePathLoading.value = true
  try {
    // 直接使用 API 调用获取 Hugging Face 缓存路径
    const response = await apiClient.post('/file/files/select-folder')
    if (response.data.success) {
      hfCachePath.value = response.data.path
    }
  } catch (error) {
    console.error('获取 Hugging Face 缓存路径失败:', error)
  } finally {
    hfCachePathLoading.value = false
  }
}

// 组件挂载后获取 Hugging Face 缓存路径和模型状态
onMounted(async () => {
  loadHfCachePath()
  await documentsStore.fetchModelStatuses() // 确保每次打开设置弹窗时都能展示最新的模型状态
})

// 打开外部链接的函数
const openExternalLink = async (url) => {
  // 如果是Electron环境，使用electronAPI.openExternal
  if (window.electronAPI && typeof window.electronAPI.openExternal === 'function') {
    try {
      const result = await window.electronAPI.openExternal(url)
      if (!result.success) {
        console.error('Failed to open external URL:', result.error)
        // 如果 Electron API 失败，回退到 window.open
        window.open(url, '_blank', 'noopener,noreferrer')
      }
    } catch (error) {
      console.error('Failed to open external URL:', error)
      // 如果 Electron API 失败，回退到 window.open
      window.open(url, '_blank', 'noopener,noreferrer')
    }
  }
  // 否则尝试使用window.open
  else {
    window.open(url, '_blank', 'noopener,noreferrer')
  }
}

// 确认语言变更的函数
const confirmLanguageChange = async () => {
  // 设置当前语言
  locale.value = selectedLanguage.value

  // 保存语言选择到 localStorage
  try {
    localStorage.setItem('locale', selectedLanguage.value)
  } catch (error) {
    console.error('保存语言设置失败:', error)
  }

  // 等待 DOM 更新
  await nextTick()
}

// 清除知识库缓存的函数
const handleClearCache = async () => {
  try {
    // 显示确认对话框
    await ElMessageBox.confirm(
      t('settings.clearCacheConfirm') || '此操作将清除所有知识库缓存数据，包括向量数据库和元数据。此操作不可恢复，确定要继续吗？',
      t('settings.clearCacheTitle') || '确认清除缓存',
      {
        confirmButtonText: t('settings.confirm') || '确定',
        cancelButtonText: t('settings.cancel') || '取消',
        type: 'warning',
        dangerouslyUseHTMLString: false,
      }
    )

    // 用户确认后执行清除操作
    clearingCache.value = true
    try {
      const result = await clearKnowledgeBaseCache()
      ElMessage.success(
        t('settings.clearCacheSuccess') || '知识库缓存已成功清除',
      )
      console.log('清除缓存结果:', result)
    } catch (error) {
      console.error('清除缓存失败:', error)
      const errorMessage = error.response?.data?.detail || error.message || '清除缓存失败'
      ElMessage.error(
        t('settings.clearCacheError') || `清除缓存失败: ${errorMessage}`
      )
    } finally {
      clearingCache.value = false
    }
  } catch (error) {
    // 用户取消操作
    if (error !== 'cancel') {
      console.error('清除缓存操作出错:', error)
    }
    clearingCache.value = false
  }
}
</script>
