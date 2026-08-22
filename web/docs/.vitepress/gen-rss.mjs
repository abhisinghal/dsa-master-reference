import { readFileSync, writeFileSync, mkdirSync, existsSync } from 'node:fs'
import path from 'node:path'
import { fileURLToPath } from 'node:url'

const here = path.dirname(fileURLToPath(import.meta.url))
const docsDir = path.resolve(here, '..')
const webDir = path.resolve(docsDir, '..')
const repoRoot = path.resolve(webDir, '..')

const SITE_URL = 'https://abhisinghal.github.io/dsa-master-reference'
const SITE_TITLE = 'DSA Master Reference'
const SITE_DESCRIPTION = 'Java-native DSA interview reference — patterns, canonical problems, animations, and interview-realism content for senior/staff engineers.'
const CHANGELOG_URL = `${SITE_URL}/appendix/changelog.html`

function xmlEscape(s) {
  return String(s)
    .replace(/&/g, '&amp;')
    .replace(/</g, '&lt;')
    .replace(/>/g, '&gt;')
    .replace(/"/g, '&quot;')
    .replace(/'/g, '&apos;')
}

function parseChangelog(md) {
  // Each entry: "### YYYY-MM-DD — Title" then a bullet list until next heading
  const lines = md.split(/\r?\n/)
  const entries = []
  let current = null
  const entryHeadRe = /^###\s+(\d{4}-\d{2}-\d{2})\s+[—–-]\s+(.+?)\s*$/

  for (let i = 0; i < lines.length; i++) {
    const line = lines[i]
    const m = line.match(entryHeadRe)
    if (m) {
      if (current) entries.push(current)
      current = { date: m[1], title: m[2], body: [] }
      continue
    }
    if (current && line.startsWith('## ')) {
      // stop this entry when a new month/section heading appears
      entries.push(current)
      current = null
      continue
    }
    if (current) {
      current.body.push(line)
    }
  }
  if (current) entries.push(current)
  return entries
}

function bodyToHtml(bodyLines) {
  const bullets = bodyLines
    .map((l) => l.trim())
    .filter((l) => l.startsWith('- '))
    .map((l) => l.slice(2))
  if (!bullets.length) return ''
  const items = bullets.map((b) => `<li>${xmlEscape(b)}</li>`).join('')
  return `<ul>${items}</ul>`
}

function rfc822(dateStr) {
  const d = new Date(`${dateStr}T12:00:00Z`)
  return d.toUTCString()
}

function generateRss(entries) {
  const items = entries.slice(0, 40).map((e) => {
    const link = `${CHANGELOG_URL}#${e.date}-${e.title.toLowerCase().replace(/[^a-z0-9]+/g, '-').replace(/^-|-$/g, '')}`
    return `    <item>
      <title>${xmlEscape(e.title)}</title>
      <link>${xmlEscape(link)}</link>
      <guid isPermaLink="false">dsa-master-reference-${e.date}-${xmlEscape(e.title).slice(0, 40)}</guid>
      <pubDate>${rfc822(e.date)}</pubDate>
      <description><![CDATA[${bodyToHtml(e.body)}]]></description>
    </item>`
  }).join('\n')

  const now = new Date().toUTCString()
  return `<?xml version="1.0" encoding="UTF-8"?>
<rss version="2.0" xmlns:atom="http://www.w3.org/2005/Atom">
  <channel>
    <title>${xmlEscape(SITE_TITLE)}</title>
    <link>${SITE_URL}</link>
    <atom:link href="${SITE_URL}/rss.xml" rel="self" type="application/rss+xml" />
    <description>${xmlEscape(SITE_DESCRIPTION)}</description>
    <language>en-us</language>
    <lastBuildDate>${now}</lastBuildDate>
    <ttl>1440</ttl>
${items}
  </channel>
</rss>
`
}

export function generateChangelogRss() {
  const changelogPath = path.join(docsDir, 'appendix', 'changelog.md')
  if (!existsSync(changelogPath)) {
    console.warn(`[gen-rss] Changelog not found at ${changelogPath}; skipping RSS generation.`)
    return
  }
  const md = readFileSync(changelogPath, 'utf-8')
  const entries = parseChangelog(md)
  const rss = generateRss(entries)
  const publicDir = path.join(docsDir, 'public')
  if (!existsSync(publicDir)) mkdirSync(publicDir, { recursive: true })
  const outPath = path.join(publicDir, 'rss.xml')
  writeFileSync(outPath, rss, 'utf-8')
  console.log(`[gen-rss] Wrote ${entries.length} entries to ${path.relative(repoRoot, outPath)}`)
}
