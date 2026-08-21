import generatedSidebar from '../sidebar.generated.json'

type GeneratedSidebar = {
  patterns: Record<string, { problemIds?: string[] }>
}

const patternProblems = Object.fromEntries(
  Object.entries((generatedSidebar as GeneratedSidebar).patterns).map(([slug, chapter]) => [
    slug,
    chapter.problemIds ?? []
  ])
)

let installed = false
let scheduled = false

function readSolvedMap() {
  try {
    const stored = window.localStorage.getItem('dsa-solved')
    return stored ? JSON.parse(stored) as Record<string, boolean> : {}
  } catch {
    return {}
  }
}

function ensureStyles() {
  if (document.getElementById('solved-count-badge-style')) return

  const style = document.createElement('style')
  style.id = 'solved-count-badge-style'
  style.textContent = `
    .solved-badge {
      display: inline-flex;
      align-items: center;
      margin-left: 8px;
      padding: 1px 6px;
      border-radius: 999px;
      background: rgba(21, 128, 61, 0.1);
      color: #15803d;
      font-size: 11px;
      font-weight: 700;
      line-height: 1.4;
      vertical-align: middle;
      white-space: nowrap;
    }
    .dark .solved-badge {
      background: rgba(34, 197, 94, 0.16);
      color: #86efac;
    }
  `
  document.head.appendChild(style)
}

function slugFromSidebarLink(anchor: HTMLAnchorElement) {
  const url = new URL(anchor.href)
  if (url.hash) return undefined

  const pathname = url.pathname.replace(/\/$/, '')
  const match = pathname.match(/\/patterns\/([^/]+)$/)
  return match?.[1]
}

function updateBadges() {
  if (typeof document === 'undefined') return

  ensureStyles()
  const solved = readSolvedMap()

  document.querySelectorAll<HTMLAnchorElement>('.VPSidebar a[href]').forEach((anchor) => {
    const slug = slugFromSidebarLink(anchor)
    if (!slug) return

    const problemIds = patternProblems[slug]
    if (!problemIds?.length) return

    const solvedCount = problemIds.filter((id) => solved[id] === true).length
    const target = anchor.querySelector<HTMLElement>('.text') ?? anchor
    let badge = target.querySelector<HTMLSpanElement>('.solved-badge')

    if (!badge) {
      badge = document.createElement('span')
      badge.className = 'solved-badge'
      target.appendChild(badge)
    }

    badge.textContent = `${solvedCount}/${problemIds.length}`
  })
}

function scheduleUpdate() {
  if (scheduled) return
  scheduled = true
  window.requestAnimationFrame(() => {
    scheduled = false
    updateBadges()
  })
}

export function installSolvedCountBadges(router?: {
  onAfterRouteChanged?: (to: string) => void
}) {
  if (installed || typeof window === 'undefined') return
  installed = true

  const previousAfterRouteChanged = router?.onAfterRouteChanged
  if (router) {
    router.onAfterRouteChanged = (to: string) => {
      previousAfterRouteChanged?.(to)
      scheduleUpdate()
    }
  }

  window.addEventListener('storage', (event) => {
    if (event.key === 'dsa-solved') scheduleUpdate()
  })
  document.addEventListener('change', () => window.setTimeout(scheduleUpdate, 0))

  const observer = new MutationObserver(scheduleUpdate)
  observer.observe(document.body, { childList: true, subtree: true })

  scheduleUpdate()
}
