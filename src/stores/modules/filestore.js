import { defineStore } from 'pinia'
import { ref } from 'vue'
import { loadFileList, loadFileTree } from '@/services/api'

export const useFileStore = defineStore('file', () => {
  const fileTree = ref([])
  const isTreeLoading = ref(false)
  // [修复] 变量名从 filelist 修改为 fileList，以匹配组件中的使用
  const fileList = ref([])
  const isListLoading = ref(false)
  // 添加标记，指示是否需要刷新数据（初始加载或文件操作后）
  const needsRefresh = ref(true)
  // 添加筛选条件状态
  const currentFilters = ref({
    searchTerm: '',
    fileTypes: [],
  })

  const fetchFileTree = async () => {
    isTreeLoading.value = true
    try {
      const response = await loadFileTree()
      fileTree.value = response.data.tree
      // 获取成功后，标记为无需刷新
      needsRefresh.value = false
    } catch (error) {
      console.error('Failed to load file tree from store:', error)
      fileTree.value = []
    } finally {
      isTreeLoading.value = false
    }
  }

  const fetchFileList = async (options = {}) => {
    isListLoading.value = true
    try {
      const response = await loadFileList({
        basePath: options.basePath || '.',
        filters: options.filters || currentFilters.value, // 使用当前存储的筛选条件
        sortBy: 'name',
        sortOrder: 'asc',
        // [修复] 参数名从 _timestamp 修改为 timestamp
        timestamp: Date.now(),
      })
      if (response.data && response.data.files) {
        // [修复] 更新正确的变量名
        fileList.value = response.data.files
        // 获取成功后，标记为无需刷新
        needsRefresh.value = false
      } else {
        // [修复] 更新正确的变量名
        fileList.value = []
      }
    } catch (error) {
      console.error('Failed to load file list from store:', error)
      // [修复] 更新正确的变量名
      fileList.value = []
    } finally {
      isListLoading.value = false
    }
  }
  const setUploadData = (uploadResult) => {
    if (uploadResult && uploadResult.success && uploadResult.newTree && uploadResult.newFileList) {
      console.log('📊 [FileStore] Received valid upload data. Updating state directly.')
      fileTree.value = uploadResult.newTree
      // [修复] 更新正确的变量名
      fileList.value = uploadResult.newFileList
      // 文件上传成功后，标记为无需刷新（因为数据已经是最新的）
      needsRefresh.value = true
    } else {
      console.error('❌ [FileStore] Invalid upload data received. Falling back to refetch.')
      // 上传失败时，标记为需要刷新数据
      needsRefresh.value = false
      setTimeout(() => {
        fetchFileTree()
        fetchFileList()
      }, 500)
    }
  }
  
  // 标记需要刷新数据（在某些文件操作后）
  const markNeedsRefresh = () => {
    needsRefresh.value = true
  }
  
  // 更新筛选条件
  const updateFilters = (newFilters) => {
    currentFilters.value = { ...currentFilters.value, ...newFilters }
    // 更新筛选条件后，标记为需要刷新
    needsRefresh.value = true
  }
  
  // 重置筛选条件
  const resetFilters = () => {
    currentFilters.value = {
      searchTerm: '',
      fileTypes: [],
    }
    // 重置筛选条件后，标记为需要刷新
    needsRefresh.value = true
  }
  
  return {
    fileTree,
    isTreeLoading,
    // [修复] 导出正确的变量名
    fileList,
    isListLoading,
    needsRefresh,
    currentFilters,
    fetchFileTree,
    fetchFileList,
    setUploadData,
    markNeedsRefresh,
    updateFilters,
    resetFilters,
  }
})
