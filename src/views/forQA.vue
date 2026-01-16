<template>
  <div class="qa-view-container">
    <!-- 嵌入模型加载检测组件 -->
    <EModelCheck @ready="handleBackendReady" />
    
    <!-- 使用新的QALayout组件 -->
    <QALayout>
      <!-- 主消息区域 -->
      <template #messages>
        <MessageList :messages="messages" />
      </template>

      <!-- 左侧面板 - 消息列表 (历史记录) -->
      <!-- 已移至Sidebar组件中 -->
      <template #left-panel> </template>

      <!-- 中央输入区域 -->
      <template #input>
        <div class="input-section">
          <div class="input-header"></div>
          <div class="input-wrapper">
            <Input @send-message="handleSendMessage" />
          </div>
        </div>
      </template>
    </QALayout>
  </div>
</template>

<script setup>
import { ref, onMounted, watch, inject, onUnmounted, computed } from 'vue'
import { useChatStore } from '@/stores/modules/chat'
import { useI18n } from 'vue-i18n' // Import useI18n for locale
import QALayout from '@/components/qa/QALayout.vue'
import Input from '@/components/qa/Input.vue'
import MessageList from '@/components/qa/MessageList.vue' // Import MessageList component
import EModelCheck from '@/components/common/EModelCheck.vue' // 导入嵌入模型检测组件
import { getChatResponseURL } from '@/api/qa.js' // 导入URL获取函数
import { v4 as uuidv4 } from 'uuid' // 导入uuid生成唯一ID

// 获取chatStore实例
const chatStore = useChatStore()

// 获取当前语言设置
const { locale } = useI18n()

// 注入由QALayout提供的滚动到底部函数
const scrollToBottom = inject('scrollToBottom')

// 使用chatStore中的messages作为唯一数据源
const messages = computed(() => chatStore.messages)

// 保存消息数据到localStorage
const saveMessagesToStorage = () => {
  localStorage.setItem('chatMessages', JSON.stringify(chatStore.messages))
}

// 从localStorage加载消息数据
const loadMessagesFromStorage = () => {
  const savedMessages = localStorage.getItem('chatMessages')
  if (savedMessages) {
    chatStore.messages = JSON.parse(savedMessages)
  }
}

// 创建新聊天会话
const createNewSession = () => {
  // 清空当前消息（通过store）
  chatStore.messages = []
  // 清除localStorage中的消息
  localStorage.removeItem('chatMessages')
  // 重置当前会话ID
  chatStore.currentSessionId = null
  // 可以在这里添加其他初始化逻辑
  console.log('New chat session created')
}

// 在组件挂载时加载消息
onMounted(() => {
  loadMessagesFromStorage()
  // 监听createNewSession事件
  window.addEventListener('createNewSession', createNewSession)
})

// 组件卸载时移除事件监听器
onUnmounted(() => {
  window.removeEventListener('createNewSession', createNewSession)
})

// 监听消息变化，当消息更新时滚动到底部
watch(
  () => chatStore.messages,
  () => {
    // 如果scrollToBottom函数存在，则调用它
    if (scrollToBottom) {
      scrollToBottom()
    }
  },
  {
    deep: true, // 深度监听消息数组内部对象的变化
    flush: 'post', // 在DOM更新后执行回调，确保滚动到正确的位置
  },
)

// 后端就绪状态
const isBackendReady = ref(false)

// 处理后端就绪事件
const handleBackendReady = () => {
  isBackendReady.value = true
  console.log('Backend is ready, embedding model loaded')
}

// 在组件中维护会话ID
const conversationId = ref(uuidv4())
const userId = ref('user_' + Date.now()) // 或从用户系统获取

// 如果需要开始新会话，生成新的 conversationId

// 添加一个解码函数
function decodeUnicode(str) {
  try {
    // 使用JSON.parse来解码Unicode转义序列
    return JSON.parse(`"${str}"`)
  } catch (e) {
    // 如果不是有效的Unicode转义序列，返回原字符串
    return str
  }
}

