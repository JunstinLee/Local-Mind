<template>
  <!--
    Markdown渲染组件
    功能：将Markdown文本渲染为安全的HTML并应用样式
    特性：
    - 支持代码高亮
    - XSS防护
    - 可配置内边距
  -->
  <div class="markdown-body" v-html="sanitizedHtml" :style="containerStyle" data-testid="markdown-renderer"></div>
</template>

<script setup>
import { computed } from 'vue'
import { useI18n } from 'vue-i18n'
import { marked } from 'marked'
import DOMPurify from 'dompurify'
import hljs from 'highlight.js'

const { t } = useI18n()

/**
 * 组件属性定义
 * @property {string} source - 要渲染的Markdown源文本（必需）
 * @property {string|number} padding - 容器内边距，支持数字（自动转为px）或字符串（如'10px'）
 */
const props = defineProps({
  source: {
    type: String,
    required: true,
    default: '',
  },
  padding: {
    type: [String, Number],
    default: '10px',
  },
})

/**
 * 配置marked解析器
 * 设置代码高亮、GitHub风格Markdown等选项
 */
marked.setOptions({
  /**
   * 代码高亮处理函数
   * @param {string} code - 代码内容
   * @param {string} lang - 语言类型
   * @returns {string} 高亮后的HTML代码
   */
  highlight: (code, lang) => {
    // 检查语言是否被highlight.js支持，不支持则使用纯文本
    const language = hljs.getLanguage(lang) ? lang : 'plaintext'
    return hljs.highlight(code, { language }).value
  },
  langPrefix: 'hljs language-', // 代码块CSS类前缀
  pedantic: false, // 不强制符合原始markdown.pl行为
  gfm: true, // 启用GitHub风格Markdown
  breaks: false, // 不将换行符转换为<br>
  sanitize: false, // 禁用marked内置的XSS过滤（使用DOMPurify代替）
  smartLists: true, // 启用智能列表渲染
  smartypants: false, // 禁用智能引号和破折号
  xhtml: false, // 不输出XHTML
})

/**
 * 原始HTML计算属性
 * 将Markdown源文本转换为HTML，不做任何过滤
 */
const rawHtml = computed(() => {
  if (!props.source) {
    return ''
  }
  
  // 处理后端返回的 I18N 占位符
  // 格式: I18N:KEY -> rag_table.key
  const processedSource = props.source.replace(/I18N:([A-Z_]+)/g, (match, key) => {
    return t(`rag_table.${key.toLowerCase()}`)
  })
  
  return marked(processedSource)
})

/**
 * 净化后的HTML计算属性
 * 使用DOMPurify进行XSS防护，确保渲染内容安全
 */
const sanitizedHtml = computed(() => {
  return DOMPurify.sanitize(rawHtml.value, {
    USE_PROFILES: { html: true }, // 使用HTML配置文件
    ADD_ATTR: ['target'], // 允许target属性（用于链接新窗口打开）
  })
})

/**
 * 标准化内边距值
 * 将数字类型转换为带px单位的字符串
 */
const normalizedPadding = computed(() => {
  if (typeof props.padding === 'number') {
    return `${props.padding}px`
  }
  return props.padding
})

/**
 * 容器样式计算属性
 * 根据props.padding生成内联样式对象
 */
const containerStyle = computed(() => {
  return {
    padding: normalizedPadding.value,
  }
})
</script>

<style>
/**
 * Markdown内容基础样式
 * 遵循GitHub风格设计，确保良好的可读性
 */

/* 标题样式 - 统一处理所有级别标题的基础样式 */
.markdown-body h1,
.markdown-body h2,
.markdown-body h3,
.markdown-body h4,
.markdown-body h5,
.markdown-body h6 {
  margin-top: 0;
  /* 移除顶部外边距 */
  margin-bottom: 0;
  /* 移除底部外边距 */
  font-weight: 600;
  /* 半粗体，突出显示 */
  line-height: 1.25;
  /* 标题行高略小，更紧凑 */
}

/* 一级标题样式 - 最大标题，带底边框 */
.markdown-body h1 {
  font-size: 2em;
  /* 2倍字体大小 */
  border-bottom: 1px solid #eaecef;
  /* 浅灰色底边框，分隔内容 */
}

/* 二级标题样式 - 次级标题，也带底边框 */
.markdown-body h2 {
  font-size: 1.5em;
  /* 1.5倍字体大小 */
  border-bottom: 1px solid #eaecef;
  /* 浅灰色底边框 */
}

/* 段落样式 - 基础文本块 */
.markdown-body p {
  margin-top: 0;
  /* 移除顶部外边距 */
  margin-bottom: 0;
  /* 移除底部外边距 */
}

/* 列表样式 - 有序列表和无序列表 */
.markdown-body ul,
.markdown-body ol {
  padding-left: 2em;
  /* 左侧缩进2字符，为项目符号留出空间 */
  margin-top: 0;
  /* 移除顶部外边距 */
  margin-bottom: 0;
  /* 移除底部外边距 */
}

/* 引用块样式 - 类似邮件引用格式 */
.markdown-body blockquote {
  margin: 0;
  /* 移除外边距 */
  padding: 0 1em;
  /* 左右内边距1字符 */
  color: #6a737d;
  /* 灰色文字，表示次要内容 */
  border-left: 0.25em solid #dfe2e5;
  /* 左侧边框，引用标识 */
}

/* 行内代码样式 - 单行代码片段 */
/* 基础容器样式 - 需要添加宽度约束 */
.markdown-body {
  line-height: 1.6;
  word-wrap: break-word;
  background-color: transparent;
  /* 添加以下属性 */
  max-width: 100%;
  width: 100%;
  box-sizing: border-box;
  overflow-wrap: break-word;
}

/* 代码块样式 - 不自动换行，显示滚动条 */
.markdown-body pre {
  background-color: #f6f8fa !important;
  border-radius: 6px !important;
  padding: 16px !important;
  overflow-x: auto !important;
  overflow-y: hidden !important;
  white-space: pre !important;
  /* 强制不换行 */
  margin-top: 0 !important;
  margin-bottom: 0 !important;

  /* 强制宽度约束 */
  width: 100% !important;
  /* 视口宽度的40%，响应式且有明确边界 */
  max-width: 40vw !important;
  box-sizing: border-box !important;
}



/* 暗色模式下的代码块样式 */
.dark .markdown-body pre {
  background-color: transparent;
  /* 暗色背景 */
  color: #e2e8f0;
  /* 浅色文字 */
}

/* 暗色模式下的行内代码样式 */
.dark .markdown-body code {
  background-color: transparent;
  /* 半透明白色背景 */
  color: #e2e8f0;
  /* 浅色文字 */
}

/* 暗色模式下的代码块中的代码样式 */
.dark .markdown-body pre code {
  background-color: transparent;
  /* 透明背景 */
  color: inherit;
  /* 继承父元素颜色 */
}

/* 链接样式 - 默认状态 */
.markdown-body a {
  color: #0366d6;
  /* GitHub蓝色链接色 */
  text-decoration: none;
  /* 移除下划线，悬停时显示 */
}

/* 链接悬停样式 - 交互反馈 */
.markdown-body a:hover {
  text-decoration: underline;
  /* 悬停时显示下划线 */
}
</style>
