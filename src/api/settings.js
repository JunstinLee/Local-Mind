import axios from 'axios'

const apiClient = axios.create({
  baseURL: import.meta.env.VITE_API_BASE_URL || '/api',
})

// 清除知识库缓存
export const clearKnowledgeBaseCache = async () => {
  try {
    const response = await apiClient.delete('/settings/knowledge-base-cache')
    return response.data
  } catch (error) {
    console.error('Error clearing knowledge base cache:', error)
    throw error
  }
}

