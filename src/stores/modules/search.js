// stores/modules/search.js
import { defineStore } from 'pinia'
import { ref, computed } from 'vue' // 导入 computed
import { api } from '@/services/api'
export const useSearchStore = defineStore('search', () => {
  // State
  const searchQuery = ref('')
  const searchResults = ref([])
  const isSearching = ref(false)
  const searchError = ref(null)
  const searchMode = ref('speed_priority') // 'speed_priority' or 'accuracy_priority'
  const searchConfig = ref({
    top_k: 30,
  })
  const selectedFilters = ref({
    fileType: [],
    modifiedDate: null,
    fileSize: null,
    dateRange: null, // 添加默认值
  })
  const hasSearched = ref(false) // 新增：跟踪是否已执行过搜索
  const noResultsDueToFilters = ref(false) // 新增：跟踪是否因为筛选条件没有返回结果

  // Getters (computed properties)
  const areFiltersActive = computed(() => {
    const filters = selectedFilters.value
    return (
      (filters.fileType && filters.fileType.length > 0) ||
      (filters.dateRange && filters.dateRange !== 'all') ||
      (filters.modifiedDate && filters.modifiedDate !== 'any') ||
      (filters.fileSize && filters.fileSize !== 'any')
    )
  })

  // Actions
  async function getDocumentCount() {
    try {
      const response = await api.get('/search/count');
      return response.data.count;
    } catch (error) {
      console.error('Failed to get document count:', error);
      throw error;
    }
  }

  async function performSearch() {
    if (!searchQuery.value.trim()) {
      searchResults.value = [];
      hasSearched.value = false; // 如果查询为空，重置状态
      noResultsDueToFilters.value = false; // 重置筛选状态
      return;
    }

    isSearching.value = true;
    searchError.value = null;
    if (!hasSearched.value) {
      hasSearched.value = true; // 在第一次有效搜索时设置为 true
    }

    // 获取文档总数并动态调整 top_k
    let documentCount;
    try {
      documentCount = await getDocumentCount();
      if (documentCount <= 50) {
        searchConfig.value.top_k = documentCount;
      } else {
        searchConfig.value.top_k = 20; // 或其它预设值
      }
    } catch (error) {
      console.error('Failed to get document count, using default top_k:', error);
      // 如果获取文档数失败，可以使用默认值或直接抛出错误
      // 这里选择继续使用当前的 searchConfig.value.top_k 值
    }

    // 构建激活的筛选条件
    const activeFilters = {};
    for (const key in selectedFilters.value) {
      const value = selectedFilters.value[key];
      if (value !== null && value !== undefined && (!Array.isArray(value) || value.length > 0)) {
        activeFilters[key] = value;
      }
    }

    try {
      const payload = {
        query: searchQuery.value,
        n_results: searchConfig.value.top_k,
        filters: Object.keys(activeFilters).length > 0 ? activeFilters : null,
      };
      const response = await api.post('/search/', payload);
      searchResults.value = response.data;

      // 检查是否因为筛选条件没有返回结果
      noResultsDueToFilters.value = response.data.length === 0 && areFiltersActive.value;
    } catch (error) {
      console.error('Search failed:', error);
      searchError.value = '搜索失败，请稍后重试。';
      searchResults.value = [];
      noResultsDueToFilters.value = false; // 发生错误时重置状态
    } finally {
      isSearching.value = false;
    }
  }

  function resetFilters() {
    selectedFilters.value = {
      fileType: [],
      modifiedDate: null,
      fileSize: null,
      dateRange: null, // 改为 null 而不是 'all'
    }
    // 重置筛选状态
    noResultsDueToFilters.value = false
    // 触发一次新的搜索以显示所有结果
    if (hasSearched.value && searchQuery.value.trim()) {
      performSearch()
    }
  }

  // 切换文件类型筛选条件
  function toggleFileTypeFilter(fileType) {
    const currentFilters = selectedFilters.value.fileType
    const index = currentFilters.indexOf(fileType)

    if (index > -1) {
      // 如果已存在，则移除
      selectedFilters.value.fileType = currentFilters.filter((type) => type !== fileType)
    } else {
      // 如果不存在，则添加
      selectedFilters.value.fileType = [...currentFilters, fileType]
    }
  }

  return {
    searchQuery,
    searchResults,
    isSearching,
    searchError,
    searchMode,
    searchConfig,
    selectedFilters,
    toggleFileTypeFilter,
    hasSearched, // 暴露新状态
    areFiltersActive, // 暴露新 getter
    noResultsDueToFilters, // 暴露新状态
    performSearch,
    resetFilters,
  }
})
