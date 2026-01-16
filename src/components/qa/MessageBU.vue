<template>
  <!-- 消息项的根容器，根据消息发送者（用户或AI）应用不同的样式类 -->
  <div class="message-item" :class="messageClass">
    <!-- AI消息模板：当消息角色为 'assistant' 时显示 -->
    <template v-if="message.role === 'assistant'">
      <!-- CHATBOX图片作为AI头像，显示在消息内容的左侧 -->
      <img src="/logo.png" alt="AI Avatar" class="message-avatar chatbox-avatar" />
      <!-- 消息内容包装器，包含发送者名称和消息气泡 -->
      <div class="message-content-wrapper">
        <!-- AI发送者名称，默认为 'AI' -->
        <div class="message-sender">{{ message.name || 'AI' }}</div>
        <!-- 消息气泡，包含实际的消息内容（思考链、文本、图片） -->
        <div class="message-bubble">
          <!-- 思考链独立显示，不受打字状态影响 -->
          <ThinkingChain v-if="
            message.thinkingData && message.thinkingData.length > 0 && message.thinkingData[0]
          " :thinking-data="message.thinkingData" />

          <!-- 正文内容区域 -->
          <div v-if="isTyping || message.content">
            <!-- 如果正在打字且没有内容，显示打字指示器 -->
            <TypingIndicator v-if="isTyping && !message.content" :avatar="message.avatar" />
            <!-- 如果有内容，显示内容 -->
            <div v-if="message.content" class="content-with-provenance">
              <span v-for="(part, index) in processedContent" :key="index" class="content-part">
                <template v-if="part.type === 'provenance'">
                  <span class="provenance-text">{{ part.text }}</span>
                </template>
                <template v-else>
                  <MarkdownRenderer :source="part.text" />
                </template>
              </span>
            </div>
            <!-- 如果消息包含图片URL，则渲染 ImagePreview 组件 -->
            <div v-else-if="message.imageUrl" class="image-container">
              <ImagePreview :src="message.imageUrl" />
            </div>

            <!-- 如果消息包含来源信息，则显示来源信息 -->
            <div v-if="message.provenance" class="provenance-container">
              <details class="provenance-details">
                <summary>来源信息</summary>
                <div class="provenance-list">
                  <div v-for="(item, index) in message.provenance" :key="index" class="provenance-item">
                    <div class="provenance-header">
                      <strong>{{ getDocumentTitle(item) }}</strong>
                      <span class="score">相似度: {{ formatScore(item.score) }}</span>
                    </div>
                    <div class="provenance-content">
                      <p>{{ truncateText(item.snippet, 200) }}</p>
                    </div>
                  </div>
                </div>
              </details>
            </div>
          </div>
          <!-- 操作按钮 -->
          <div v-if="message.content && !isTyping" class="action-buttons">
            <el-button circle :icon="CopyDocument" @click="copyContent(message.content)" title="复制" />
            <el-button circle :icon="Download" @click="saveAs(message.content)" title="另存为" />
          </div>
        </div>
      </div>
    </template>

    <!-- 用户消息模板：当消息角色不为 'assistant' 时显示（通常为 'user'） -->
    <template v-else>
      <!-- 消息内容包装器，包含发送者名称和消息气泡 -->
      <div class="message-content-wrapper">
        <!-- 用户发送者名称，默认为 'You' -->
        <div class="message-sender">{{ message.name || 'You' }}</div>
        <!-- 消息气泡，包含实际的消息内容（思考链、文本、图片） -->
        <div class="message-bubble">
          <!-- 如果消息包含思考链数据，则渲染 ThinkingChain 组件 -->
          <ThinkingChain v-if="message.thinkingData && message.thinkingData.length > 0"
            :thinking-data="message.thinkingData" />
          <!-- 如果消息包含文本内容，则渲染 MarkdownRenderer 组件 -->
          <MarkdownRenderer v-if="message.content" :source="message.content" />
          <!-- 如果消息包含图片URL，则渲染 ImagePreview 组件 -->
          <div v-if="message.imageUrl" class="image-container">
            <ImagePreview :src="message.imageUrl" />
          </div>
        </div>
      </div>
    </template>
  </div>
