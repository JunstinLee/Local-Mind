import axios from 'axios'

const apiClient = axios.create({
  baseURL: import.meta.env.VITE_API_BASE_URL || '/api',
})

// 获取历史记录列表
export const getHistoryList = async () => {
  try {
    const response = await apiClient.get('/history/')
    return response.data
  } catch (error) {
    console.error('Error fetching history list:', error)
    return [] // 出错时返回空数组
  }
}

// 加载特定历史会话
export const loadHistorySession = async (sessionId) => {
  try {
    const response = await apiClient.get(`/history/${sessionId}`)
    return response.data
  } catch (error) {
    console.error(`Error loading history session ${sessionId}:`, error)
    return [] // 出错时返回空数组
  }
}

// 保存历史会话
export const saveHistorySession = async (messages, sessionId = null) => {
  try {
    const response = await apiClient.post('/history/', {
      messages,
      session_id: sessionId,
    })
    return response.data
  } catch (error) {
    console.error('Error saving history session:', error)
    throw error
  }
}

// 清除所有历史记录
export const clearAllHistory = async () => {
  try {
    const response = await apiClient.delete('/history/')
    return response.data
  } catch (error) {
    console.error('Error clearing history:', error)
    throw error
  }
}
