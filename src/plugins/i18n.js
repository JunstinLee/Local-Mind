import { createI18n } from 'vue-i18n'

// 导入语言文件
import enUS from '../locales/en-US.json'
import enUK from '../locales/en-UK.json'
import zhCN from '../locales/zh-CN.json'

// 从 localStorage 获取用户选择的语言，如果没有则使用浏览器语言或默认中文
const getLocale = () => {
  const savedLocale = localStorage.getItem('locale')
  if (savedLocale && ['zh-CN', 'en-US', 'en-UK'].includes(savedLocale)) {
    return savedLocale
  }
  // 检测浏览器语言
  const browserLang = navigator.language || navigator.languages[0]
  if (browserLang.startsWith('zh') || browserLang.startsWith('zh')) {
    return 'zh-CN'
  } else if (browserLang.startsWith('en-GB') || browserLang.startsWith('en-UK')) {
    return 'en-UK'
  } else if (browserLang.startsWith('en')) {
    return 'en-US'
  }
  return 'zh-CN'
}

const i18n = createI18n({
  legacy: true, // 使用 Legacy API 模式，在生产环境更稳定
  globalInjection: true, // 全局注入 $t 函数
  locale: getLocale(), // 设置当前语言，优先从 localStorage 读取
  fallbackLocale: 'en-US', // 设置备用语言
  messages: {
    'en-US': enUS,
    'en-UK': enUK,
    'zh-CN': zhCN,
  },
})

// 调试：打印当前语言和可用的翻译
if (import.meta.env.MODE === 'production') {
  console.log('[i18n] Debug Info:')
  console.log('1. Current locale:', i18n.global.locale)
  console.log('2. Fallback locale:', i18n.global.fallbackLocale)

  // 检查 messages 对象
  const messages = i18n.global.messages
  const validLocales = Object.keys(messages).filter((key) => !!messages[key])
  console.log('3. Loaded valid locales:', validLocales)

  // 深度检查 zh-CN
  if (messages['zh-CN']) {
    console.log('4. zh-CN content check:', {
      type: typeof messages['zh-CN'],
      hasHeader: !!messages['zh-CN'].header,
      sample: messages['zh-CN'].header ? messages['zh-CN'].header.title : 'N/A',
    })
  } else {
    console.error('CRITICAL: zh-CN message is missing or undefined!')
    console.log('Raw messages object:', messages)
  }

  // 测试翻译
  setTimeout(() => {
    console.log('5. Test translation (async):', i18n.global.t('header.title'))
  }, 1000)
}

// 导出 i18n 实例和语言切换函数
export { i18n as default, getLocale }
