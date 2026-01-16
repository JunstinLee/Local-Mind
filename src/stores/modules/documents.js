// stores/documents.js
import { reactive } from 'vue'
import { defineStore } from 'pinia'

import axios from 'axios'

// 显示刷新弹窗的全局方法
const showRefreshModal = (modelName) => {
  if (window.showRefreshModal) {
    window.showRefreshModal(modelName)
  }
}

// 创建API客户端
const apiClient = axios.create({
  baseURL: import.meta.env.VITE_API_BASE_URL || '/api',
})

// 定义完整的模型列表
const MASTER_MODEL_LIST = [
  {
    name: 'Qwen/Qwen3-Embedding-0.6B',
    Date: '2025-5',
    size: '1.19GB',
    supportedLanguages: '100+ Languages',
    parameters: '0.6B',
    contextLength: '32k',
    sourceUrl: 'https://huggingface.co/Qwen/Qwen3-Embedding-0.6B',
  },
  // 可以在这里添加更多模型
]

export const useDocumentsStore = defineStore('documents', () => {
  // 状态 (State)
  const models = reactive({
    traditional: MASTER_MODEL_LIST.map((model) => ({
      ...model,
      status: 'not_downloaded', // 默认状态为未下载
      progress: 0,
    })),
  })

  // 新增获取模型状态的函数
  async function fetchModelStatuses() {
    try {
      // 并行发起两个请求
      const [downloadedListResponse, activeModelResponse] = await Promise.all([
        apiClient.get('/Embedding/EmModel'),
        apiClient.get('/Embedding/active'),
      ])

      const downloadedList = downloadedListResponse.data.map((model) => model.name)
      const activeModelName = activeModelResponse.data.active_model

      // 遍历前端的MASTER_MODEL_LIST，根据后端返回结果更新状态
      models.traditional.forEach((model) => {
        if (model.name === activeModelName && downloadedList.includes(model.name)) {
          // 仅当模型既被设置为激活，又在已下载列表中时，才设为'active'
          model.status = 'active'
        } else if (downloadedList.includes(model.name)) {
          // 如果只是已下载，但不是激活的模型
          model.status = 'downloaded'
        } else {
          // 未下载
          model.status = 'not_downloaded'
        }
        // 重置进度为0，但保持状态
        if (model.status !== 'downloading') {
          model.progress = 0
        }
      })
    } catch (error) {
      console.error('获取模型状态失败:', error)
    }
  }

  // 用于存储轮询定时器和SSE连接的引用
  const downloadPollers = {}

  // 操作 (Actions)
  async function handleModelAction(mode, modelName, action) {
    const model = models[mode].find((m) => m.name === modelName)
    if (model) {
      if (action === 'download') {
        // 在调用 API 前，立即将对应模型的 status 设置为 'downloading'，progress 设置为 0
        model.status = 'downloading'
        model.progress = 0

        try {
          // 调用后端下载API
          await apiClient.post('/Embedding/download', {
            model_name: modelName,
            use_custom_dir: false,
          })

          // 启动进度SSE连接
          startProgressSSE(modelName)
        } catch (error) {
          console.error(`下载模型 ${modelName} 失败:`, error)
          model.status = 'not_downloaded'
          model.progress = 0
        }
      } else if (action === 'activate') {
        try {
          // 调用后端激活API
          const response = await apiClient.post('/Embedding/active', {
            model_name: modelName,
          })

          // 触发全局通知
          // 由于Element Plus的ElNotification需要在组件中使用，这里我们简单地在控制台输出信息
          console.log(response.data.message)
          console.log(response.data.notice)

          // 刷新模型状态
          await fetchModelStatuses()
        } catch (error) {
          console.error(`激活模型 ${modelName} 失败:`, error)
          // 激活失败时可能需要提示用户
        }
      }
    }
  }

  // 获取Hugging Face缓存路径
  async function getHfCachePath() {
    try {
      const response = await apiClient.post('/file/files/select-folder')
      if (response.data.success) {
        console.log('Hugging Face缓存路径:', response.data.path)
        return response.data.path
      } else {
        console.error('获取Hugging Face缓存路径失败:', response.data.message)
        return null
      }
    } catch (error) {
      console.error('获取Hugging Face缓存路径时发生错误:', error)
      return null
    }
  }

  // 启动进度SSE连接
  function startProgressSSE(modelName) {
    // 如果已有连接，先清理
    if (downloadPollers[modelName]) {
      if (downloadPollers[modelName].eventSource) {
        // 如果是SSE连接，关闭它
        downloadPollers[modelName].eventSource.close()
      } else if (downloadPollers[modelName].intervalId) {
        // 如果是轮询，清理它
        clearInterval(downloadPollers[modelName].intervalId)
      }
      delete downloadPollers[modelName]
    }

    // 创建新的SSE连接
    const baseURL = import.meta.env.VITE_API_BASE_URL || '/api'
    const eventSource = new EventSource(`${baseURL}/Embedding/download-progress-sse/${modelName}`)

    eventSource.onmessage = (event) => {
      try {
        const progressData = JSON.parse(event.data)
        const model = models.traditional.find((m) => m.name === modelName)
        if (model) {
          model.progress = progressData.progress

          if (progressData.status === 'completed') {
            model.status = 'downloaded'
            stopProgressSSE(modelName)

            // 显示刷新弹窗
            showRefreshModal(modelName)

            fetchModelStatuses() // 刷新模型状态
          } else if (progressData.status === 'error') {
            model.status = 'not_downloaded'
            stopProgressSSE(modelName)
            console.error('下载错误:', progressData.error)
          }
        }
      } catch (error) {
        console.error('解析SSE消息失败:', error)
      }
    }

    eventSource.onerror = (error) => {
      console.error(`SSE连接错误 for ${modelName}:`, error)
      const model = models.traditional.find((m) => m.name === modelName)
      if (model) {
        model.status = 'not_downloaded'
        stopProgressSSE(modelName)
      }
    }

    // 将SSE连接对象存储到downloadPollers中
    downloadPollers[modelName] = {
      eventSource: eventSource,
    }
  }

  // 停止进度SSE连接
  function stopProgressSSE(modelName) {
    if (downloadPollers[modelName] && downloadPollers[modelName].eventSource) {
      downloadPollers[modelName].eventSource.close()
      delete downloadPollers[modelName]
    }
  }

  // 启动进度轮询（保留作为备选方案）
  function startProgressPolling(modelName) {
    // 如果已有连接，先清理
    if (downloadPollers[modelName]) {
      if (downloadPollers[modelName].eventSource) {
        // 如果是SSE连接，关闭它
        downloadPollers[modelName].eventSource.close()
      } else if (downloadPollers[modelName].intervalId) {
        // 如果是轮询，清理它
        clearInterval(downloadPollers[modelName].intervalId)
      }
      delete downloadPollers[modelName]
    }

    // 创建新的轮询
    downloadPollers[modelName] = {
      intervalId: setInterval(async () => {
        try {
          const response = await apiClient.get(`/Embedding/download-progress/${modelName}`)
          const model = models.traditional.find((m) => m.name === modelName)
          if (model) {
            model.progress = response.data.progress
            if (response.data.status === 'completed') {
              model.status = 'downloaded'
              stopProgressPolling(modelName)
              await fetchModelStatuses() // 刷新模型状态
            } else if (response.data.status === 'error') {
              model.status = 'not_downloaded'
              stopProgressPolling(modelName)
              console.error('下载错误:', response.data.error)
            }
          }
        } catch (error) {
          console.error('获取下载进度失败:', error)
          stopProgressPolling(modelName)
        }
      }, 1000), // 每秒更新一次进度
    }
  }

  // 停止进度轮询
  function stopProgressPolling(modelName) {
    if (downloadPollers[modelName] && downloadPollers[modelName].intervalId) {
      clearInterval(downloadPollers[modelName].intervalId)
      delete downloadPollers[modelName]
    }
  }

  // 在组件卸载时清理所有轮询器和SSE连接
  function stopAllProgressPolling() {
    Object.keys(downloadPollers).forEach((key) => {
      const poller = downloadPollers[key]
      if (poller.eventSource) {
        poller.eventSource.close()
      } else if (poller.intervalId) {
        clearInterval(poller.intervalId)
      }
      delete downloadPollers[key]
    })
  }

  return {
    models,
    handleModelAction,
    getHfCachePath,
    fetchModelStatuses,
    startProgressPolling,
    stopProgressPolling,
    stopAllProgressPolling,
  }
})
