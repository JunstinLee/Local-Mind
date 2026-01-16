<template>
  <!-- 思考链组件的根容器 -->
  <div class="think-chain">
    <!-- Element Plus 卡片组件，用于包裹思考过程内容，并提供阴影效果 -->
    <el-card shadow="never" class="toggleExpanded">
      <!-- 卡片的头部插槽 -->
      <template #header>
        <!-- 思考过程头部区域，点击可展开/收起 -->
        <div class="think-header" @click="toggleExpand">
          <!-- 信息图标 -->
          <el-icon class="think-icon">
            <InfoFilled />
          </el-icon>
          <!-- 思考过程标题 -->
          <span class="think-title">{{ t('qa.thinking') }}</span>
          <!-- 展开/收起按钮 -->
          <el-button type="text" size="small" class="toggle-btn">
            <el-icon>
              <!-- 根据 expanded 状态动态显示向上或向下的箭头图标 -->
              <component :is="expanded ? 'ArrowUp' : 'ArrowDown'" />
            </el-icon>
            <!-- 根据 expanded 状态动态显示“Collapse”（收起）或“Expand”（展开）文本 -->
            {{ expanded ? t('qa.collapse') : t('qa.expand') }}
          </el-button>
        </div>
      </template>
      <!-- Element Plus 折叠过渡组件，提供展开/收起时的动画效果 -->
      <el-collapse-transition>
        <!-- 思考过程内容区域，只有当 expanded 为 true 时才显示 -->
        <div v-show="expanded" class="think-content">
          <!-- 遍历思考数据，显示实时思考内容 -->
          <div v-for="(step, index) in props.thinkingData" :key="index" class="thinking-step-container">
            <div class="thinking-step">
              <!-- 步骤标签，显示阶段信息 -->
              <el-tag type="primary" size="small" class="step-tag">
                {{ t('qa.step', { index: index + 1 }) }}
              </el-tag>
              <!-- 步骤内容区域 -->
              <div class="step-content">
                <!-- 显示思考内容 -->
                <p class="step-text">{{ step }}</p>
              </div>
            </div>
            <!-- 如果不是最后一项，添加分隔线 -->
            <div v-if="index < props.thinkingData.length - 1" class="step-separator"></div>
          </div>
        </div>
      </el-collapse-transition>
    </el-card>
  </div>
</template>

<script setup>
import { ref } from 'vue' // 导入 Vue 的 ref 函数
import { useI18n } from 'vue-i18n' // 导入 useI18n
import { InfoFilled } from '@element-plus/icons-vue' // 导入 Element Plus 图标

const { t } = useI18n()

// 定义组件的props，接收父组件传递的数据
const props = defineProps({
  thinkingData: {
    type: Array, // 思考链数据，期望是一个字符串数组，每个字符串代表一个思考片段
    default: () => [], // 默认值为空数组
  },
  defaultExpanded: {
    type: Boolean, // 默认是否展开思考过程
    default: true, // 默认为展开
  },
})

// 响应式变量，控制思考过程内容的展开/收起状态，初始值由 defaultExpanded prop 决定
const expanded = ref(props.defaultExpanded)

// 切换展开/收起状态的函数
const toggleExpand = () => {
  expanded.value = !expanded.value
}
</script>

<style scoped>
/* 思考链容器的样式 */
.think-chain {
  margin: 12px 0;
  /* 上下外边距 */
  width: 100%;
  /* 确保占满容器宽度 */
}

/* 思考头部区域的样式 */
.think-header {
  display: flex;
  /* Flexbox 布局 */
  align-items: center;
  /* 垂直居中对齐 */
  cursor: pointer;
  /* 鼠标悬停时显示手型光标 */
}

/* 思考图标的样式 */
.think-icon {
  color: var(--el-color-primary);
  /* 颜色 */
  margin-right: 8px;
  /* 右侧外边距 */
}

/* 思考标题的样式 */
.think-title {
  font-weight: 500;
  /* 字体粗细 */
  color: var(--el-text-color-primary);
  /* 文本颜色 */
}

/* 思考内容区域的样式 */
.think-content {
  max-height: 400px;
  /* 最大高度 */
  overflow-y: auto;
  /* 垂直滚动条 */
}

/* 单个思考步骤容器的样式 */
.thinking-step-container {
  margin-bottom: 12px;
  /* 底部外边距 */
}

/* 单个思考步骤的样式 */
.thinking-step {
  display: flex;
  /* Flexbox 布局 */
  flex-direction: column;
  /* 垂直排列 */
}

/* 步骤标签的样式 */
.step-tag {
  align-self: flex-start;
  /* 左对齐 */
  margin-bottom: 6px;
  /* 下边距 */
}

/* 步骤内容区域的样式 */
.step-content {
  margin-left: 0;
  /* 左边距 */
}

/* 步骤文本的样式 */
.step-text {
  margin: 0;
  /* 外边距 */
  color: var(--el-text-color-primary);
  /* 文本颜色 */
  line-height: 1.5;
  /* 行高 */
  white-space: pre-wrap;
  /* 保留空白符换行 */
  word-wrap: break-word;
  /* 自动换行 */
}

/* 步骤分隔线的样式 */
.step-separator {
  height: 1px;
  background-color: var(--el-border-color);
  margin: 12px 0;
}
</style>