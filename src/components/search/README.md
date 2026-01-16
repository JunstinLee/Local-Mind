# Search 组件库

本目录包含搜索功能的所有前端组件。这些组件使用 Vue 3、Element Plus 和 TailwindCSS 构建，提供了语义搜索功能和丰富的过滤选项。

## 文件结构

```
fronted/src/components/search/
├── ResultItem.vue          # 搜索结果项组件
├── SearchControlPanel.vue  # 搜索控制面板组件
├── SearchFilters.vue       # 搜索过滤器组件
└── SearchResults.vue       # 搜索结果容器组件
```

## 组件功能说明

### 1. SearchControlPanel.vue
- **功能**：搜索控制面板，包含主搜索输入框和过滤器切换按钮
- **特性**：
  - 提供大型文本输入区域用于输入搜索查询
  - 包含圆形搜索按钮，支持回车触发搜索
  - 集成 SearchFilters 组件，提供过滤选项
  - 响应式设计，适配不同屏幕尺寸

### 2. SearchFilters.vue
- **功能**：搜索过滤器组件，提供多种筛选条件
- **特性**：
  - 文件类型过滤（支持多选）
  - 时间范围过滤（全部时间、今天、本周、本月、本年）
  - 修改时间过滤（任意时间、24小时内、一周内、一个月内）
  - 文件大小过滤（任意大小、小于1MB、1-10MB、大于10MB）
  - 重置所有过滤器功能

### 3. SearchResults.vue
- **功能**：搜索结果容器组件，管理并展示搜索结果
- **特性**：
  - 显示搜索加载状态和动画
  - 展示搜索结果的数量和时间信息
  - 提供筛选后无结果的友好提示
  - 展示通用无结果状态和搜索前的初始状态
  - 结果动画效果（fade-in-up）

### 4. ResultItem.vue
- **功能**：单个搜索结果项组件，展示每个搜索结果的详细信息
- **特性**：
  - 显示文件名和相关性分数
  - 支持内容预览，最多显示3行
  - 高亮显示搜索匹配的内容
  - 显示文档来源信息
  - 响应式设计和暗色模式支持
  - 悬停效果（阴影变化、边框变色、轻微上移）

## 设计原则

1. **响应式设计**：所有组件都适配不同屏幕尺寸
2. **暗色模式**：支持暗色主题，提供良好的夜间使用体验
3. **用户体验**：提供加载状态、空状态和错误状态的友好提示
4. **性能优化**：使用虚拟滚动等技术确保大列表的流畅性
5. **可访问性**：遵循可访问性最佳实践，包含适当的标签和ARIA属性

## 使用说明

这些组件通常组合在一个搜索页面中使用：

```vue
<template>
  <div class="search-container">
    <SearchControlPanel />
    <SearchResults />
  </div>
</template>
```

SearchControlPanel 包含搜索输入和过滤选项，SearchResults 展示搜索结果。两个组件通过 Pinia store 进行状态管理，确保数据同步和通信。

## 技术栈

- Vue 3 Composition API
- Element Plus UI 组件库
- TailwindCSS 样式框架
- Pinia 状态管理
- Lucide Vue Next 图标库
- Vue I18n 国际化