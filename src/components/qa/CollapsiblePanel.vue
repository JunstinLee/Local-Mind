<template>
  <div
    class="collapsible-panel"
    :class="[`collapsible-panel--${position}`, { 'collapsible-panel--collapsed': collapsed }]"
  >
    <!-- 面板内容 -->
    <div class="panel-content" :class="{ 'panel-content--hidden': collapsed }">
      <div class="panel-header" v-if="title && !collapsed">
        <h3 class="panel-title">{{ title }}</h3>
      </div>
      <div class="panel-body">
        <slot></slot>
      </div>
    </div>

    <!-- 切换按钮 - 使用绝对定位浮在面板上 -->
    <button
      class="toggle-button"
      :class="[`toggle-button--${position}`, { 'toggle-button--collapsed': collapsed }]"
      :aria-label="collapsed ? `展开${title}` : `折叠${title}`"
      @click="handleToggle"
    >
      <ChevronLeft
        v-if="position === 'left'"
        class="toggle-icon"
        :class="{ 'toggle-icon--rotated': collapsed }"
      />
      <ChevronRight
        v-if="position === 'right'"
        class="toggle-icon"
        :class="{ 'toggle-icon--rotated': collapsed }"
      />
    </button>
  </div>
</template>

<script setup>
import { ChevronLeft, ChevronRight } from 'lucide-vue-next'

// Props定义
const props = defineProps({
  title: {
    type: String,
    default: '',
  },
  collapsed: {
    type: Boolean,
    default: true,
  },
  position: {
    type: String,
    default: 'left',
    validator: (value) => ['left', 'right'].includes(value),
  },
  width: {
    type: String,
    default: '300px',
  },
})

// Events定义
const emit = defineEmits(['update:collapsed'])

// 方法
const handleToggle = () => {
  emit('update:collapsed', !props.collapsed)
}
</script>

<style scoped>
.collapsible-panel {
  height: 100%;
  position: relative;
}

.collapsible-panel--collapsed {
  width: 48px;
}

.collapsible-panel:not(.collapsible-panel--collapsed) {
  width: v-bind(width);
}

/* 切换按钮样式 - 绝对定位浮在面板上 */
.toggle-button {
  position: absolute;
  top: 12px;
  display: flex;
  align-items: center;
  justify-content: center;
  width: 36px;
  height: 36px;
  background-color: var(--el-bg-color);
  border: 1px solid var(--el-border-color);
  border-radius: 6px;
  cursor: pointer;
  transition: all 0.3s ease;
  color: var(--el-text-color-regular);
  z-index: 100;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
}

.toggle-button:hover {
  background-color: var(--el-fill-color);
  color: var(--el-text-color-primary);
  border-color: var(--el-border-color-light);
  box-shadow: 0 4px 8px rgba(0, 0, 0, 0.15);
}

/* 左侧面板按钮位置 - 在面板右边缘 */
.toggle-button--left {
  right: -18px; /* 按钮一半在面板外 */
}

/* 右侧面板按钮位置 - 在面板左边缘 */
.toggle-button--right {
  left: -18px; /* 按钮一半在面板外 */
}

/* 折叠状态下的按钮位置调整 */
.toggle-button--collapsed.toggle-button--left {
  right: 6px; /* 折叠时按钮在面板内 */
}

.toggle-button--collapsed.toggle-button--right {
  left: 6px; /* 折叠时按钮在面板内 */
}

/* 图标样式 */
.toggle-icon {
  width: 16px;
  height: 16px;
  transition: transform 0.3s ease;
}

.toggle-icon--rotated {
  transform: rotate(180deg);
}

/* 面板内容样式 */
.panel-content {
  height: 100%;
  display: flex;
  flex-direction: column;
  min-width: 0;
  overflow: hidden;
  transition: opacity 0.3s ease;
}

.panel-content--hidden {
  opacity: 0;
  width: 0;
  overflow: hidden;
}

/* 面板头部样式 - 去除底部边框，添加居中对齐 */
.panel-header {
  padding: 12px 16px;
  border-bottom: none;
  background-color: var(--el-bg-color);
  display: flex;
  align-items: center;
  justify-content: center;
  min-height: 48px;
}

.panel-title {
  margin: 0;
  font-size: 18px;
  font-weight: 500;
  color: var(--el-text-color-primary);
  text-align: center;
}

/* 面板主体样式 - 完全去除边框 */
.panel-body {
  flex: 1;
  overflow: hidden;
  background-color: var(--el-bg-color-page);
  border: none;
  border-radius: 0;
  margin: 0;
}

/* 暗色模式适配 */
html.dark .toggle-button {
  background-color: var(--el-bg-color);
  border-color: var(--el-border-color);
  color: var(--el-text-color-regular);
}

html.dark .toggle-button:hover {
  background-color: var(--el-fill-color);
  color: var(--el-text-color-primary);
  border-color: var(--el-border-color-light);
}

html.dark .panel-header {
  background-color: var(--el-bg-color);
}

html.dark .panel-title {
  color: var(--el-text-color-primary);
}

html.dark .panel-body {
  background-color: var(--el-bg-color-page);
}

/* 响应式设计 */
@media (max-width: 768px) {
  .collapsible-panel {
    flex-direction: column;
  }

  .collapsible-panel--right {
    flex-direction: column;
  }

  .collapsible-panel--collapsed {
    width: 100%;
    height: 48px;
  }

  .collapsible-panel:not(.collapsible-panel--collapsed) {
    width: 100%;
    height: 200px;
  }

  .toggle-button--left,
  .toggle-button--right {
    margin: 0;
  }

  .toggle-button--collapsed.toggle-button--left,
  .toggle-button--collapsed.toggle-button--right {
    margin: 0;
  }
}
</style>
