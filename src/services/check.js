import { api } from './api'

/**
 * 获取未向量化的文件列表
 * @param {Object} options - 请求选项
 * @param {string} options.basePath - 基础路径
 * @param {Object} options.filters - 过滤选项
 * @param {string} options.filters.searchTerm - 搜索关键词
 * @param {Array} options.filters.fileTypes - 文件类型过滤
 * @param {string} options.sortBy - 排序字段
 * @param {string} options.sortOrder - 排序顺序
 * @returns {Promise<Object>} API响应
 */
export const loadUnvectorizedFileList = ({
  basePath,
  filters = {},
  sortBy,
  sortOrder,
  timestamp,
}) => {
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
  console.log('发送未向量化文件列表请求:', requestData)
  return api.post('/file/files/unvectorized_list', requestData)
}
