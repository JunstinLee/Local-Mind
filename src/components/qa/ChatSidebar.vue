<template>
  <aside class="sidebar" :class="{ 'is-collapsed': isCollapsed }">
    <div v-if="!isCollapsed" class="sidebar-expanded">
      <div class="sidebar-header">
        <el-button :icon="ArrowLeft" circle @click="toggleSidebar"></el-button>
      </div>
      <div class="new-chat-section">
        <el-button type="primary" :icon="Plus" size="large" round @click="createNewChat">{{
          t('qa.newChat')
        }}</el-button>
      </div>
      <el-scrollbar>
        <el-menu
          class="chat-history-menu"
          :default-active="chatStore.currentSessionId"
          @select="handleSelect"
        >
          <template v-for="item in chatStore.historyList" :key="item.id || item.title">
            <div v-if="item.type === 'separator'" class="history-separator">
              {{ item.title.replace(/-----/g, '') }}
            </div>
            <el-menu-item v-else-if="item.type === 'session'" :index="item.id">
              <el-icon>
                <ChatDotRound />
              </el-icon>
              <span>{{ item.title }}</span>
            </el-menu-item>
          </template>
        </el-menu>
      </el-scrollbar>
    </div>

    <div v-else class="sidebar-collapsed">
      <div class="collapsed-buttons-wrapper">
        <el-button :icon="ArrowRight" circle @click="toggleSidebar"></el-button>
        <el-button :icon="Plus" circle @click="createNewChat"></el-button>
      </div>
    </div>
  </aside>
</template>

<script setup>
import { computed, onMounted } from 'vue'
import { useUiStore } from '@/stores/modules/ui'
import { useChatStore } from '@/stores/modules/chat'
import { Plus, ArrowLeft, ArrowRight } from '@element-plus/icons-vue'
import { useI18n } from 'vue-i18n'

const { t } = useI18n()

// 获取store实例
const uiStore = useUiStore()
const chatStore = useChatStore()

// 计算属性：控制侧边栏折叠状态
const isCollapsed = computed(() => uiStore.isSidebarCollapsed)

// 组件挂载时获取聊天历史
onMounted(() => {
  chatStore.fetchHistoryList()
  chatStore.fetchModels()
})

// 切换侧边栏状态
const toggleSidebar = () => {
  uiStore.isSidebarCollapsed = !uiStore.isSidebarCollapsed
}

// 创建新聊天
const createNewChat = () => {
  chatStore.createNewChat()
}

// 处理历史记录选择
const handleSelect = async (sessionId) => {
  if (sessionId) {
    try {
      await chatStore.loadSession(sessionId)
      // 成功加载会话后，收起侧边栏以提供更多的消息显示空间
      if (!isCollapsed.value) {
        toggleSidebar()
      }
    } catch (error) {
      console.error('Failed to load session:', error)
    }
  }
}
</script>

<style scoped>
/*
  侧边栏基础样式
  - 宽度为 260px（默认展开状态）
  - 高度占满父容器
  - 使用 Flexbox 垂直排列子元素
  - 背景色为浅灰
  - 移除右侧边框
  - 宽度变化时添加过渡动画
  - 固定定位
  - 设置z-index确保在其他元素之上
*/
.sidebar {
  width: 245px;
  height: 100%;
  display: flex;
  flex-direction: column;
  background-color: #eee8d5;
  border-right: 1px solid #ffffff;
  transition: width 0.3s ease;
  top: 0;
  left: 0;
  z-index: 10; /* 确保高于主内容区域 */
}

/*
  侧边栏折叠状态样式
  - 宽度缩小为 60px
*/
.sidebar.is-collapsed {
  width: 60px;
}

/*
  展开状态下侧边栏内容容器样式
  - 使用 Flexbox 垂直排列
  - 高度占满父容器
*/
.sidebar-expanded {
  display: flex;
  flex-direction: column;
  height: 100%;
}

/*
  侧边栏头部样式
  - 使用 Flexbox 布局，左右对齐
  - 垂直居中对齐
  - 添加内边距和底部边框
*/
.sidebar-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 16px;
  border-bottom: 1px solid #e0e0e0;
}

/*
  用户信息区域样式
  - 使用 Flexbox 水平排列
  - 垂直居中对齐
  - 元素之间有 10px 间距
*/
.user-info {
  display: flex;
  align-items: center;
  gap: 10px;
}

/*
  用户名样式
  - 设置字体大小
*/
.username {
  font-size: 16px;
}

/*
  新建聊天区域样式
  - 添加内边距和底部边框
  - 使用 Flexbox 布局，子元素均匀分布
*/
.new-chat-section {
  padding: 16px;
  border-bottom: 1px solid #e0e0e0;
  display: flex;
  justify-content: space-evenly;
}
.new-chat-section .el-button {
  width: 100%;
  max-width: 200px;
  background-color: #eee8d5;
  color: #333; /* 文字颜色 */
  border: none;
}

html.dark .new-chat-section .el-button {
  width: 100%;
  max-width: 200px;
  background-color: #1e1e20;
  color: #ebe4e4; /* 文字颜色 */
  border: none;
}
/*
  新建聊天按钮样式
  - 宽度占满父容器
  - 最大宽度为 200px（可选）
*/
/*
  折叠状态下侧边栏内容容器样式
  - 使用 Flexbox 垂直排列
  - 水平居中对齐
  - 添加顶部内边距
*/
.sidebar-collapsed {
  display: flex;
  flex-direction: column;
  align-items: center;
  padding-top: 16px;
}