</template>

<script setup>
import { computed } from 'vue'
import { ElMessage } from 'element-plus'
import { CopyDocument, Download } from '@element-plus/icons-vue'
import ImagePreview from './UI_in_QA/ImagePreview.vue'
import ThinkingChain from './UI_in_QA/ThinkingChain.vue'
import MarkdownRenderer from './UI_in_QA/MarkdownRenderer.vue'
import TypingIndicator from './TypingIndicator.vue'

// 定义组件的props，接收一个message对象作为输入
const props = defineProps({
  message: {
    type: Object,
    required: true, // message对象是必需的
  },
  isTyping: {
    type: Boolean,
    default: false, // 是否显示打字指示器
  },
})

// 根据消息发送者动态计算消息样式类名
// 'is-user' 类应用于用户消息，'is-ai' 类应用于AI消息
const messageClass = computed(() => {
  return {
    'is-user': props.message.role === 'user', // 用户消息样式
    'is-ai': props.message.role === 'assistant', // AI消息样式
  }
})

// 复制内容到剪贴板
const copyContent = async (content) => {
  if (!content) return
  try {
    await navigator.clipboard.writeText(content)
    ElMessage.success('已复制到剪贴板')
  } catch (err) {
    console.error('Failed to copy: ', err)
    ElMessage.error('复制失败')
  }
}

// 将内容另存为文件
const saveAs = (content) => {
  if (!content) return
  const blob = new Blob([content], { type: 'text/markdown;charset=utf-8' })
  const url = URL.createObjectURL(blob)
  const a = document.createElement('a')
  a.href = url
  a.download = 'ai-message.md'
  document.body.appendChild(a)
  a.click()
  document.body.removeChild(a)
  URL.revokeObjectURL(url)
}

// 截断文本以避免过长
const truncateText = (text, maxLength) => {
  if (!text) return ''
  return text.length > maxLength ? text.substring(0, maxLength) + '...' : text
}

// 格式化分数
const formatScore = (score) => {
  if (typeof score === 'number') {
    return (score * 100).toFixed(2) + '%'
  }
  return 'N/A'
}

// 获取文档标题
const getDocumentTitle = (item) => {
  if (item.title) return item.title
  if (item.path) return item.path.split('/').pop().split('\\').pop() // 获取文件名
  return '未知文档'
}

// 处理内容，将Source信息标记为特殊类型
const processContent = (content) => {
  if (!content) return []

  // 正则表达式匹配 [] 内的 Source: 及其后内容
  const regex = /(\[[^\]]*Source:[^\]]*\])/g
  const parts = []
  let lastIndex = 0
  let match

  while ((match = regex.exec(content)) !== null) {
    // 添加匹配前的普通文本
    if (match.index > lastIndex) {
      parts.push({
        type: 'normal',
        text: content.substring(lastIndex, match.index),
      })
    }

    // 添加匹配到的来源信息
    parts.push({
      type: 'provenance',
      text: match[1], // 整个匹配项（包括方括号）
    })

    lastIndex = match.index + match[0].length
  }

  // 添加最后剩余的普通文本
  if (lastIndex < content.length) {
    parts.push({
      type: 'normal',
      text: content.substring(lastIndex),
    })
  }

  return parts
}

// 计算处理后的内容
const processedContent = computed(() => {
  return processContent(props.message.content)
})
</script>

<style scoped>
/*
  消息项基础布局样式
  使用 Flexbox 布局，使头像和内容并排显示
*/
.message-item {
  display: flex;
  /* 启用 Flexbox 布局 */
  margin-bottom: 20px;
  /* 每条消息之间的垂直间距 */
  gap: 12px;
  /* 头像与消息内容之间的水平间距 */
  min-width: 0;
}

/*
  AI 消息样式
  - 内容靠左对齐，头像在左侧
  - 去除左侧边距
*/
.message-item.is-ai {
  justify-content: flex-start;
  /* 内容靠左对齐 */
  flex-direction: row;
  /* 水平排列 */
  margin-left: 0;
  /* 去除左侧边距 */
}

