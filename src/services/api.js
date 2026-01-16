import axios from 'axios'

// 创建一个axios实例，并配置基础URL
const apiClient = axios.create({
  baseURL: import.meta.env.VITE_API_BASE_URL || '/api',
  headers: {
    'Content-Type': 'application/json',
  },
})

// 全局错误处理
apiClient.interceptors.response.use(
  (response) => response,
  (error) => {
    console.error('API Error:', {
      url: error.config?.url,
      method: error.config?.method,
      data: error.config?.data,
      status: error.response?.status,
      statusText: error.response?.statusText,
      responseData: error.response?.data,
    })
    const errorMessage =
      error.response?.data?.detail ||
      error.response?.data?.message ||
      error.message ||
      'An unknown error occurred'
    return Promise.reject(new Error(errorMessage))
  },
)

// 导出 apiClient 作为命名导出
export { apiClient as api }

/**

/**
 * [核心上传方法]
 * 批量文件上传，将所有文件打包在一个请求中发送。
 */
export const uploadFileBatch = (files, options = {}) => {
  const { destinationFolder = '.', saveInfo = true, onUploadProgress = null } = options

  const formData = new FormData()
  formData.append('destination_folder', destinationFolder)
  formData.append('save_info', saveInfo.toString())

  for (const file of files) {
    formData.append('files', file)
  }

  const config = {
    headers: { 'Content-Type': 'multipart/form-data' },
    timeout: 300000,
    onUploadProgress,
  }

  return apiClient.post('/file/files/upload', formData, config)
}

/**
 * 加载文件目录树
 */
export const loadFileTree = (options = {}) => {
  return apiClient.post('/filetree/tree/generate', {
    path: '.',
    timestamp: options.timestamp || Date.now(),
  })
}

/**
 * 根据筛选条件加载文件列表
 */
export const loadFileList = ({ basePath, filters = {}, sortBy, sortOrder, timestamp }) => {
  const requestData = {
    base_path: basePath,
    filters: {
      search_term: filters?.searchTerm || '',
      file_types: filters?.fileTypes || [],
    },
    sort_by: sortBy || 'name',
    sort_order: sortOrder || 'asc',
    timestamp: timestamp || Date.now(),
  }
  console.log('发送文件列表请求:', requestData)
  return apiClient.post('/file/files/list', requestData)
}
// 上传路径配置
export const UPLOAD_PATHS = {
  files: 'Docs', // 文件上传路径 - 上传到Docs目录
  folders: '.', // 文件夹上传路径
}

/**
 * [知识库构建]
 * 发送文件路径列表到后端，启动批处理任务并获取任务ID。
 * @param {string[]} filePaths - 要处理的文件的路径数组。
 * @returns {Promise<{job_id: string, message: string}>} 包含任务ID的响应数据。
 */
export const buildKnowledgeBase = (filePaths) => {
  const requestData = {
    file_paths: filePaths,
  }
  // 设置一个较长的超时时间，因为批量处理可能非常耗时
  const config = {
    timeout: 1200000, // 10分钟
  }
  return apiClient.post('/v1/documents/batch-process-and-index', requestData, config)
}

/**
 * 获取指定批处理任务的实时状态。
 * @param {string} jobId - 批处理任务的ID。
 * @returns {Promise<Object>} 包含任务状态、进度和已处理文件结果的响应数据。
 */
export const getBuildStatus = (jobId) => {
  return apiClient.get(`/v1/documents/batch-status/${jobId}`)
}
