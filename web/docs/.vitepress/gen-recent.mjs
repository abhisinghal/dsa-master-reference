import { execFileSync } from 'node:child_process'
import { existsSync, mkdirSync, readFileSync, writeFileSync } from 'node:fs'
import path from 'node:path'
import { fileURLToPath } from 'node:url'

const here = path.dirname(fileURLToPath(import.meta.url))
const docsDir = path.resolve(here, '..')
const webDir = path.resolve(docsDir, '..')
const repoRoot = path.resolve(webDir, '..')
const sourceDir = path.join(repoRoot, 'gen', 'src2')
const outputFile = path.join(docsDir, 'public', 'recent.json')

const mapping = {
  '00-front.md': 'foundations/how-to-use.md',
  '01-playbook.md': 'foundations/playbook.md',
  '02-glossary.md': 'foundations/glossary.md',
  '03-roadmap.md': 'foundations/roadmap.md',
  '04-part1.md': null,
  '06-java-ds.md': 'foundations/java-primer.md',
  '07-java-gotchas.md': 'foundations/java-gotchas.md',
  '10-complexity.md': 'foundations/complexity.md',
  '11-debugging.md': 'foundations/debugging.md',
  '20-patterns.md': 'patterns/index.md',
  '21-sliding-window.md': 'patterns/sliding-window.md',
  '22-two-pointers.md': 'patterns/two-pointers.md',
  '23-fast-slow.md': 'patterns/fast-slow.md',
  '24-prefix-sum.md': 'patterns/prefix-sum.md',
  '25-hashing.md': 'patterns/hashing.md',
  '26-monotonic-stack.md': 'patterns/monotonic-stack.md',
  '27-binary-search.md': 'patterns/binary-search.md',
  '28-bs-on-answer.md': 'patterns/bs-on-answer.md',
  '29-top-k-heap.md': 'patterns/top-k-heap.md',
  '30-k-way-merge.md': 'patterns/k-way-merge.md',
  '31-merge-intervals.md': 'patterns/merge-intervals.md',
  '32-sweep-line.md': 'patterns/sweep-line.md',
  '33-topological-sort.md': 'patterns/topological-sort.md',
  '34-union-find.md': 'patterns/union-find.md',
  '35-greedy.md': 'patterns/greedy.md',
  '36-backtracking.md': 'patterns/backtracking.md',
  '37-divide-conquer.md': 'patterns/divide-conquer.md',
  '38-dp.md': 'patterns/dp.md',
  '39-trie-pattern.md': 'patterns/trie-pattern.md',
  '40-bit-manip.md': 'patterns/bit-manip.md',
  '41-quickselect.md': 'patterns/quickselect.md',
  '42-math.md': 'patterns/math.md',
  '44-design.md': 'patterns/design.md',
  '50-arrays.md': 'data-structures/arrays.md',
  '52-strings.md': 'data-structures/strings.md',
  '56-linked-lists.md': 'data-structures/linked-lists.md',
  '58-stacks-queues.md': 'data-structures/stacks-queues.md',
  '60-trees.md': 'data-structures/trees.md',
  '62-heaps.md': 'data-structures/heaps.md',
  '64-trie.md': 'data-structures/trie.md',
  '66-graphs.md': 'data-structures/graphs.md',
  '68-segment-fenwick.md': 'data-structures/segment-fenwick.md',
  '90-cheatsheets.md': 'appendix/cheatsheets.md',
  '95-self-check.md': 'appendix/self-check.md',
  '96-problem-index.md': 'appendix/problem-index.md',
  '97-practice-solutions.md': 'appendix/practice-solutions.md',
  '98-mock-transcripts.md': 'appendix/mock-transcripts.md',
  '99-traps-catalog.md': 'appendix/traps-catalog.md'
}

const entities = {
  '&amp;': '&',
  '&quot;': '"',
  '&#39;': "'",
  '&apos;': "'",
  '&lt;': '<',
  '&gt;': '>',
  '&ndash;': '–',
  '&mdash;': '—'
}

function fallbackTitle(fileName) {
  return path
    .parse(fileName)
    .name
    .replace(/^\d+-/, '')
    .split('-')
    .map((word) => word.charAt(0).toUpperCase() + word.slice(1))
    .join(' ')
}

function decodeTitle(title) {
  return title
    .replace(/<[^>]*>/g, '')
    .replace(/\*\*/g, '')
    .replace(/&(?:amp|quot|#39|apos|lt|gt|ndash|mdash);/g, (entity) => entities[entity] ?? entity)
    .trim()
}

function titleFor(fileName) {
  const sourceFile = path.join(sourceDir, fileName)
  if (!existsSync(sourceFile)) return fallbackTitle(fileName)

  const h1 = readFileSync(sourceFile, 'utf8')
    .split(/\r?\n/)
    .find((line) => /^#\s+/.test(line))

  return h1 ? decodeTitle(h1.replace(/^#\s+/, '')) : fallbackTitle(fileName)
}

function urlFor(fileName) {
  const destination = mapping[fileName]
  if (!destination) return null

  const normalized = destination.replace(/\\/g, '/').replace(/\.md$/, '').replace(/\/index$/, '/')
  return `/${normalized}`
}

function fileNameFromGitPath(gitPath) {
  const normalized = gitPath.trim().replace(/\\/g, '/')
  if (!normalized.startsWith('gen/src2/') || !normalized.endsWith('.md')) return null
  return normalized.split('/').pop()
}

export function generateRecentUpdates(limit = 6) {
  mkdirSync(path.dirname(outputFile), { recursive: true })

  let log
  try {
    log = execFileSync(
      'git',
      ['log', '--format=%H|%ct|%s', '--name-only', '--diff-filter=AM', '--', '..\\gen\\src2\\'],
      { cwd: webDir, encoding: 'utf8' }
    )
  } catch (error) {
    console.warn(`[recent] Unable to read git history: ${error.message}`)
    writeFileSync(outputFile, '[]\n')
    return []
  }

  const recent = []
  const seen = new Set()
  let currentCommit = null

  for (const rawLine of log.split(/\r?\n/)) {
    const line = rawLine.trim()
    if (!line) continue

    const commit = line.match(/^([0-9a-f]{40})\|(\d+)\|(.*)$/)
    if (commit) {
      currentCommit = {
        hash: commit[1],
        timestamp: Number(commit[2]),
        subject: commit[3]
      }
      continue
    }

    if (!currentCommit) continue

    const fileName = fileNameFromGitPath(line)
    if (!fileName || seen.has(fileName)) continue

    const url = urlFor(fileName)
    if (!url) continue

    seen.add(fileName)
    recent.push({
      title: titleFor(fileName),
      url,
      updated: new Date(currentCommit.timestamp * 1000).toISOString()
    })

    if (recent.length >= limit) break
  }

  writeFileSync(outputFile, `${JSON.stringify(recent, null, 2)}\n`)
  return recent
}

if (process.argv[1] && path.resolve(process.argv[1]) === fileURLToPath(import.meta.url)) {
  const recent = generateRecentUpdates()
  console.log(`[recent] Wrote ${recent.length} updates to ${outputFile}`)
}
