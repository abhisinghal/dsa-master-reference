import { defineConfig } from 'vitepress'
import { withMermaid } from 'vitepress-plugin-mermaid'
import { generateRecentUpdates } from './gen-recent.mjs'
import generatedSidebar from './sidebar.generated.json'

type SidebarChapter = {
  items?: { text: string; link: string }[]
}

const sidebarData = generatedSidebar as {
  patterns: Record<string, SidebarChapter>
  dataStructures: Record<string, SidebarChapter>
}

const rCombining = /[\u0300-\u036F]/g
const rAsciiSeparators = /[—–→·]/g
const rNonAsciiSlugChar = /[^a-z0-9]+/g

function slugifyHeading(str: string) {
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

function nestedPattern(text: string, slug: string) {
  const items = sidebarData.patterns[slug]?.items ?? []
  return items.length
    ? { text, link: `/patterns/${slug}`, collapsed: true, items }
    : { text, link: `/patterns/${slug}` }
}

function nestedDataStructure(text: string, slug: string) {
  const items = sidebarData.dataStructures[slug]?.items ?? []
  return items.length
    ? { text, link: `/data-structures/${slug}`, collapsed: true, items }
    : { text, link: `/data-structures/${slug}` }
}

export default withMermaid(defineConfig({
  base: '/dsa-master-reference/',
  title: 'DSA Master Reference',
  description: 'Patterns, invariants, and problems for senior/staff DSA interviews (Java 17)',
  cleanUrls: true,
  ignoreDeadLinks: true,
  sitemap: {
    hostname: 'https://abhisinghal.github.io/dsa-master-reference/'
  },
  head: [
    ['link', { rel: 'icon', href: '/dsa-master-reference/favicon.svg' }],
    ['meta', { name: 'theme-color', content: '#2563eb' }],
    ['script', { src: 'https://cjrtnc.leaningtech.com/3.0/cj3loader.js' }]
  ],
  markdown: {
    lineNumbers: true,
    anchor: {
      slugify: slugifyHeading
    },
    theme: {
      light: 'github-light',
      dark: 'github-dark-high-contrast'
    }
  },
  vite: {
    plugins: [
      {
        name: 'generate-recent-updates',
        apply: 'build',
        buildStart() {
          generateRecentUpdates()
        }
      }
    ]
  },
  themeConfig: {
    logo: '/logo.svg',
    nav: [
      { text: 'Home', link: '/' },
      { text: 'Roadmap', link: '/foundations/roadmap' },
      { text: 'Patterns', link: '/patterns/' },
      { text: 'Data Structures', link: '/data-structures/' },
      { text: 'Cheat sheets', link: '/appendix/cheatsheets' },
      { text: 'PDF', link: 'https://github.com/abhisinghal/dsa-master-reference/releases' }
    ],
    sidebar: {
      '/foundations/': [
        {
          text: 'Foundations',
          items: [
            { text: 'How to Use This Book', link: '/foundations/how-to-use' },
            { text: 'Interview Playbook', link: '/foundations/playbook' },
            { text: 'Zero-to-Hero Roadmap', link: '/foundations/roadmap' },
            { text: 'Glossary', link: '/foundations/glossary' },
            { text: 'Java Data Structures Primer', link: '/foundations/java-primer' },
            { text: 'Java DSA Gotchas', link: '/foundations/java-gotchas' },
            { text: 'How this compares', link: '/foundations/vs-competitors' },
            { text: 'Complexity Model', link: '/foundations/complexity' },
            { text: 'Debugging DSA Code', link: '/foundations/debugging' }
          ]
        }
      ],
      '/patterns/': [
        {
          text: 'The 21 Core Patterns',
          items: [
            { text: 'Overview', link: '/patterns/' },
            nestedPattern('1. Sliding Window', 'sliding-window'),
            nestedPattern('2. Two Pointers', 'two-pointers'),
            nestedPattern('3. Fast/Slow Pointers', 'fast-slow'),
            nestedPattern('4. Prefix Sum', 'prefix-sum'),
            nestedPattern('5. Hashing', 'hashing'),
            nestedPattern('6. Monotonic Stack', 'monotonic-stack'),
            nestedPattern('7. Binary Search', 'binary-search'),
            nestedPattern('8. Binary Search on Answer', 'bs-on-answer'),
            nestedPattern('9. Top-K / Heap', 'top-k-heap'),
            nestedPattern('10. K-way Merge', 'k-way-merge'),
            nestedPattern('11. Merge Intervals', 'merge-intervals'),
            nestedPattern('12. Sweep Line', 'sweep-line'),
            nestedPattern('13. Topological Sort', 'topological-sort'),
            nestedPattern('14. Union-Find', 'union-find'),
            nestedPattern('15. Greedy', 'greedy'),
            nestedPattern('16. Backtracking', 'backtracking'),
            nestedPattern('17. Divide & Conquer', 'divide-conquer'),
            nestedPattern('18. Dynamic Programming', 'dp'),
            nestedPattern('19. Trie Pattern', 'trie-pattern'),
            nestedPattern('20. Bit Manipulation', 'bit-manip'),
            nestedPattern('21. Quickselect', 'quickselect'),
            nestedPattern('Bonus: Math & Number Theory', 'math'),
            nestedPattern('Bonus: Design', 'design')
          ]
        }
      ],
      '/data-structures/': [
        {
          text: 'Part III — Data Structures in Depth',
          items: [
            { text: 'Overview', link: '/data-structures/' },
            nestedDataStructure('Arrays', 'arrays'),
            nestedDataStructure('Strings', 'strings'),
            nestedDataStructure('Linked Lists', 'linked-lists'),
            nestedDataStructure('Stacks & Queues', 'stacks-queues'),
            nestedDataStructure('Trees', 'trees'),
            nestedDataStructure('Heaps', 'heaps'),
            nestedDataStructure('Trie', 'trie'),
            nestedDataStructure('Graphs', 'graphs'),
            nestedDataStructure('Segment / Fenwick Tree', 'segment-fenwick')
          ]
        }
      ],
      '/appendix/': [
        {
          text: 'Appendix',
          items: [
            { text: 'Cheat Sheets & Templates', link: '/appendix/cheatsheets' },
            { text: 'Self-Check & Drills', link: '/appendix/self-check' },
            { text: 'Master Problem Index', link: '/appendix/problem-index' },
            { text: 'Practice Solutions', link: '/appendix/practice-solutions' },
            { text: 'Mock Interview Transcripts', link: '/appendix/mock-transcripts' },
            { text: 'Traps Catalog', link: '/appendix/traps-catalog' },
            { text: 'Changelog', link: '/appendix/changelog' }
          ]
        }
      ]
    },
    socialLinks: [
      { icon: 'github', link: 'https://github.com/abhisinghal/dsa-master-reference' }
    ],
    footer: {
      message: 'Released under MIT license.',
      copyright: 'Copyright © 2026 Abhishek Singhal'
    },
    search: {
      provider: 'local'
    },
    outline: 2
  }
}))
