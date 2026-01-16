# Services 服务层

本目录包含前端应用的网络请求和业务逻辑服务层。这些服务负责与后端 API 通信、处理数据和封装业务逻辑。

## 文件结构

```
fronted/src/services/
├── api.js          # API 请求基础服务
├── BuildBase.js    # 知识库构建服务
└── check.js        # 检查服务
```

## 服务功能说明

### 1. api.js
- **功能**：API 请求基础服务，封装了与后端通信的通用方法
- **特性**：
  - 基于 Axios 创建的 API 客户端实例
  - 统一的基础 URL 配置（`/api`）
  - 全局响应拦截器，处理错误和异常
  - 批量文件上传功能
  - 文件目录树加载服务
  - 文件列表筛选加载服务
  - 知识库批量构建服务
  - 上传路径配置管理

### 2. BuildBase.js
- **功能**：知识库构建服务，处理文档批量处理和索引
- **特性**：
  - 提供 `useKnowledgeBaseBuilder` 组合式函数
  - 支持文件处理进度可视化
  - 模拟和真实处理进度同步
  - 处理状态管理（处理中、成功、错误、空文件等）
  - 批量文件处理和索引
  - 进度计算和状态跟踪

### 3. check.js
- **功能**：检查服务，提供未向量化文件列表功能
- **特性**：
  - 获取未向量化的文件列表
  - 支持路径、筛选条件、排序等参数
  - 与后端 `/file/files/unvectorized_list` 端点通信

## 设计原则

1. **模块化**：将不同功能的服务分离到不同文件中
2. **可复用性**：API 服务函数可在多个组件中复用
3. **错误处理**：统一的错误处理机制
4. **响应式**：与 Vue 3 的响应式系统集成
5. **类型安全**：通过 JSDoc 提供类型提示

## 技术栈

- Axios - HTTP 客户端库
- Vue 3 Composition API - 组合式函数
- JavaScript ES6+ - 现代 JavaScript 特性

## 使用方式

在组件中使用服务：

```javascript
// 使用 API 服务
import { uploadFileBatch, loadFileTree, loadFileList } from '@/services/api'

// 使用知识库构建服务
import { useKnowledgeBaseBuilder } from '@/services/BuildBase'

// 使用检查服务
import { loadUnvectorizedFileList } from '@/services/check'
```

## 服务组合

这些服务通常与其他层（如 stores）结合使用：

1. API 服务提供数据获取能力
2. BuildBase 服务处理复杂的业务逻辑
3. Check 服务提供特定的数据检查功能

这些服务共同构成了前端应用与后端 API 通信的基础设施。