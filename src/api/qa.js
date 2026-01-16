import axios from 'axios' // 假设项目使用axios

const apiClient = axios.create({
  baseURL: import.meta.env.VITE_API_BASE_URL || '/api',
})

// 获取模型列表
export const getModels = async () => {
  try {
    const response = await apiClient.get('/enhanced/models')
    // 后端返回直接的模型数组 [{ "name": "qwen:1.8b" }]
    // 我们需要转换成 { id: 'qwen:1.8b', name: 'qwen:1.8b' } 的格式
    return response.data.map((model) => ({
      id: model.name,
      name: model.name,
    }))
  } catch (error) {
    console.error('Error fetching models:', error)
    return [] // 出错时返回空数组
  }
}

// 发起聊天请求 (注意：这里不直接调用，而是返回一个可用于EventSource的URL)
export const getChatResponseURL = () => {
  const baseURL = import.meta.env.VITE_API_BASE_URL || '/api'
  return `${baseURL}/enhanced/enhanced_stream` // 使用增强版聊天路由
}
