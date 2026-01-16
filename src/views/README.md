# Views 视图层

本目录包含应用的三个主要视图页面，分别对应问答、搜索和传统文档管理功能。

## 文件结构

```
fronted/src/views/
├── forQA.vue         # 问答系统视图
├── forSearch.vue     # 搜索系统视图
└── forTradition.vue  # 传统文档管理视图
```

## 视图功能说明

### 1. forQA.vue
- **功能**：问答系统视图，提供智能问答功能
- **特性**：
  - 集成 QALayout 布局组件，提供统一的问答界面
  - 支持消息列表显示和历史记录
  - 集成输入组件，支持模型选择和消息发送
  - 实现流式响应处理，支持思考链显示
  - 支持消息持久化到 localStorage
  - 使用 UUID 生成会话 ID
  - 支持历史消息上下文传递
  - 集成来源信息显示

### 2. forSearch.vue
- **功能**：搜索系统视图，提供语义搜索功能
- **特性**：
  - 集成 SearchControlPanel 组件，提供搜索输入和过滤器
  - 集成 SearchResults 组件，展示搜索结果
  - 响应式设计，适配不同屏幕尺寸
  - 暗色模式支持
  - 渐变背景设计
  - 搜索结果动画效果

### 3. forTradition.vue
- **功能**：传统文档管理视图，提供文件浏览和管理功能
- **特性**：
  - 采用响应式网格布局（左侧筛选器和文件树，右侧文档列表）
  - 集成 TraditionalFilter 组件，提供文档筛选功能
  - 集成 FileTree 组件，以树形结构展示文件
  - 集成 DocItem 组件，展示文档详细信息
  - 支持文件上传功能
  - 集成 FileUploadModal 组件
  - 高度自适应布局
  - 自定义滚动条样式
  - 暗色模式支持

## 设计原则

1. **响应式设计**：所有视图都适配不同屏幕尺寸
2. **状态管理**：通过 Pinia store 统一管理应用状态
3. **组件复用**：各视图共享通用组件
4. **用户体验**：提供流畅的交互体验
5. **性能优化**：合理管理数据加载和渲染

## 架构模式

- **模块化**：每个视图专注于特定功能
- **组件化**：通过组合多个子组件构建完整视图
- **状态驱动**：通过 store 管理视图状态
- **事件驱动**：通过事件处理用户交互

## 技术栈

- Vue 3 Composition API
- Element Plus UI 组件库
- TailwindCSS 样式框架
- Pinia 状态管理
- Lucide Vue Next 图标库
- Vue I18n 国际化
- UUID 生成器

## 路由集成

这些视图通常通过 Vue Router 集成到应用中：

```javascript
{
  path: '/qa',
  name: 'QA',
  component: () => import('@/views/forQA.vue')
},
{
  path: '/search',
  name: 'Search',
  component: () => import('@/views/forSearch.vue')
},
{
  path: '/traditional',
  name: 'Traditional',
  component: () => import('@/views/forTradition.vue')
}
```