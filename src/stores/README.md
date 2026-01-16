# Stores 状态管理模块

本目录包含整个应用的状态管理模块，使用 Pinia 框架实现。这些 store 负责管理应用的全局状态，包括UI状态、聊天数据、文档管理、搜索和文件系统等。

## 文件结构

```
fronted/src/stores/
├── index.js                    # store 根模块（空文件）
├── modules/                    # 各功能模块的 store
│   ├── chat.js                 # 聊天功能状态管理
│   ├── documents.js            # 文档和模型管理状态
│   ├── filestore.js            # 文件系统状态管理
│   ├── search.js               # 搜索功能状态管理
│   └── ui.js                   # UI 相关状态管理
```

## Store 模块功能说明

### 1. ui.js
- **功能**：管理UI相关的全局状态
- **特性**：
  - 主题切换（明暗模式）管理
  - 侧边栏折叠状态管理
  - 模态框显示状态管理（设置、历史记录）
  - 全局通知状态管理
  - 状态持久化到 localStorage
  - 系统主题偏好同步

### 2. chat.js
- **功能**：聊天功能状态管理
- **特性**：
  - 消息列表状态管理
  - 聊天历史记录管理
  - 模型选择状态管理
  - 会话管理（创建、加载、保存）
  - 消息流处理
  - 错误处理和加载状态

### 3. documents.js
- **功能**：文档和模型管理状态
- **特性**：
  - 模型列表管理（传统模式）
  - 模型下载和激活状态管理
  - 模型下载进度跟踪
  - SSE连接管理（用于下载进度）
  - Hugging Face缓存路径管理
  - 模型状态同步

### 4. filestore.js
- **功能**：文件系统状态管理
- **特性**：
  - 文件树结构管理
  - 文件列表管理
  - 文件筛选条件管理
  - 加载状态管理
  - 文件上传结果处理
  - 数据刷新状态管理
  - 异步文件操作处理

### 5. search.js
- **功能**：搜索功能状态管理
- **特性**：
  - 搜索查询状态管理
  - 搜索结果状态管理
  - 搜索配置（优先级、top_k等）
  - 搜索过滤器管理
  - 搜索状态管理（加载、错误）
  - 搜索历史跟踪
  - 过滤器结果状态管理

## 设计原则

1. **单一职责**：每个 store 负责特定功能的状态管理
2. **状态集中**：将相关的状态逻辑集中在一个模块中
3. **异步处理**：统一处理API调用和异步操作
4. **持久化**：重要状态可持久化到本地存储
5. **响应式**：状态变化可触发UI更新

## 技术栈

- Pinia - Vue 官方状态管理库
- Vue 3 Composition API - 响应式数据管理
- Axios - HTTP 客户端
- SSE (Server-Sent Events) - 实时进度更新

## 使用方式

在组件中使用 store：

```javascript
import { useUiStore } from '@/stores/modules/ui'
import { useChatStore } from '@/stores/modules/chat'

export default {
  setup() {
    const uiStore = useUiStore()
    const chatStore = useChatStore()
    
    return {
      uiStore,
      chatStore
    }
  }
}
```

## 架构模式

- **模块化**：每个业务功能独立成一个 store 模块
- **响应式状态**：使用 ref 和 reactive 管理状态
- **组合式 API**：使用 defineStore 定义 store
- **状态同步**：通过 API 调用同步前后端状态
- **错误处理**：统一的错误处理机制