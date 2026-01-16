<template>
  <el-dialog
    v-model="visible"
    :title="t('refresh.title')"
    width="400px"
    :close-on-click-modal="false"
    :close-on-press-escape="false"
    :show-close="false"
  >
    <div class="tw-text-center tw-py-4">
      <div class="tw-mb-4">
        <Check class="tw-w-12 tw-h-12 tw-text-green-500 tw-mx-auto tw-mb-2" />
        <h3 class="tw-text-lg tw-font-semibold tw-mb-2">
          {{ t('refresh.downloadComplete') }}
        </h3>
        <p class="tw-text-gray-600 dark:tw-text-gray-300">
          {{ t('refresh.modelDownloaded', { modelName }) }}
        </p>
      </div>

      <div class="tw-bg-blue-50 dark:tw-bg-blue-900/20 tw-border tw-border-blue-200 dark:tw-border-blue-800 tw-rounded-lg tw-p-3 tw-mb-4">
        <div class="tw-flex tw-items-center tw-justify-center tw-text-blue-800 dark:tw-text-blue-200">
          <RefreshCw class="tw-w-5 tw-h-5 tw-mr-2" />
          <span class="tw-text-sm">{{ t('refresh.refreshRequired') }}</span>
        </div>
      </div>
    </div>

    <template #footer>
      <div class="tw-flex tw-justify-center">
        <el-button type="primary" size="large" @click="refreshNow">
          <RefreshCw class="tw-w-4 tw-h-4 tw-mr-2" />
          {{ t('refresh.refreshNow') }}
        </el-button>
      </div>
    </template>
  </el-dialog>
</template>

<script setup>
import { ref } from 'vue'
import { Check, RefreshCw } from 'lucide-vue-next'
import { useI18n } from 'vue-i18n'

const { t } = useI18n()

const visible = ref(false)
const modelName = ref('')

const show = (name) => {
  modelName.value = name
  visible.value = true
}

const refreshNow = () => {
  // 强制刷新整个页面
  window.location.reload()
}

defineExpose({
  show
})
</script>