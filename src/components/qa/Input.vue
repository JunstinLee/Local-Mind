<!-- components/qa/Input.vue -->
<template>
  <div class="qa-input-container">
    <el-input
      ref="textareaRef"
      v-model="userInput"
      type="textarea"
      :autosize="{ minRows: 1, maxRows: 5 }"
      :placeholder="t('qa.sendMessagePlaceholder')"
      class="qa-textarea"
      @keydown.enter.prevent="handleEnterKey"
    />
    <div class="qa-actions-container">
      <div class="qa-model-selector-container">
        <el-dropdown placement="top-start" trigger="click" popper-class="qa-dropdown-popper">
          <button class="qa-action-button qa-text-button">
            <span>{{ selectedModel ? selectedModel.name : t('qa.selectModel') }}</span>
            <ChevronDown :size="16" />
          </button>
          <template #dropdown>
            <el-dropdown-menu>
              <el-dropdown-item
                v-for="model in models"
                :key="model.id"
                @click="handleModelSelect(model)"
              >
                <span>{{ model.name }}</span>
              </el-dropdown-item>
            </el-dropdown-menu>
          </template>
        </el-dropdown>
      </div>

      <!-- Upload button -->
      <button class="qa-action-button qa-circle-button" @click="sendMessage">
        <ArrowUp :size="20" />
      </button>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import { useI18n } from 'vue-i18n'
import { useUiStore } from '@/stores/modules/ui'
import { ChevronDown, ArrowUp } from 'lucide-vue-next'
import { getModels } from '@/api/qa.js'

const { t } = useI18n()

// 定义emit事件
const emit = defineEmits(['send-message'])

const userInput = ref('')
const textareaRef = ref(null)
const uiStore = useUiStore()

// --- Dropdown Model Selection State ---
const models = ref([])
const selectedModel = ref(null) // 初始为null

onMounted(async () => {
  models.value = await getModels()
  if (models.value.length > 0) {
    selectedModel.value = models.value[0] // 默认选中第一个
  }
})

const handleModelSelect = (model) => {
  selectedModel.value = model
}
// -------------------------------------

// 计算属性：判断用户输入是否为空（去除首尾空格后）
const isInputEmpty = computed(() => userInput.value.trim() === '')

// 发送消息的函数
const sendMessage = () => {
  if (isInputEmpty.value || !selectedModel.value) {
    return
  }
  // 发送事件给父组件，包含消息和模型ID
  emit('send-message', {
    content: userInput.value,
    model: selectedModel.value.id,
  })
  userInput.value = ''
}

// 处理回车键事件的函数
const handleEnterKey = (event) => {
  if (event.shiftKey) {
    // 如果同时按下了 Shift 键，则允许默认行为（换行）
  } else {
    // 否则，调用 sendMessage 方法发送消息
    sendMessage()
  }
}
</script>

<style scoped>
/* --- 1. CSS 变量定义 (组件内部) --- */
.qa-input-container {
  /* 布局与阴影 */
  width: 100%;
  min-width: 600px;
  max-width: 1200px;
  margin: 0 auto;
  border-radius: 1rem; /* rounded-2xl */
  padding: 1rem;
  display: flex;
  flex-direction: column;
  gap: 1rem; /* space-y-4 */
  box-shadow:
    0 20px 25px -5px rgb(0 0 0 / 0.1),
    0 8px 10px -6px rgb(0 0 0 / 0.1); /* shadow-2xl */
  transition: all 0.3s ease;

  /* --- 颜色变量：亮色模式 (默认) --- */
  --bg-container: #f8f8f8; /* 使用Element Plus的主题背景色 */
  --bg-textarea: #f8f8f8; /* 输入框背景色 - 白色 */
  --text-textarea: #3f3f46; /* 输入框文字色 - 锌灰-700 */
  --text-placeholder: #71717a; /* 输入框占位符色 - 锌灰-500 */
  --bg-button: #e4e4e7; /* 按钮背景色 - 锌灰-200 */
  --text-button: #52525b; /* 按钮文字色 - 锌灰-600 */
  --bg-button-hover: #d4d4d8; /* 按钮悬停背景色 - 锌灰-300 */
}

