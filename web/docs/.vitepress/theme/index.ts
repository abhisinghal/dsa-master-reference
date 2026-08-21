import { h } from 'vue'
import DefaultTheme from 'vitepress/theme'
import Callout from './Callout.vue'
import CodeTabs from './CodeTabs.vue'
import ProgressCheck from './ProgressCheck.vue'
import JavaRunner from './JavaRunner.vue'
import SlidingWindowAnim from './SlidingWindowAnim.vue'
import MonoStackAnim from './MonoStackAnim.vue'
import UnionFindAnim from './UnionFindAnim.vue'
import SweepLineAnim from './SweepLineAnim.vue'
import DivideConquerAnim from './DivideConquerAnim.vue'
import QuickselectAnim from './QuickselectAnim.vue'
import BacktrackingAnim from './BacktrackingAnim.vue'
import Breadcrumbs from './Breadcrumbs.vue'
import ReadingTime from './ReadingTime.vue'
import RecentUpdates from './RecentUpdates.vue'
import { installSolvedCountBadges } from './SolvedCountBadge'
import './style.css'

export default {
  extends: DefaultTheme,
  Layout: () => {
    return h(DefaultTheme.Layout, null, {
      'doc-before': () => h(Breadcrumbs)
    })
  },
  enhanceApp({ app, router }) {
    app.component('Callout', Callout)
    app.component('CodeTabs', CodeTabs)
    app.component('ProgressCheck', ProgressCheck)
    app.component('JavaRunner', JavaRunner)
    app.component('SlidingWindowAnim', SlidingWindowAnim)
    app.component('MonoStackAnim', MonoStackAnim)
    app.component('UnionFindAnim', UnionFindAnim)
    app.component('SweepLineAnim', SweepLineAnim)
    app.component('DivideConquerAnim', DivideConquerAnim)
    app.component('QuickselectAnim', QuickselectAnim)
    app.component('BacktrackingAnim', BacktrackingAnim)
    app.component('Breadcrumbs', Breadcrumbs)
    app.component('ReadingTime', ReadingTime)
    app.component('RecentUpdates', RecentUpdates)
    installSolvedCountBadges(router)
  }
}