/*
  用户消息样式
  - 内容靠右对齐，头像在右侧
  - 去除右侧边距
*/
.message-item.is-user {
  justify-content: flex-end;
  /* 内容靠右对齐 */
  flex-direction: row;
  /* 水平排列 */
  margin-right: 0;
  /* 去除右侧边距 */
}

/*
  消息头像样式
  确保头像不会被压缩变形
*/
.message-avatar {
  flex-shrink: 0;
  /* 不允许头像被压缩 */
}

/*
  CHATBOX头像图片样式
  - 保持图片比例
  - 应用圆形边框使其看起来像头像
*/
.chatbox-avatar {
  width: 40px;
  height: 40px;
  border-radius: 50%;
  object-fit: cover;
}

/*
  消息内容容器样式
  用于包裹发送者名称和消息气泡
*/
.message-content-wrapper {
  display: flex;
  /* 启用 Flexbox 布局 */
  flex-direction: column;
  /* 垂直排列（发送者名称在上，消息气泡在下） */
  min-width: 0;
  /* 允许内部文本换行 */
}

/*
  消息发送者名称样式
*/
.message-sender {
  font-size: 13px;
  /* 字体大小 */
  color: var(--el-text-color-secondary);
  /* 使用 Element Plus 主题的次要文本颜色 */
  margin-bottom: 4px;
  /* 与下方消息气泡的间距 */
}

/* 消息气泡样式 */
.message-bubble {
  padding: 2px 2px;
  /* 内边距 */
  display: flex;
  /* 启用 Flexbox 布局 */
  flex-direction: column;
  /* 垂直排列内容 */
  justify-content: flex-start;
  /* 内容顶部对齐 */
  align-items: flex-start;
  /* 内容左侧对齐 */
  border-radius: 10px;
  /* 圆角 */
  box-shadow: 0 1px 2px rgba(0, 0, 0, 0.05);
  /* 轻微阴影 */
  word-wrap: break-word;
  /* 自动换行 */
  overflow-wrap: break-word;
  /* 防止内容溢出 */
  max-width: 100%;
  /* 限制消息气泡最大宽度，防止超出容器 */
  width: fit-content;
  /* 宽度随内容自适应 */
  min-width: 0;
}

/*
  AI 消息内容容器样式
  - 内容靠左对齐
*/
.message-item.is-ai .message-content-wrapper {
  align-items: flex-start;
  /* 内容靠左对齐 */
}

/*
  AI 消息发送者名称样式
  - 文本左对齐
*/
.message-item.is-ai .message-sender {
  text-align: flex-start;
  /* 文本左对齐 */
}

/*
  AI 消息气泡样式
  - 使用透明背景色和边框
*/
.message-item.is-ai .message-bubble {
  background-color: transparent;
  /* 透明背景色 */
  border: 1px solid var(--el-border-color-light);
  /* 浅色边框 */
}

html.dark.message-item.is-ai .message-bubble {
  background-color: transparent;
  /* 透明背景色 */
  border: 1px solid var(--el-border-color-light);
  /* 浅色边框 */
}

/*
  用户消息内容容器样式
  - 内容靠右对齐
*/
.message-item.is-user .message-content-wrapper {
  align-items: flex-end;
  /* 内容靠右对齐 */
}

/*
  用户消息发送者名称样式
  - 文本右对齐
*/
.message-item.is-user .message-sender {
  text-align: flex-end;
  /* 文本右对齐 */
}

/*
  用户消息气泡样式
  - 使用主题主色作为背景和边框
*/
.message-item.is-user .message-bubble {
  background-color: var(--el-fill-color-darker);
  color: var(--el-text-color-primary);
  border: 1px solid var(--el-border-color);
}

/*
  用户消息中的链接样式
  - 设置为浅蓝色，提高可读性
*/
.message-item.is-user .message-bubble :deep(.markdown-body a) {
  color: #d1e9ff;
  /* 浅蓝色链接 */
}

