# Locales 多语言配置

本目录包含应用的多语言配置文件，支持多种语言的国际化功能。

## 文件结构

```
fronted/src/locales/
├── de-DE.json              # 德语 (German)
├── en-UK.json              # 英语 (英国 English - UK)
├── en-US.json              # 英语 (美国 English - US)
├── es-ES.json              # 西班牙语 (Spanish)
├── fr-FR.json              # 法语 (French)
├── ja-JP.json              # 日语 (Japanese)
├── ko-KR.json              # 韩语 (Korean)
├── zh-CN.json              # 中文 (简体 Chinese - Simplified)
├── zh-HK.json              # 中文 (香港繁体 Chinese - Hong Kong)
└── zh-TW.json              # 中文 (台湾繁体 Chinese - Taiwan)
```

## 语言支持说明

### 已支持语言
- **中文系列**：简体中文、香港繁体、台湾繁体
- **英语系列**：美国英语、英国英语
- **欧洲语言**：法语、德语、西班牙语
- **亚洲语言**：日语、韩语

### 语言配置结构
每个语言文件都包含以下模块：
- `search` - 搜索功能相关文本
- `filter` - 筛选器相关文本
- `upload` - 上传功能相关文本
- `knowledgeBase` - 知识库相关文本
- `document` - 文档管理相关文本
- `settings` - 设置页面相关文本
- `time` - 时间相关文本
- `refresh` - 模型下载完成刷新提示相关文本
- `common` - 通用文本

其中，`refresh` 模块包含以下键值对：
- `title` - 刷新模态框标题
- `downloadComplete` - 下载完成提示文本
- `modelDownloaded` - 模型已下载文本（包含{modelName}参数）
- `refreshRequired` - 刷新必要性提示文本
- `refreshNow` - 立即刷新按钮文本

## 技术栈

- vue-i18n - Vue.js 国际化插件
- JSON - 语言配置文件格式

## 功能特性

1. **自动检测**：根据浏览器语言自动选择对应语言包
2. **本地存储**：优先使用用户选择的语言设置
3. **备选语言**：设置备选语言以确保文本显示
4. **参数化**：支持文本中的参数替换（如 {count}）

## 使用方式

语言配置已在 i18n 插件中集成：

```javascript
// 在组件中使用
import { useI18n } from 'vue-i18n'

const { t } = useI18n()
const text = t('search.prompt') // 获取对应语言的文本
```

## 添加新语言

1. 创建新的语言 JSON 文件（如 ru-RU.json）
2. 在 i18n.js 插件中导入新的语言文件
3. 添加到 messages 配置中
4. 在语言检测逻辑中添加相应的检测规则