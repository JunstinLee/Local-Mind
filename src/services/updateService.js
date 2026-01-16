/**
 * 更新检查服务
 * 用于从GitHub获取最新版本信息并与当前版本比较
 */

// 从环境变量获取配置，如果没有则使用默认值
const OWNER = import.meta.env.VITE_GITHUB_OWNER || 'yourname'
const REPO = import.meta.env.VITE_GITHUB_REPO || 'yourrepo'
const CURRENT_VERSION = import.meta.env.VITE_APP_VERSION || '1.0.0'

/**
 * 检查是否有新版本可用
 * @returns {Promise<Object>} 包含更新信息的对象
 * @throws {Error} 当获取更新信息失败时抛出错误
 */
export const checkForUpdate = async () => {
  try {
    console.log(`检查更新: 当前版本 ${CURRENT_VERSION}, 仓库 ${OWNER}/${REPO}`)

    const res = await fetch(`https://api.github.com/repos/${OWNER}/${REPO}/releases/latest`, {
      headers: {
        Accept: 'application/vnd.github+json',
        'X-GitHub-Api-Version': '2022-11-28',
      },
    })

    if (!res.ok) {
      throw new Error(`Failed to fetch release info: ${res.status} ${res.statusText}`)
    }

    const data = await res.json()
    const latestVersion = data.tag_name.replace(/^v/, '')

    console.log(`最新版本: ${latestVersion}, 当前版本: ${CURRENT_VERSION}`)

    if (isNewerVersion(latestVersion, CURRENT_VERSION)) {
      return {
        hasUpdate: true,
        latestVersion,
        url: data.html_url,
        notes: data.body || '',
        name: data.name,
        publishedAt: data.published_at,
      }
    }

    return { hasUpdate: false }
  } catch (error) {
    console.error('检查更新失败:', error)
    throw new Error(`Failed to check for updates: ${error.message}`)
  }
}

/**
 * 语义化版本比较
 * @param {string} a - 版本字符串 a
 * @param {string} b - 版本字符串 b
 * @returns {boolean} 如果 a > b 则返回 true
 */
function isNewerVersion(a, b) {
  // 处理预发布版本 (如 1.0.0-alpha)
  const aPreRelease = a.split('-')
  const bPreRelease = b.split('-')

  const aMain = aPreRelease[0].split('.').map(Number)
  const bMain = bPreRelease[0].split('.').map(Number)

  // 比较主版本号
  for (let i = 0; i < Math.max(aMain.length, bMain.length); i++) {
    const na = aMain[i] || 0
    const nb = bMain[i] || 0
    if (na > nb) return true
    if (na < nb) return false
  }

  // 主版本号相同，检查预发布版本
  // 有预发布版本的版本被认为比没有预发布版本的版本旧
  if (aPreRelease.length === 1 && bPreRelease.length > 1) {
    return true // a 是正式版，b 是预发布版
  }
  if (aPreRelease.length > 1 && bPreRelease.length === 1) {
    return false // a 是预发布版，b 是正式版
  }

  // 如果都有预发布版本，继续比较预发布版本
  if (aPreRelease.length > 1 && bPreRelease.length > 1) {
    const aPre = aPreRelease[1]
    const bPre = bPreRelease[1]

    // 这里简化处理，直接比较字符串
    // 实际应用中可能需要更复杂的预发布版本比较逻辑
    return aPre.localeCompare(bPre) < 0
  }

  return false // 版本相同
}

/**
 * 获取更新检查状态信息
 * @param {Object} updateInfo - 更新信息对象
 * @returns {string} 状态描述文本
 */
export const getUpdateStatusText = (updateInfo) => {
  if (!updateInfo) {
    return '未知状态'
  }

  if (updateInfo.hasUpdate) {
    return `发现新版本 ${updateInfo.latestVersion}`
  }

  return '当前已是最新版本'
}
