import { defineConfig } from 'vitepress'
import { withMermaid } from 'vitepress-plugin-mermaid'
import { generateRecentUpdates } from './gen-recent.mjs'
import { generateChangelogRss } from './gen-rss.mjs'
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
    ['link', { rel: 'alternate', type: 'application/rss+xml', title: 'DSA Master Reference changelog', href: '/dsa-master-reference/rss.xml' }],
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
          generateChangelogRss()
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
      { text: 'Practice', link: '/problems/' },
      { text: 'System Design', link: '/system-design/' },
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
      '/system-design/': [
        {
          text: 'Part IV — System Design',
          items: [
            { text: 'Fundamentals', link: '/system-design/' }
          ]
        }
      ],
      '/problems/': [
        {
          text: 'Practice — 21 Multi-Approach Deep Dives',
          items: [
            { text: 'Overview', link: '/problems/' },
            { text: '1. Sliding Window — Longest Substring', link: '/problems/sliding-window-longest-substring' },
            { text: '2. Two Pointers — Container With Most Water', link: '/problems/two-pointers-container-with-most-water' },
            { text: '3. Fast/Slow — Linked List Cycle II', link: '/problems/fast-slow-linked-list-cycle-ii' },
            { text: '4. Prefix Sum — Subarray Sum Equals K', link: '/problems/prefix-sum-subarray-sum-equals-k' },
            { text: '5. Hashing — Two Sum', link: '/problems/hashing-two-sum' },
            { text: '6. Monotonic Stack — Daily Temperatures', link: '/problems/monotonic-stack-daily-temperatures' },
            { text: '7. Binary Search — Rotated Sorted', link: '/problems/binary-search-rotated-sorted' },
            { text: '8. BS on Answer — Koko Bananas', link: '/problems/bs-on-answer-koko-bananas' },
            { text: '9. Top-K / Heap — Top K Frequent', link: '/problems/top-k-frequent-elements' },
            { text: '10. K-way Merge — Merge K Lists', link: '/problems/k-way-merge-k-sorted-lists' },
            { text: '11. Merge Intervals', link: '/problems/merge-intervals-classic' },
            { text: '12. Sweep Line — Meeting Rooms II', link: '/problems/sweep-line-meeting-rooms-ii' },
            { text: '13. Topo Sort — Course Schedule II', link: '/problems/topological-sort-course-schedule' },
            { text: '14. Union-Find — Number of Provinces', link: '/problems/union-find-number-of-provinces' },
            { text: '15. Greedy — Jump Game II', link: '/problems/greedy-jump-game-ii' },
            { text: '16. Backtracking — N-Queens', link: '/problems/backtracking-n-queens' },
            { text: '17. Divide & Conquer — Inversions', link: '/problems/divide-conquer-inversions' },
            { text: '18. DP — House Robber', link: '/problems/dp-house-robber' },
            { text: '19. Trie — Word Search II', link: '/problems/trie-word-search-ii' },
            { text: '20. Bit Manipulation — Single Number', link: '/problems/bit-manip-single-number' },
            { text: '21. Quickselect — Kth Largest', link: '/problems/quickselect-kth-largest' }
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