/*
  图片容器样式
  - 与上方文本之间留出间距
*/
.image-container {
  margin-top: 8px;
  /* 与文本的间距 */
}

/*
  思考链与正式内容之间的间距
  - 自动添加上边距
*/
.message-bubble>*+* {
  margin-top: 12px;
  /* 相邻元素之间的垂直间距 */
}

/*
  打字指示器样式调整
  - 确保在消息气泡内正确显示
  - 调整与头像的间距
*/
.message-bubble .typing-indicator {
  padding: 8px 0;
}

.message-bubble .typing-avatar {
  width: 24px;
  height: 24px;
}

.message-bubble .typing-dots {
  flex: 1;
}

/*
  确保 Markdown 渲染器内容撑满气泡宽度
*/
.message-bubble :deep(.markdown-body) {
  width: 100%;
  /* 占满容器宽度 */
  max-width: 100%;
  box-sizing: border-box;
}

/* 来源信息文本特殊样式 */
.content-with-provenance {
  width: 100%;
}

.content-part {
  display: inline;
}

.provenance-text {
  color: #409eff;
  /* Element Plus 主蓝色 */
  font-weight: 500;
  padding: 2px 4px;
  border-radius: 4px;
  margin: 0 2px;
  font-size: 0.9em;
  word-break: break-word;
}

/* 确保来源文本在AI消息中保持特定样式 */
.message-item.is-ai .provenance-text {
  color: #409eff;
}

/*
  响应式设计：适配不同电脑屏幕尺寸
  - 为 AI 和用户消息设置不同屏幕宽度下的左右边距
*/

/* 默认大屏（如 4K） */
.message-item.is-ai {
  margin-left: 0;
  /* 去除左边距 */
}

.message-item.is-user {
  margin-right: 0;
  /* 去除右边距 */
}

/* 2560px 及以下 */
@media (max-width: 2559px) {
  .message-item.is-ai {
    margin-left: 0;
    /* 去除左边距 */
  }

  .message-item.is-user {
    margin-right: 0;
    /* 去除右边距 */
  }
}

/* 1920px 及以下 */
@media (max-width: 1919px) {
  .message-item.is-ai {
    margin-left: 0;
    /* 去除左边距 */
  }

  .message-item.is-user {
    margin-right: 0;
    /* 去除右边距 */
  }
}

/* 1366px 及以下 */
@media (max-width: 1365px) {
  .message-item.is-ai {
    margin-left: 0;
    /* 去除左边距 */
  }

  .message-item.is-user {
    margin-right: 0;
    /* 去除右边距 */
  }
}

/* 来源信息样式 */
.provenance-container {
  margin-top: 10px;
  padding: 10px;
  border-radius: 5px;
  background-color: #f8f9fa;
  border: 1px solid #e9ecef;
}

.provenance-details summary {
  cursor: pointer;
  font-weight: bold;
  color: #495057;
  list-style: none;
  padding: 8px;
  margin: -10px -10px 0 -10px;
}

.provenance-details summary::-webkit-details-marker {
  display: none;
}

.provenance-details[open] summary {
  border-bottom: 1px solid #e9ecef;
  margin-bottom: 10px;
  padding-bottom: 8px;
}

.provenance-list {
  max-height: 200px;
  overflow-y: auto;
  padding-right: 5px;
}

.provenance-item {
  margin-bottom: 12px;
  padding: 8px;
  border-radius: 4px;
  background-color: #fff;
  border: 1px solid #dee2e6;
}

.provenance-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 6px;
  font-size: 0.9em;
}

.score {
  background-color: #e9ecef;
  color: #495057;
  padding: 2px 6px;
  border-radius: 12px;
  font-size: 0.8em;
}

.provenance-content {
  font-size: 0.85em;
  color: #6c757d;
}

/* 操作按钮样式 */
.action-buttons {
  display: flex;
  align-items: center;
  gap: 8px;
  margin-top: 8px;
}

.action-buttons .el-button {
  background-color: transparent;
  color: var(--el-text-color-regular);
}

.action-buttons .el-button:hover {
  color: var(--el-color-primary);
}
</style>