const handleSendMessage = async (payload) => {
  console.log('handleSendMessage called with payload:', payload)
  // 1. 创建并显示用户消息
  const userMessage = {
    id: uuidv4(),
    role: 'user',
    content: payload.content,
    avatar: '/path/to/user/avatar.png', // 请替换为实际用户头像路径
  }
  chatStore.messages.push(userMessage)

  // 2. 准备并显示一个空的AI消息，用于接收流式数据
  const aiMessageId = uuidv4()
  const aiMessage = {
    id: aiMessageId,
    role: 'assistant',
    content: '', // 初始为空
    thinkingData: [''], // 初始化用于流式接收思考过程 (初始化为含有一个空字符串的数组，防止 [0] 访问失败)
    isTyping: true, // 设置打字状态
  }
  console.log('forQA: 添加AI消息到store，ID:', aiMessageId)
  chatStore.messages.push(aiMessage)

  // ... (messageHistory part is the same)
  const messageHistory = chatStore.messages
    .filter((msg) => msg.role && msg.content && msg.id !== userMessage.id && msg.id !== aiMessageId) // 排除当前消息
    .map(({ role, content }) => ({ role, content }))
    .slice(-10) // 限制历史消息数量，避免请求过大

  // 4. 使用fetch API处理流
  fetch(getChatResponseURL(), {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
      Accept: 'text/event-stream',
      'Accept-Language': locale.value, // 传递用户选择的语言
    },
    body: JSON.stringify({
      conversation_id: conversationId.value,
      user_id: userId.value,
      message: payload.content, // 替换 prompt 为 message
      model: payload.model,
      history: messageHistory, // 添加历史消息
      options: {}, // 可选选项
    }),
  })
    .then((response) => {
      const reader = response.body.getReader()
      const decoder = new TextDecoder()
      let buffer = ''

      function push() {
        reader.read().then(({ done, value }) => {
          if (done) {
            console.log('Stream finished.')
            const targetMessage = chatStore.messages.find((m) => m.id === aiMessageId)
            if (targetMessage) {
              targetMessage.isTyping = false
              console.log('forQA: 流完成，AI消息内容长度:', targetMessage.content.length, '思考链长度:', targetMessage.thinkingData[0] ? targetMessage.thinkingData[0].length : 0)
            }

            // 在流完成时，将完整的AI消息（含思考链）发送到后端保存
            // 通过chatStore保存到后端
            saveMessagesToStorage()

            // 保存当前会话到历史记录
            chatStore.saveCurrentSession()
            return
          }

          buffer += decoder.decode(value, { stream: true })
          const lines = buffer.split('\n\n')
          buffer = lines.pop() // The last part might be incomplete

          lines.forEach((line) => {
            if (line.startsWith('data: ')) {
              try {
                const jsonData = JSON.parse(line.substring(6))
                const targetMessage = chatStore.messages.find((m) => m.id === aiMessageId)
                if (targetMessage) {
                  if (jsonData.type === 'thinking_token' && jsonData.token) {
                    // 实时追加思考内容到thinkingData的第一个元素
                    targetMessage.thinkingData[0] += jsonData.token
                    console.log('forQA: 接收到思考链token，当前长度:', targetMessage.thinkingData[0].length)
                  } else if (jsonData.type === 'final_token' && jsonData.token) {
                    // 处理最终的回复内容，并解析Unicode转义序列
                    const decodedToken = decodeUnicode(jsonData.token)
                    targetMessage.content += decodedToken
                    console.log('forQA: 接收到内容token，当前长度:', targetMessage.content.length)
                  } else if (jsonData.type === 'provenance') {
                    targetMessage.provenance = jsonData.data
                    console.log('forQA: 接收到来源信息')
                  } else if (jsonData.type === 'meta') {
                    targetMessage.meta = jsonData.data
                    console.log('forQA: 接收到元数据')
                  } else if (jsonData.type === 'error') {
                    targetMessage.content = `Error: ${jsonData.message}`
                    console.log('forQA: 接收到错误信息:', jsonData.message)
                  }
                }
              } catch (e) {
                console.error('JSON parsing error:', e, 'on line:', line)
              }
            }
          })
          push()
        })
      }
      push()
    })
    .catch((error) => {
      console.error('Fetch stream error:', error)
      const targetMessage = chatStore.messages.find((m) => m.id === aiMessageId)
      if (targetMessage) {
        targetMessage.content = 'Error: Could not connect to the server.'
      }
      // 6. 设置AI输入状态为false
      const errorTargetMessage = chatStore.messages.find((m) => m.id === aiMessageId)
      if (errorTargetMessage) {
        errorTargetMessage.isTyping = false
      }
    })
}
</script>

<style scoped>
.qa-view-container {
  height: 100vh; /* 占满整个视口高度 */
  display: flex;
  flex-direction: column;
}

.input-section {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  text-align: center;
  padding: 0.1rem;
  min-height: 100px;
}

.input-header {
  margin-bottom: 1.5rem;
}

.input-wrapper {
  width: 100%;
  max-width: 1000px; /* 匹配Input组件的max-width */
}

/* 响应式设计 */
@media (max-width: 768px) {
  .input-section {
    padding: 1rem;
    min-height: 100px;
  }

  .input-header {
    margin-bottom: 1rem;
  }

  .input-wrapper {
    max-width: 100%;
  }
}

/* 暗色模式适配 */
</style>
