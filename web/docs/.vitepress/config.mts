import { defineConfig } from 'vitepress'
import { withMermaid } from 'vitepress-plugin-mermaid'

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
    ['meta', { name: 'theme-color', content: '#2563eb' }]
  ],
  markdown: {
    lineNumbers: true,
    theme: {
      light: 'github-light',
      dark: 'github-dark'
    }
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
            { text: '1. Sliding Window', link: '/patterns/sliding-window' },
            { text: '2. Two Pointers', link: '/patterns/two-pointers' },
            { text: '3. Fast/Slow Pointers', link: '/patterns/fast-slow' },
            { text: '4. Prefix Sum', link: '/patterns/prefix-sum' },
            { text: '5. Hashing', link: '/patterns/hashing' },
            { text: '6. Monotonic Stack', link: '/patterns/monotonic-stack' },
            { text: '7. Binary Search', link: '/patterns/binary-search' },
            { text: '8. Binary Search on Answer', link: '/patterns/bs-on-answer' },
            { text: '9. Top-K / Heap', link: '/patterns/top-k-heap' },
            { text: '10. K-way Merge', link: '/patterns/k-way-merge' },
            { text: '11. Merge Intervals', link: '/patterns/merge-intervals' },
            { text: '12. Sweep Line', link: '/patterns/sweep-line' },
            { text: '13. Topological Sort', link: '/patterns/topological-sort' },
            { text: '14. Union-Find', link: '/patterns/union-find' },
            { text: '15. Greedy', link: '/patterns/greedy' },
            { text: '16. Backtracking', link: '/patterns/backtracking' },
            { text: '17. Divide & Conquer', link: '/patterns/divide-conquer' },
            { text: '18. Dynamic Programming', link: '/patterns/dp' },
            { text: '19. Trie Pattern', link: '/patterns/trie-pattern' },
            { text: '20. Bit Manipulation', link: '/patterns/bit-manip' },
            { text: '21. Quickselect', link: '/patterns/quickselect' },
            { text: 'Bonus: Math & Number Theory', link: '/patterns/math' },
            { text: 'Bonus: Design', link: '/patterns/design' }
          ]
        }
      ],
      '/data-structures/': [
        {
          text: 'Part III — Data Structures in Depth',
          items: [
            { text: 'Overview', link: '/data-structures/' },
            { text: 'Arrays', link: '/data-structures/arrays' },
            { text: 'Strings', link: '/data-structures/strings' },
            { text: 'Linked Lists', link: '/data-structures/linked-lists' },
            { text: 'Stacks & Queues', link: '/data-structures/stacks-queues' },
            { text: 'Trees', link: '/data-structures/trees' },
            { text: 'Heaps', link: '/data-structures/heaps' },
            { text: 'Trie', link: '/data-structures/trie' },
            { text: 'Graphs', link: '/data-structures/graphs' },
            { text: 'Segment / Fenwick Tree', link: '/data-structures/segment-fenwick' }
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
            { text: 'Traps Catalog', link: '/appendix/traps-catalog' }
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
