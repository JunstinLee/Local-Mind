# QA 组件库

本目录包含问答系统的所有核心前端组件。这些组件使用 Vue 3、Element Plus 和 TailwindCSS 构建，实现了完整的聊天界面功能。

## 文件结构

```
fronted/src/components/qa/
├── ChatSidebar.vue          # 聊天侧边栏组件，管理会话历史
├── CollapsiblePanel.vue     # 可折叠面板组件
├── Input.vue                # 用户输入组件，包含模型选择和消息发送功能
├── MessageBU.vue            # 消息项组件，显示单条用户或AI消息
├── MessageList.vue          # 消息列表组件，渲染整个聊天记录
├── QALayout.vue             # QA系统主布局组件
├── TypingIndicator.vue      # 打字指示器组件，显示AI正在思考的状态
├── UI_in_QA/               # UI组件子目录
│   ├── ImagePreview.vue     # 图片预览组件
│   ├── MarkdownRenderer.vue # Markdown渲染组件
│   └── ThinkingChain.vue    # 思考链显示组件
```

## 组件功能说明

### 1. QALayout.vue
- **功能**：问答系统的主布局组件，提供整体的页面结构
- **特性**：包含侧边栏、消息内容区域和底部输入框布局

### 2. ChatSidebar.vue
- **功能**：聊天侧边栏组件，管理会话历史记录
- **特性**：
  - 显示用户信息
  - 提供创建新聊天的功能
  - 展示聊天历史列表
  - 支持侧边栏折叠/展开

### 3. MessageList.vue
- **功能**：消息列表容器组件，管理并渲染聊天消息列表
- **特性**：自动滚动到最新消息，响应消息列表变化

### 4. MessageBU.vue
- **功能**：单个消息项组件，显示用户或AI的消息
- **特性**：
  - 根据消息角色显示不同布局（用户或AI）
  - 集成思考链显示
  - 支持来源信息显示
  - 提供复制和另存为功能
  - 支持Markdown内容渲染

### 5. Input.vue
- **功能**：用户输入组件，提供消息输入和模型选择功能
- **特性**：
  - 支持多行文本输入，可自动调整大小
  - 模型选择下拉菜单
  - 回车发送消息，Shift+回车换行
  - 发送按钮

### 6. TypingIndicator.vue
- **功能**：打字指示器组件，显示AI正在生成回复的状态
- **特性**：三个动态点的动画效果

### 7. CollapsiblePanel.vue
- **功能**：可折叠面板组件，用于节省界面空间
- **特性**：
  - 支持左右位置配置
  - 可控的展开/折叠状态
  - 自定义标题

## UI_in_QA 子目录组件

### 1. MarkdownRenderer.vue
- **功能**：安全渲染Markdown内容的组件
- **特性**：
  - 支持代码高亮
  - XSS防护
  - 自定义内边距

### 2. ThinkingChain.vue
- **功能**：显示AI思考过程的组件
- **特性**：
  - 可展开/收起思考内容
  - 步骤标签显示
  - 动画过渡效果

### 3. ImagePreview.vue
- **功能**：图片预览组件
- **特性**：
  - 懒加载
  - 点击放大预览
  - 加载状态显示
  - 错误状态显示

## 设计原则

1. **组件化**：将UI拆分为独立、可复用的组件
2. **响应式**：适配不同屏幕尺寸
3. **国际化**：支持多语言显示
4. **可访问性**：遵循可访问性最佳实践
5. **性能**：使用虚拟滚动等技术处理大量数据

## 使用示例

这些组件通常在问答系统的主页面中组合使用：

```vue
<template>
  <QALayout>
    <template #messages>
      <MessageList :messages="chatMessages" />
    </template>
    <template #input>
      <Input @send-message="handleSendMessage" />
    </template>
  </QALayout>
</template>
```

这些组件共同构成了一个功能完整的问答界面，支持模型选择、消息历史记录、思考链显示、来源引用等功能。