import { defineStore } from 'pinia'
import { ref } from 'vue'
import { getHistoryList, loadHistorySession, saveHistorySession } from '@/api/history.js'
import { getModels } from '@/api/qa.js'

export const useChatStore = defineStore('chat', () => {
  // 状态定义
  const messages = ref([])
  const historyList = ref([])
  const models = ref([])
  const selectedModel = ref(null)
  const isLoading = ref(false)
  const error = ref(null)
  const currentSessionId = ref(null)

  // 获取模型列表
  async function fetchModels() {
    error.value = null
    try {
      models.value = await getModels()
      if (models.value.length > 0) {
        selectedModel.value = models.value[0]
      }
    } catch (e) {
      error.value = e.message
      console.error(e)
    }
  }

  // 获取聊天历史
  async function fetchHistoryList() {
    error.value = null
    try {
      historyList.value = await getHistoryList()
    } catch (e) {
      error.value = e.message
      console.error(e)
    }
  }

  // 加载会话
  async function loadSession(sessionId) {
    if (!sessionId) return
    isLoading.value = true
    error.value = null

    try {
      const sessionData = await loadHistorySession(sessionId)
      messages.value = sessionData
      currentSessionId.value = sessionId
    } catch (e) {
      error.value = e.message
      console.error(e)
    } finally {
      isLoading.value = false
    }
  }

  // 发送消息
  async function sendMessage(prompt, modelId) {
    if (!prompt || isLoading.value || !modelId) return
    isLoading.value = true
    error.value = null

    try {
      // 创建用户消息
      const userMessage = {
        id: Date.now().toString(),
        role: 'user',
        content: prompt,
      }

      // 添加用户消息到消息列表
      messages.value = [...messages.value, userMessage]

      // 模拟AI回复
      setTimeout(async () => {
        const aiMessage = {
          id: (Date.now() + 1).toString(),
          role: 'assistant',
          content: `这是对"${prompt}"的回复。Vue.js是一个用于构建用户界面的渐进式框架...`,
        }
        messages.value = [...messages.value, aiMessage]

        // 在收到AI回复后，保存会话并刷新历史记录列表

        isLoading.value = false
      }, 1000)
    } catch (e) {
      error.value = e.message
      console.error(e)
      isLoading.value = false
    }
  }

  // 创建新聊天
  async function createNewChat() {
    // 清空当前消息
    messages.value = []
    // 重置当前会话ID
    currentSessionId.value = null
    // 刷新历史记录列表
    await fetchHistoryList()
    // 触发一个自定义事件，让forQA.vue组件来处理创建新会话的逻辑
    window.dispatchEvent(new CustomEvent('createNewSession'))
  }

  // 保存当前会话
  async function saveCurrentSession() {
    if (messages.value.length === 0) {
      // 如果没有消息，不需要保存
      console.log('ChatStore: 没有消息需要保存')
      return
    }

    console.log(`ChatStore: 准备保存 ${messages.value.length} 条消息`)

    try {
      // 确保消息包含思考链数据，以兼容后端历史服务
      const messagesWithThinkingData = messages.value.map((msg, index) => {
        console.log(`ChatStore: 消息 ${index} - role: ${msg.role}, content长度: ${msg.content?.length || 0}, thinkingData长度: ${msg.thinkingData?.length || 0}`)

        // 如果消息不包含thinkingData字段，创建一个空数组
        if (!msg.hasOwnProperty('thinkingData')) {
          const updatedMsg = {
            ...msg,
            thinkingData: msg.thinkingData || []
          }
          console.log(`ChatStore: 消息 ${index} 未包含thinkingData，已添加空数组`)
          return updatedMsg
        }
        return msg
      })

      // 调用API保存当前会话
      console.log(`ChatStore: 调用API保存 ${messagesWithThinkingData.length} 条消息`)
      const result = await saveHistorySession(messagesWithThinkingData, currentSessionId.value)
      console.log('ChatStore: 会话保存成功，返回ID:', result.session_id)

      // 更新当前会话ID，如果这是一个新会话
      if (result.session_id && !currentSessionId.value) {
        currentSessionId.value = result.session_id
        console.log('ChatStore: 更新当前会话ID为:', currentSessionId.value)
      }

      // 刷新历史记录列表
      await fetchHistoryList()
    } catch (e) {
      console.error('Error saving current session:', e)
      throw e
    }
  }

  // 返回store接口
  return {
    messages,
    historyList,
    models,
    selectedModel,
    isLoading,
    error,
    currentSessionId,
    fetchModels,
    fetchHistoryList,
    loadSession,
    sendMessage,
    createNewChat,
    saveCurrentSession,
  }
})
