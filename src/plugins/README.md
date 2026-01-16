# Plugins 插件配置

本目录包含应用使用的第三方插件配置模块。

## 文件结构

```
fronted/src/plugins/
└── i18n.js                 # 国际化插件配置
```

## 插件功能说明

### i18n.js
- **功能**：应用的国际化插件配置文件
- **特性**：
  - 基于 vue-i18n 实现多语言支持
  - 集成多种语言配置（包括中文、英语、法语、德语、西班牙语、日语、韩语等）
  - 支持从 localStorage 读取用户选择的语言设置
  - 兼容浏览器语言检测并自动切换
  - 设置备用语言选项（默认为英文）

#### 语言支持：
- 中文系列：简体中文、香港繁体、台湾繁体
- 英语系列：美国英语、英国英语
- 欧洲语言：法语、德语、西班牙语
- 亚洲语言：日语、韩语

#### 主要功能：
- 自动检测浏览器语言并切换
- 优先使用用户本地存储的语言设置
- 提供语言切换函数
- 使用 Composition API 模式（legacy: false）

## 技术栈

- vue-i18n - Vue.js 国际化插件
- Vue 3 - Composition API 模式

## 设计原则

1. **模块化**：将国际化配置独立为插件模块
2. **可扩展性**：易于添加新的语言支持
3. **用户体验**：支持自动语言检测和本地存储偏好
4. **性能优化**：使用按需导入减少包体积

## 使用方式

插件已在 main.js 中集成：

```javascript
// 在组件中使用
import { useI18n } from 'vue-i18n'

const { t, locale } = useI18n()

// 获取当前文本
const text = t('search.prompt')

// 切换语言
locale.value = 'zh-CN'
```

## 配置选项

- `legacy: false` - 使用 Composition API 模式
- `locale` - 当前语言，从 localStorage 或浏览器语言检测
- `fallbackLocale` - 备用语言（英文）
- `messages` - 所有支持的语言配置