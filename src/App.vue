<template>
  <div class="tw-h-screen tw-flex tw-flex-col tw-overflow-hidden">
    <!-- Compact Header -->
    <CompactHeader />

    <!-- Main Content -->
    <main class="tw-flex-1 tw-min-h-0 tw-overflow-hidden">
      <router-view v-slot="{ Component }">
        <keep-alive include="traditional">
          <component :is="Component" />
        </keep-alive>
      </router-view>
    </main>

    <!-- Settings Modal (使用 changeset.vue 作为设置弹窗) -->
    <Changeset />

    <!-- +++ 全局通知组件 +++ -->
    <GlobalNotification />

    <!-- 后端加载进度弹窗 -->
    <LoadingProgressModal v-model="showLoadingModal" @backendReady="onBackendReady" />

    <!-- 刷新弹窗 -->
    <RefreshModal ref="refreshModal" />
  </div>
</template>

<script setup>
import { onMounted, watch, ref, provide } from 'vue'
import CompactHeader from './components/common/CompactHeader.vue'
// 假设我们创建一个 HistoryModal.vue 来处理历史记录弹窗
import { useUiStore } from './stores/modules/ui'
import Changeset from './components/common/APPSetting.vue'
// +++ 导入全局通知组件 +++
import GlobalNotification from './components/common/GlobalNotification.vue'
import LoadingProgressModal from './components/common/LoadingProgressModal.vue'
import RefreshModal from './components/common/RefreshModal.vue'

const uiStore = useUiStore()
const showLoadingModal = ref(true)
const refreshModal = ref(null)

// 提供全局方法供其他组件调用
const showRefreshModal = (modelName) => {
  if (refreshModal.value) {
    refreshModal.value.show(modelName)
  }
}

// 将方法提供给全局
provide('showRefreshModal', showRefreshModal)

// 也可以挂载到window对象上，方便store调用
window.showRefreshModal = showRefreshModal

// 当后端准备就绪时的处理函数
const onBackendReady = () => {
  console.log('后端服务已准备就绪')
  // 可以在这里添加其他逻辑，如自动关闭模态框（通过v-model控制）
  setTimeout(() => {
    showLoadingModal.value = false
  }, 2000) // 2秒后自动关闭
}

// 在组件挂载时从localStorage或系统偏好初始化主题状态
onMounted(() => {
  uiStore.initTheme()
  // 启动时显示加载进度弹窗
  showLoadingModal.value = true
})

// 监听isDarkMode状态，并将其应用到<html>标签
// 这是全应用中唯一一处修改 `<html>` class 的地方
watch(
  () => uiStore.isDarkMode,
  (isDark) => {
    const root = document.documentElement
    if (isDark) {
      root.classList.add('dark')
    } else {
      root.classList.remove('dark')
    }
  },
  {
    immediate: true, // 关键：确保应用加载时立即执行一次，保证初始状态正确
  },
)
</script>
