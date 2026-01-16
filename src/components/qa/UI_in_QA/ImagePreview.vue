<template>
  <!-- Element Plus 图片组件，用于显示图片和提供预览功能 -->
  <el-image
    :src="src"
    :preview-src-list="[src]"
    :initial-index="0"
    fit="cover"
    class="image-review"
    hide-on-click-modal
    lazy
  >
    <!-- 占位符插槽，图片加载时显示的内容 -->
    <template #placeholder>
      <div class="image-slot">正在加载<span class="dot">...</span></div>
    </template>
    <!-- 错误插槽，图片加载失败时显示的内容 -->
    <template #error>
      <div class="image-slot">
        <el-icon><Picture /></el-icon> <!-- 显示图片图标 -->
      </div>
    </template>
  </el-image>
</template>

<script setup>
import { Picture } from '@element-plus/icons-vue' // 导入 Element Plus 的 Picture 图标

// 定义组件的props，接收父组件传递的数据
const props = defineProps({
  src: {
    type: String, // 图片源地址，字符串类型
    required: true, // 必需的prop
  },
})
</script>

<style scoped>
/* 图片预览容器的样式 */
.image-prerview {
  width: 100%; /* 宽度占满父容器 */
  max-width: 300px; /* 最大宽度 */
  border-radius: 8px; /* 圆角 */
  cursor: pointer; /* 鼠标悬停时显示手型光标 */
  display: block; /* 块级元素 */
}

/* 图片占位符/错误插槽的样式 */
.image-slot {
  display: flex; /* Flexbox 布局 */
  justify-content: center; /* 水平居中对齐 */
  align-items: center; /* 垂直居中对齐 */
  width: 100%; /* 宽度占满父容器 */
  height: 100%; /* 高度占满父容器 */
  min-height: 150px; /* 最小高度 */
  background: var(--el-fill-color-light); /* 背景颜色 */
  color: var(--el-text-color-secondary); /* 文本颜色 */
  font-size: 14px; /* 字体大小 */
}

/* 图片占位符/错误插槽中图标的样式 */
.image-slot .el-icon {
  font-size: 30px; /* 图标大小 */
}

/* 加载点动画的样式 */
.dot {
  animation: dot 1.4s infinite ease-in-out both; /* 应用点动画 */
  animation-delay: -0.32s; /* 动画延迟 */
}

/* 定义点动画 */
@keyframes dot {
  0%,
  80%,
  100% {
    box-shadow: 0 0; /* 阴影 */
    height: 4px; /* 高度 */
  }
  40% {
    box-shadow: 0 -4px; /* 阴影 */
    height: 5px; /* 高度 */
  }
}
</style>