/*
  折叠状态下按钮容器样式
  - 使用 Flexbox 垂直排列
  - 顶部对齐
  - 水平居中对齐
  - 按钮之间有 32px 间距
  - 高度和宽度占满父容器
  - 添加顶部内边距
*/
.collapsed-buttons-wrapper {
  display: flex;
  flex-direction: column;
  justify-content: flex-start;
  align-items: center;
  gap: 32px;
  height: 100%;
  width: 100%;
  padding-top: 16px;
  background-color: #eee8d5; /* 明亮模式背景色 */
}

/*
  折叠状态下按钮样式
  - 宽度和高度为 40px
  - 防止按钮被压缩
  - 移除边框
  - 确保无额外外边距
*/
.collapsed-buttons-wrapper .el-button {
  width: 40px !important;
  height: 40px !important;
  flex-shrink: 0;
  border: none !important;
  margin: 0 !important;
  background-color: #eee8d5 !important; /* 明亮模式背景色 */
  color: #333 !important; /* 明亮模式文字颜色 */
}

/* 暗色模式下的折叠按钮容器样式 */
html.dark .collapsed-buttons-wrapper {
  background-color: #1e1e20; /* 暗色模式背景色 */
}

/* 暗色模式下的折叠按钮样式 */
html.dark .collapsed-buttons-wrapper .el-button {
  background-color: #1e1e20 !important; /* 暗色模式背景色 */
  color: #ccc !important; /* 暗色模式文字颜色 */
}

/*
  聊天历史菜单样式
  - 移除右侧边框
*/
.chat-history-menu {
  border-right: none;
}

/*
  菜单项样式（明暗模式适配）
*/
.chat-history-menu .el-menu-item {
  border-radius: 6px; /* 圆角 */
  margin: 2px 8px; /* 上下间距和左右外边距 */
  transition: background-color 0.2s ease; /* 背景色过渡动画 */
}

/* 明亮模式下的菜单项样式 */
.chat-history-menu .el-menu-item {
  background-color: #eee8d5;
  color: #333; /* 文字颜色 */
}

.chat-history-menu .el-menu-item:hover {
  background-color: #faf8f8; /* 悬停背景色 */
}

.chat-history-menu .el-menu-item.is-active {
  background-color: #d1e7ff; /* 激活项背景色 */
  color: #1677ff; /* 激活项文字颜色 */
}

/*
  历史记录分隔符样式
  - 添加内边距
  - 设置字体大小、颜色和字重
*/
.history-separator {
  padding: 10px 15px 5px;
  font-size: 0.8rem;
  color: #8a8a8e;
  font-weight: 500;
}

/*
  暗色模式适配
  - 侧边栏背景色
  - 侧边栏头部底部边框
  - 新建聊天区域底部边框
  - 历史记录分隔符颜色
  - 菜单项样式
*/
html.dark .sidebar {
  background-color: #1e1e20;
  border-right: 1px solid #303030;
}

html.dark .sidebar-header {
  border-bottom: 1px solid #303030;
}

html.dark .new-chat-section {
  border-bottom: 1px solid #303030;
}

html.dark .history-separator {
  color: #a0a0a0;
}

/* 暗色模式下的菜单项样式（使用 :deep() 穿透 scoped 限制） */
html.dark .chat-history-menu .el-menu-item {
  background-color: #1e1e20;
  color: #ccc; /* 文字颜色 */
}

html.dark .chat-history-menu .el-menu-item:hover {
  background-color: #333; /* 悬停背景色 */
}

html.dark .chat-history-menu .el-menu-item.is-active {
  background-color: #2a3d55; /* 激活项背景色 */
  color: #63a0e0; /* 激活项文字颜色 */
}
.chat-history-menu {
  background-color: #eee8d5; /* 明亮模式 */
}

html.dark .chat-history-menu {
  background-color: #1e1e20; /* 暗色模式 */
}

/* 侧边栏展开状态下的收缩按钮样式 */
.sidebar-header .el-button {
  /* 你可以在这里添加自定义样式 */
  background-color: #eee8d5 !important; /* 明亮模式背景色 */
  border: 1px solid #e0e0e0 !important; /* 边框 */
  color: #333 !important; /* 文字颜色 */
}

/* 暗色模式下的收缩按钮样式 */
html.dark .sidebar-header .el-button {
  background-color: #1e1e20 !important; /* 暗色模式背景色 */
  border: 1px solid #303030 !important; /* 边框 */
  color: #ccc !important; /* 文字颜色 */
}

/* --- Hover Effects --- */

/* 1. 新建聊天按钮(展开状态) */
.new-chat-section .el-button:hover {
  background-color: #e0e0e0;
}

html.dark .new-chat-section .el-button:hover {
  background-color: #333;
}

/* 2. 侧边栏控制按钮(展开/折叠) */
.sidebar-header .el-button:hover,
.collapsed-buttons-wrapper .el-button:hover {
  background-color: #e0e0e0 !important;
}

html.dark .sidebar-header .el-button:hover,
html.dark .collapsed-buttons-wrapper .el-button:hover {
  background-color: #333 !important;
}
</style>
