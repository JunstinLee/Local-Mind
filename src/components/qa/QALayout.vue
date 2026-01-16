<template>
  <div class="qa-layout" :class="{ 'sidebar-collapsed': isSidebarCollapsed }">
    <!-- 左侧边栏 -->
    <Sidebar />

    <!-- 中央内容区域 -->
    <div ref="mainContent" class="qa-main-content">
      <div class="qa-messages-container">
        <!-- 消息内容区域 -->
        <slot name="messages">
          <!-- 默认消息插槽内容 -->
        </slot>
      </div>
    </div>

    <!-- 底部输入框容器 -->
    <div class="qa-input-container">
      <slot name="input">
        <!-- 问答输入组件插槽 -->
      </slot>
    </div>
  </div>
</template>

<script setup>
import { onMounted, ref, provide, nextTick, computed } from 'vue'
import Sidebar from './ChatSidebar.vue'
import { useUiStore } from '@/stores/modules/ui'
import { useChatStore } from '@/stores/modules/chat'

// 获取store实例
const uiStore = useUiStore()
const chatStore = useChatStore()

// 创建一个ref来引用主内容区域DOM元素
const mainContent = ref(null)

// 计算侧边栏是否折叠
const isSidebarCollapsed = computed(() => uiStore.isSidebarCollapsed)

// 定义滚动到底部的函数
const scrollToBottom = () => {
  // 使用nextTick确保在DOM更新后执行滚动操作
  nextTick(() => {
    const container = mainContent.value // 获取主内容区域的DOM元素
    if (container) {
      // 使用平滑滚动效果滚动到容器底部
      container.scrollTo({
        top: container.scrollHeight,
        behavior: 'smooth',
      })
    }
  })
}

// 使用provide使scrollToBottom函数对子组件可用
provide('scrollToBottom', scrollToBottom)

// 组件挂载时初始化
onMounted(() => {
  // 初始化聊天历史和模型
  chatStore.fetchHistoryList()
  chatStore.fetchModels()
})
</script>
<style scoped>
.qa-layout {
  position: relative;
  height: 100vh;
  background-color: #eee8d5;
  display: block;
}

.qa-main-content {
  position: fixed;
  top: 70px;
  /* 为CompactHeader留出空间 */
  left: 60%;
  /* 水平居中 */
  transform: translateX(-47.5%);
  /* 水平居中 */
  width: 75%;
  /* 与输入框协调 */
  max-width: 80%;
  /* 与输入框协调 */
  bottom: 20px;
  /* 为输入框留出空间 */
  padding: 0;
  /* 移除padding */
  overflow-y: auto;
  overflow-x: hidden;
  scrollbar-width: thin;
  scrollbar-color: var(--el-scrollbar-color) var(--el-scrollbar-bg-color);
  box-sizing: border-box;
  z-index: 10;
  /* 确保高于侧边栏但低于其他弹出层 */
}

/* Webkit浏览器滚动条样式 */
.qa-main-content::-webkit-scrollbar {
  width: 8px;
}

.qa-main-content::-webkit-scrollbar-track {
  background: var(--el-scrollbar-bg-color);
  border-radius: 4px;
}

.qa-main-content::-webkit-scrollbar-thumb {
  background-color: var(--el-scrollbar-color);
  border-radius: 4px;
  border: 2px solid var(--el-scrollbar-bg-color);
}

.qa-main-content::-webkit-scrollbar-thumb:hover {
  background-color: var(--el-scrollbar-color);
  opacity: 0.8;
}

.qa-messages-container {
  width: 100%;
  max-width: 900px;
  height: 100%;

  display: flex;
  flex-direction: column;
  align-items: center;
  overflow: visible;
  /* 继承父容器的滚动 */
  min-width: 0;
}

.qa-input-container {
  position: fixed;
  bottom: 0;
  left: 50%;
  transform: translateX(-50%);
  padding: 0 15px;
  /* 确保内容可以正常滚动 */
  overflow: visible;
}

.qa-input-container {
  position: fixed;
  /* 固定定位 */
  bottom: 0;
  /* 距离底部为0 */
  left: 50%;
  /* 水平居中 */
  transform: translateX(-50%);
  /* 水平居中 */
  width: 65%;
  max-width: 75%;
  padding: 15px 20px;
  /* 内边距 */
  z-index: 100;
  /* z-index */
  background-color: transparent;
  /* 背景色与主内容区域一致 */
}

/* 暗色模式适配 */
html.dark .qa-input-container {}

/* 响应式设计 */
@media (max-width: 768px) {
  .qa-layout {
    display: block;
    padding: 0.5rem;
    overflow: hidden;
  }

  .qa-main-content {
    position: fixed;
    top: 60px;
    left: 50%;
    /* 移动端也保持居中 */
    transform: translateX(-50%);
    /* 移动端居中 */
    right: auto;
    /* 移除right: 0 */
    bottom: 120px;
    width: 90%;
    /* 移动端适当增加宽度 */
    max-width: none;
    padding: 0;
    overflow: hidden;
  }

  .qa-input-container {
    min-height: 120px;
    left: 50%;
    /* 移动端也保持居中 */
    transform: translateX(-50%);
    /* 移动端居中 */
    width: 72%;
    max-width: 75%;
  }
}

/* 大屏幕设备优化 */
@media (min-width: 1025px) {
  .qa-main-content {
    padding: 1.25rem;
    overflow-y: auto;
    overflow-x: hidden;
  }

  .qa-input-container {
    margin-bottom: 0.1rem;
    flex-shrink: 0;
  }
}

/* 暗色模式适配 */
html.dark .qa-layout {
  background-color: #1e1e20;
}
</style>
