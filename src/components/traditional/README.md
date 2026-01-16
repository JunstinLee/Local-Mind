# Traditional 组件库

本目录包含传统文件管理功能的所有前端组件。这些组件使用 Vue 3、Element Plus 和 TailwindCSS 构建，提供了传统的文件浏览、筛选和管理功能。

## 文件结构

```
fronted/src/components/traditional/
├── DocItem.vue           # 文档项展示组件
├── FileTree.vue          # 文件树结构展示组件
└── TraditionalFilter.vue # 传统筛选器组件
```

## 组件功能说明

### 1. DocItem.vue
- **功能**：文档列表项组件，展示单个文档的详细信息
- **特性**：
  - 显示文档名称、修改日期、大小和路径
  - 格式化日期和文件大小显示
  - 提供文档详情查看和删除操作
  - 响应式设计，适配不同屏幕尺寸
  - 暗色模式支持

### 2. FileTree.vue
- **功能**：文件树结构展示组件，以树形结构展示文件和文件夹
- **特性**：
  - 递归渲染文件树结构
  - 支持文件夹展开/收起
  - 不同文件类型使用不同颜色图标
  - 显示文件数量统计
  - 响应式设计和暗色模式支持

### 3. TraditionalFilter.vue
- **功能**：传统筛选器组件，提供关键词和文件类型筛选功能
- **特性**：
  - 弹窗式筛选设置界面
  - 支持关键词搜索
  - 多文件类型选择（PDF, DOCX, TXT, MD等）
  - 已选筛选项可视化展示
  - 筛选项重置和应用功能
  - 与文件存储状态集成

## 设计原则

1. **响应式设计**：所有组件都适配不同屏幕尺寸
2. **暗色模式**：支持暗色主题，提供良好的夜间使用体验
3. **用户体验**：提供加载状态、空状态和错误状态的友好提示
4. **性能优化**：使用虚拟滚动等技术确保大列表的流畅性
5. **可访问性**：遵循可访问性最佳实践，包含适当的标签和ARIA属性

## 使用说明

这些组件通常组合在一个传统文件管理页面中使用：

```vue
<template>
  <div class="traditional-container">
    <TraditionalFilter @filters-changed="handleFiltersChange" />
    <FileTree :treeData="fileTreeData" :isLoading="isLoading" />
    <DocItem :documents="filteredDocuments" :isLoading="isLoading" />
  </div>
</template>
```

组件之间通过 Pinia store 进行状态管理和通信，确保数据同步。

## 技术栈

- Vue 3 Composition API
- Element Plus UI 组件库
- TailwindCSS 样式框架
- Pinia 状态管理
- Lucide Vue Next 图标库
- Vue I18n 国际化

## 组件间关系

- `TraditionalFilter` 组件负责筛选条件的设置和管理
- `FileTree` 组件以树形结构展示文件系统层次结构
- `DocItem` 组件以列表形式展示文档详细信息
- 所有组件通过 Pinia store 进行状态同步