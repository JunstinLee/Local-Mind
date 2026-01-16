// fronted/src/services/BuildBase.js

import { ref, computed } from 'vue'
import { useI18n } from 'vue-i18n'
import { buildKnowledgeBase, getBuildStatus } from './api'

export function useKnowledgeBaseBuilder(filesRef) {
  const { t } = useI18n()
  const isProcessing = ref(false)
  const isFinished = ref(false) // Added status: whether completed
  const isStarting = ref(false)
  const currentJobId = ref(null)
  const startTime = ref(null)
  const remainingTimeSeconds = ref(null)
  let pollIntervalId = null

  const formattedRemainingTime = computed(() => {
    if (remainingTimeSeconds.value === null || remainingTimeSeconds.value < 0) return ''

    const totalSeconds = remainingTimeSeconds.value
    if (totalSeconds < 60) return `${totalSeconds}${t('buildBase.timeUnits.seconds')}`

    const minutes = Math.floor(totalSeconds / 60)
    const seconds = totalSeconds % 60

    if (minutes < 60)
      return `${minutes}${t('buildBase.timeUnits.minutes')} ${seconds}${t('buildBase.timeUnits.seconds')}`

    const hours = Math.floor(minutes / 60)
    const remainingMinutes = minutes % 60
    return `${hours}${t('buildBase.timeUnits.hours')} ${remainingMinutes}${t('buildBase.timeUnits.minutes')} ${seconds}${t('buildBase.timeUnits.seconds')}`
  })

  const resetState = () => {
    isProcessing.value = false
    isStarting.value = false
    isFinished.value = false // Reset completion status
    currentJobId.value = null
    startTime.value = null
    remainingTimeSeconds.value = null
    if (pollIntervalId) {
      clearInterval(pollIntervalId)
      pollIntervalId = null
    }
  }

  const startBuildProcess = async () => {
    if (isProcessing.value) return

    isStarting.value = true
    isFinished.value = false // Reset at start
    startTime.value = Date.now()
    remainingTimeSeconds.value = null

    // Initialize file status
    filesRef.value.forEach((file) => {
      file.status = 'waiting' // All files initial status is waiting
      file.message = t('buildBase.status.waiting')
      file.progress = 0
    })

    const pathsToProcess = filesRef.value.map((file) => file.path)

    try {
      const response = await buildKnowledgeBase(pathsToProcess)
      currentJobId.value = response.data.job_id // Get task ID
      isProcessing.value = true
      isStarting.value = false

      // Start polling
      pollIntervalId = setInterval(async () => {
        try {
          if (!currentJobId.value) return

          const statusResponse = await getBuildStatus(currentJobId.value)
          const jobData = statusResponse.data

          // --- 0. Calculate estimated remaining time ---
          if (jobData.processed > 0 && jobData.total > jobData.processed) {
            const elapsed = (Date.now() - startTime.value) / 1000
            const avgTimePerFile = elapsed / jobData.processed
            const remainingFiles = jobData.total - jobData.processed
            remainingTimeSeconds.value = Math.round(avgTimePerFile * remainingFiles)
          } else if (jobData.status === 'completed') {
            remainingTimeSeconds.value = 0
          }

          // --- 1. Update individual file status ---
          // jobData.results contains the list of processed files
          if (jobData.results && jobData.results.length > 0) {
            jobData.results.forEach((result) => {
              const file = filesRef.value.find((f) => f.path === result.source)
              // Only update if the file hasn't been marked as completed/error/empty
              if (
                file &&
                file.status !== 'completed' &&
                file.status !== 'error' &&
                file.status !== 'empty_file'
              ) {
                // Map backend status to frontend status
                let finalStatus = 'error'
                if (result.status === 'success') finalStatus = 'completed'
                else if (result.status === 'empty_file') finalStatus = 'empty_file'
                else finalStatus = 'error'

                file.status = finalStatus
                file.message =
                  result.message ||
                  (finalStatus === 'completed'
                    ? t('buildBase.status.completed')
                    : t('buildBase.status.failed'))
                file.progress = 100
              }
            })
          }

          // --- 2. Intelligently update "in progress" file status ---
          // Mark the first file still 'waiting' as 'processing' to improve user experience
          // (Optional: if not done, users will see files turn green suddenly without intermediate state)
          const waitingFile = filesRef.value.find((f) => f.status === 'waiting')
          if (waitingFile) {
            waitingFile.status = 'processing'
            waitingFile.message = t('buildBase.status.processing')
            waitingFile.progress = 50 // Simple intermediate state
          }

          // --- 3. Determine if task is completed ---
          if (jobData.status === 'completed') {
            clearInterval(pollIntervalId)
            pollIntervalId = null
            isProcessing.value = false
            isFinished.value = true // Mark as completed

            // Fallback check: if backend says completed, but frontend still has files with unupdated status
            if (jobData.status === 'completed') {
              filesRef.value.forEach((file) => {
                if (file.status === 'processing' || file.status === 'waiting') {
                  // Theoretically should not happen unless backend didn't return results for that file
                  file.status = 'error'
                  file.message = t('buildBase.status.backendError')
                  file.progress = 100
                }
              })
            }
          }
        } catch (error) {
          console.error('获取构建状态轮询失败:', error)
          // Polling failure temporarily does not terminate the entire task unless consecutive failures (simplified handling here)
        }
      }, 1000) // Poll every second
    } catch (error) {
      console.error('启动构建任务失败:', error)
      isStarting.value = false
      isProcessing.value = false
      if (pollIntervalId) {
        clearInterval(pollIntervalId)
        pollIntervalId = null
      }
      // Mark all files as error
      filesRef.value.forEach((file) => {
        file.status = 'error'
        file.message = t('buildBase.status.requestFailed', { error: error.message })
        file.progress = 100
      })
    }
  }

  const overallProgress = computed(() => {
    if (!filesRef.value || filesRef.value.length === 0) return 0

    // Calculate total progress: 100% for completed/failed/empty files + partial progress for in progress files
    const totalProgress = filesRef.value.reduce((acc, file) => {
      return acc + file.progress
    }, 0)

    return totalProgress / filesRef.value.length
  })

  return {
    isProcessing,
    isFinished, // Export completion status
    isStarting,
    overallProgress,
    formattedRemainingTime,
    startBuildProcess,
    resetState,
  }
}
