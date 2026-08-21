import { readFileSync, readdirSync, writeFileSync } from 'node:fs'
import path from 'node:path'
import { fileURLToPath } from 'node:url'

const __dirname = path.dirname(fileURLToPath(import.meta.url))
const docsDir = path.resolve(__dirname, '..')
const outputFile = path.join(__dirname, 'sidebar.generated.json')

const rCombining = /[\u0300-\u036F]/g
const rAsciiSeparators = /[—–→·]/g
const rNonAsciiSlugChar = /[^a-z0-9]+/g

function slugify(str) {
  return str
    .normalize('NFKD')
    .replace(rCombining, '')
    .toLowerCase()
    .replace(rAsciiSeparators, '-')
    .replace(rNonAsciiSlugChar, '-')
    .replace(/-{2,}/g, '-')
    .replace(/^-+|-+$/g, '')
    .replace(/^(\d)/, '_$1')
}

function uniqueSlug(base, seen) {
  let slug = base
  let index = 1
  while (seen.has(slug)) {
    slug = `${base}-${index}`
    index += 1
  }
  seen.add(slug)
  return slug
}

function decodeHtmlEntities(value) {
  return value.replace(/&(#x?[0-9a-f]+|[a-z]+);/gi, (entity, code) => {
    const named = {
      amp: '&',
      gt: '>',
      lt: '<',
      quot: '"',
      apos: "'",
      nbsp: ' '
    }
    const lower = code.toLowerCase()
    if (named[lower]) return named[lower]
    if (lower.startsWith('#x')) return String.fromCodePoint(Number.parseInt(lower.slice(2), 16))
    if (lower.startsWith('#')) return String.fromCodePoint(Number.parseInt(lower.slice(1), 10))
    return entity
  })
}

function cleanHeading(raw) {
  return decodeHtmlEntities(
    raw
      .replace(/<span\b[^>]*\bdiff\b[^>]*>.*?<\/span>/gi, '')
      .replace(/<[^>]+>/g, '')
      .replace(/[`*_~]/g, '')
      .replace(/\s+/g, ' ')
      .trim()
  )
}

function anchorHeading(raw) {
  return raw
    .replace(/<[^>]+>/g, '')
    .replace(/[`*_~]/g, '')
    .replace(/\s+/g, ' ')
    .trim()
}

function nextNonBlankLine(lines, startIndex) {
  for (let index = startIndex + 1; index < lines.length; index += 1) {
    const line = lines[index].trim()
    if (line) return line
  }
  return ''
}

function hasLeetCodeMarker(lines, headingIndex) {
  return nextNonBlankLine(lines, headingIndex).startsWith('*[↗ LeetCode:')
}

function progressIdInBlock(lines, startIndex) {
  for (let index = startIndex + 1; index < lines.length; index += 1) {
    if (/^##\s+/.test(lines[index])) return undefined
    const match = lines[index].match(/<ProgressCheck\s+id=["']([^"']+)["']/)
    if (match) return match[1]
  }
  return undefined
}

function chapterFromFile(section, fileName) {
  const slug = fileName.replace(/\.md$/i, '')
  const file = path.join(docsDir, section, fileName)
  const lines = readFileSync(file, 'utf8').split(/\r?\n/)
  const seen = new Set()
  const items = []
  const problemIds = []

  lines.forEach((line, index) => {
    const match = line.match(/^##\s+(.+?)\s*#*\s*$/)
    if (!match) return

    if (!hasLeetCodeMarker(lines, index)) return

    const text = cleanHeading(match[1])
    if (!text) return

    const anchor = uniqueSlug(slugify(anchorHeading(match[1])), seen)
    const progressId = progressIdInBlock(lines, index)
    const item = {
      text,
      link: `/${section}/${slug}#${anchor}`
    }

    if (progressId) {
      item.progressId = progressId
      problemIds.push(progressId)
    }

    items.push(item)
  })

  return { items, problemIds, totalProblems: problemIds.length }
}

function buildSection(section) {
  return Object.fromEntries(
    readdirSync(path.join(docsDir, section))
      .filter((fileName) => fileName.endsWith('.md') && fileName !== 'index.md')
      .sort()
      .map((fileName) => [fileName.replace(/\.md$/i, ''), chapterFromFile(section, fileName)])
  )
}

const sidebar = {
  patterns: buildSection('patterns'),
  dataStructures: buildSection('data-structures')
}

writeFileSync(outputFile, `${JSON.stringify(sidebar, null, 2)}\n`)
console.log(`Generated ${path.relative(process.cwd(), outputFile)}`)
