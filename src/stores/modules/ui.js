import { defineStore } from 'pinia'
import { ref } from 'vue'

export const useUiStore = defineStore('ui', () => {
  // ... 已有的状态 (isDarkMode, isHistoryModalVisible, etc.)
  const isDarkMode = ref(false)
  const isHistoryModalVisible = ref(false)
  const isSettingsModalVisible = ref(false)
  // +++ 新增：侧边栏折叠状态 +++
  const isSidebarCollapsed = ref(false)

  // +++ 新增：通知状态 +++
  const notification = ref({
    show: false,
    message: '',
    type: 'success', // 'success' 或 'error'
  })

  // 安全地从存储中获取主题偏好
  function getThemePreference() {
    try {
      return localStorage.getItem('theme')
    } catch (error) {
      console.warn('无法访问localStorage:', error)
      // 尝试使用sessionStorage作为回退
      try {
        return sessionStorage.getItem('theme')
      } catch (sessionError) {
        console.warn('无法访问sessionStorage:', sessionError)
        return null
      }
    }
  }

  // 安全地保存主题偏好
  function saveThemePreference(theme) {
    try {
      localStorage.setItem('theme', theme)
    } catch (error) {
      console.warn('无法保存主题偏好到localStorage:', error)
      // 使用sessionStorage作为回退
      try {
        sessionStorage.setItem('theme', theme)
      } catch (sessionError) {
        console.warn('无法保存主题偏好到sessionStorage:', sessionError)
      }
    }
  }

  // 安全地保存侧边栏状态
  function saveSidebarState() {
    try {
      localStorage.setItem('sidebarCollapsed', JSON.stringify(isSidebarCollapsed.value))
    } catch (error) {
      console.warn('无法保存侧边栏状态到localStorage:', error)
    }
  }

  // 从存储中加载侧边栏状态
  function loadSidebarState() {
    try {
      const saved = localStorage.getItem('sidebarCollapsed')
      if (saved !== null) {
        isSidebarCollapsed.value = JSON.parse(saved)
      }
    } catch (error) {
      console.warn('无法从localStorage加载侧边栏状态:', error)
    }
  }

  // 初始化主题
  function initTheme() {
    const savedTheme = getThemePreference()
    if (savedTheme) {
      isDarkMode.value = savedTheme === 'dark'
    } else {
      isDarkMode.value = window.matchMedia('(prefers-color-scheme: dark)').matches
    }
    // 移除了 applyTheme() 和事件派发

    // 监听系统主题变化
    window.matchMedia('(prefers-color-scheme: dark)').addEventListener('change', (e) => {
      // 只有在没有手动设置主题时才跟随系统
      if (!getThemePreference()) {
        isDarkMode.value = e.matches
      }
    })
  }

  // 切换主题
  function toggleTheme() {
    isDarkMode.value = !isDarkMode.value
    saveThemePreference(isDarkMode.value ? 'dark' : 'light')
    // 移除了 applyTheme() 和事件派发
  }

  // 切换侧边栏状态
  function toggleSidebar() {
    isSidebarCollapsed.value = !isSidebarCollapsed.value
    saveSidebarState()
  }

  function showSettingsModal() {
    isSettingsModalVisible.value = true
  }

  function hideSettingsModal() {
    isSettingsModalVisible.value = false
  }

  function showHistoryModal() {
    isHistoryModalVisible.value = true
  }

  function hideHistoryModal() {
    isHistoryModalVisible.value = false
  }

  // +++ 新增：显示通知的方法 +++
  const showNotification = ({ message, type = 'success', duration = 3000 }) => {
    notification.value = {
      show: true,
      message,
      type,
    }
    // 在指定时间后自动隐藏
    setTimeout(() => {
      notification.value.show = false
    }, duration)
  }

  // 组件初始化时加载状态
  loadSidebarState()

  return {
    isDarkMode,
    isSettingsModalVisible,
    isHistoryModalVisible,
    isSidebarCollapsed, // 导出侧边栏状态
    initTheme,
    toggleTheme,
    toggleSidebar, // 导出切换侧边栏的方法
    showSettingsModal,
    hideSettingsModal,
    showHistoryModal,
    hideHistoryModal,

    // +++ 新增的导出 +++
    notification,
    showNotification,
  }
})