/* --- 颜色变量：深色模式 (覆盖) --- */
html.dark .qa-input-container {
  --bg-container: #27272a; /* 使用Element Plus的主题背景色 */
  --bg-textarea: transparent; /* 输入框背景色 - 透明 */
  --text-textarea: #d4d4d8; /* 输入框文字色 - 锌灰-300 */
  --text-placeholder: #a1a1aa; /* 输入框占位符色 - 锌灰-400 */
  --bg-button: #3f3f46; /* 按钮背景色 - 锌灰-700 */
  --text-button: #a1a1aa; /* 按钮文字色 - 锌灰-400 */
  --bg-button-hover: #52525b; /* 按钮悬停背景色 - 锌灰-600 */
}

/* --- 2. 布局与组件样式应用 --- */

.qa-input-container {
  background-color: var(--bg-container);
}

.qa-textarea :deep(.el-textarea__inner) {
  border: none;
  box-shadow: none;
  font-size: 1.125rem; /* text-lg */
  line-height: 1.75rem;
  padding: 0;
  resize: none;
  background-color: var(--bg-textarea);
  color: var(--text-textarea);
  transition: background-color 0.3s ease;
}

.qa-textarea :deep(.el-textarea__inner::placeholder) {
  color: var(--text-placeholder);
}

.qa-actions-container {
  display: flex;
  justify-content: space-between;
  align-items: center;
  gap: 0.5rem; /* space-x-2 */
}

.qa-model-selector-container {
  display: flex;
  align-items: center;
  justify-content: flex-start;
}

.qa-action-button {
  display: inline-flex;
  align-items: center;
  justify-content: center;
  border: none;
  cursor: pointer;
  font-family: inherit;
  padding: 0.5rem 0.75rem;
  background-color: var(--bg-button);
  color: var(--text-button);
  transition: background-color 0.2s ease;
}

.qa-action-button:hover {
  background-color: var(--bg-button-hover);
}

.qa-text-button {
  border-radius: 9999px; /* rounded-full */
  gap: 0.25rem;
}
.qa-text-button span {
  font-size: 0.875rem;
}

.qa-circle-button {
  border-radius: 50%;
  width: 40px;
  height: 40px;
  padding: 0;
}

/* --- 3. Element Plus 全局下拉菜单样式 --- */
/* Popper 容器: 亮色 */
:global(.qa-dropdown-popper.el-popper) {
  background: #f4f4f5 !important; /* zinc-100 */
  border: 1px solid #e4e4e7 !important; /* zinc-200 */
  border-radius: 0.5rem;
  padding: 0.25rem;
  min-width: 180px;
}
:global(.qa-dropdown-popper.el-popper .el-popper__arrow::before) {
  background: #f4f4f5 !important; /* zinc-100 */
  border-color: #e4e4e7 !important; /* zinc-200 */
}

/* Popper 容器: 暗色 */
:global(html.dark .qa-dropdown-popper.el-popper) {
  background: #3f3f46 !important; /* zinc-700 */
  border: 1px solid #3f3f46 !important; /* zinc-700 */
}
:global(html.dark .qa-dropdown-popper.el-popper .el-popper__arrow::before) {
  background: #3f3f46 !important; /* zinc-700 */
  border-color: #3f3f46 !important; /* zinc-700 */
}

/* Popper 菜单项 */
:global(.qa-dropdown-popper .el-dropdown-menu) {
  padding: 0 !important;
  background: transparent !important;
}

:global(.qa-dropdown-popper .el-dropdown-menu__item) {
  border-radius: 0.375rem;
  padding: 0.5rem 0.75rem;
  margin: 0;
  border: none !important;
  transition:
    background-color 0.2s ease,
    color 0.2s ease;
  /* 亮色默认 */
  background-color: #f4f4f5 !important; /* zinc-100 */
  color: #3f3f46; /* zinc-700 */
}

/* 菜单项悬浮: 亮色 */
:global(.qa-dropdown-popper .el-dropdown-menu__item:hover) {
  background-color: #e4e4e7 !important; /* zinc-200 */
  color: #18181b; /* zinc-900 */
}

/* 菜单项: 暗色 */
:global(html.dark .qa-dropdown-popper .el-dropdown-menu__item) {
  background-color: #3f3f46 !important; /* zinc-700 (与按钮统一) */
  color: #d4d4d8; /* zinc-300 */
}

/* 菜单项悬浮: 暗色 */
:global(html.dark .qa-dropdown-popper .el-dropdown-menu__item:hover) {
  background-color: #52525b !important; /* zinc-600 */
  color: #fafafa; /* zinc-50 */
}
</style>
