# Common 组件库

本目录包含整个应用的通用组件。这些组件使用 Vue 3、Element Plus 和 TailwindCSS 构建，提供了一系列可复用的 UI 组件。

## 文件结构

```
fronted/src/components/common/
├── APPSetting.vue              # 应用设置弹窗组件
├── choosefolder.vue            # 文件夹选择组件
├── CompactHeader.vue           # 紧凑型头部组件
├── FileExport.vue              # 文件导出组件
├── FileUploadModal.vue         # 文件上传模态框组件
├── GlobalNotification.vue      # 全局通知组件
├── KnowledgeBuildModal.vue     # 知识库构建模态框组件
└── LoadingProgressModal.vue    # 加载进度模态框组件
```

## 组件功能说明

### 1. APPSetting.vue
- **功能**：应用设置弹窗，管理语言设置和模型管理
- **特性**：
  - 提供语言选择功能
  - 显示可用模型列表及其详细信息
  - 支持模型的下载、激活和管理
  - 显示 Hugging Face 缓存路径
  - 模型状态管理（激活、下载中、已下载等）

### 2. CompactHeader.vue
- **功能**：紧凑型头部组件，包含导航标签和操作按钮
- **特性**：
  - 标题和导航标签整合在同一行
  - 包含文件上传、知识库构建、主题切换和设置按钮
  - 响应式设计
  - 与路由系统集成

### 3. FileUploadModal.vue
- **功能**：文件上传模态框，支持文件和文件夹上传
- **特性**：
  - 拖放上传支持
  - 文件夹上传支持
  - 文件列表预览
  - 文件信息显示（名称、大小）
  - 上传进度显示

### 4. KnowledgeBuildModal.vue
- **功能**：知识库构建模态框，显示文件处理进度
- **特性**：
  - 总体进度条显示
  - 单个文件处理状态显示
  - 处理状态管理（待处理、处理中、已完成、错误）
  - 文件详细信息和错误消息显示

### 5. GlobalNotification.vue
- **功能**：全局通知组件，提供统一的通知显示
- **特性**：
  - 支持成功和错误类型的通知
  - 动画过渡效果
  - 自动居中定位
  - 可配置的通知时长

### 6. LoadingProgressModal.vue
- **功能**：加载进度模态框，显示后端初始化状态
- **特性**：
  - 显示模型加载状态
  - 显示 ChromaDB 初始化状态
  - 显示搜索服务初始化状态
  - 总体进度计算
  - 自动检查后端状态

### 7. FileExport.vue
- **功能**：文件导出组件，支持批量文件导出
- **特性**：
  - 文件和文件夹选择
  - 导出统计信息（文件数量、总大小）
  - 选中文件列表显示
  - 导出格式选择
  - 导出选项配置

### 8. choosefolder.vue
- **功能**：文件夹选择组件，提供文件夹选择界面
- **特性**：
  - 文件夹选择对话框
  - 文件夹信息显示（名称、文件数量、总大小）
  - 文件夹大小计算
  - 文件夹选择事件触发

## 设计原则

1. **可复用性**：所有组件都设计为可在整个应用中复用
2. **响应式设计**：所有组件都适配不同屏幕尺寸
3. **暗色模式**：所有组件都支持暗色主题
4. **用户体验**：提供清晰的视觉反馈和状态指示
5. **可访问性**：遵循可访问性最佳实践

## 使用说明

这些通用组件在应用的各个部分被复用：

```vue
<template>
  <div class="app-container">
    <CompactHeader />
    <FileUploadModal />
    <KnowledgeBuildModal />
    <GlobalNotification />
    <APPSetting />
    <LoadingProgressModal />
  </div>
</template>
```

各组件通过 Pinia store 进行状态管理，确保组件间的通信和数据同步。

## 技术栈

- Vue 3 Composition API
- Element Plus UI 组件库
- TailwindCSS 样式框架
- Pinia 状态管理
- Lucide Vue Next 图标库
- Vue I18n 国际化