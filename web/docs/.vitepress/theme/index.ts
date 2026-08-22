import { h } from 'vue'
import DefaultTheme from 'vitepress/theme'
import Callout from './Callout.vue'
import CodeTabs from './CodeTabs.vue'
import ProgressCheck from './ProgressCheck.vue'
import JavaRunner from './JavaRunner.vue'
import SlidingWindowAnim from './SlidingWindowAnim.vue'
import TwoPointersAnim from './TwoPointersAnim.vue'
import FastSlowAnim from './FastSlowAnim.vue'
import BFSGridAnim from './BFSGridAnim.vue'
import DFSGridAnim from './DFSGridAnim.vue'
import MonoStackAnim from './MonoStackAnim.vue'
import UnionFindAnim from './UnionFindAnim.vue'
import SweepLineAnim from './SweepLineAnim.vue'
import DivideConquerAnim from './DivideConquerAnim.vue'
import QuickselectAnim from './QuickselectAnim.vue'
import BacktrackingAnim from './BacktrackingAnim.vue'
import DpFillAnim from './DpFillAnim.vue'
import TrieWalkAnim from './TrieWalkAnim.vue'
import BinarySearchAnim from './BinarySearchAnim.vue'
import HeapAnim from './HeapAnim.vue'
import Breadcrumbs from './Breadcrumbs.vue'
import ReadingTime from './ReadingTime.vue'
import RecentUpdates from './RecentUpdates.vue'
import Quiz from './Quiz.vue'
import StepStrip from './StepStrip.vue'
import TwoSumStepStrip from './TwoSumStepStrip.vue'
import Icon from './Icon.vue'
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
    app.component('TwoPointersAnim', TwoPointersAnim)
    app.component('FastSlowAnim', FastSlowAnim)
    app.component('BFSGridAnim', BFSGridAnim)
    app.component('DFSGridAnim', DFSGridAnim)
    app.component('MonoStackAnim', MonoStackAnim)
    app.component('UnionFindAnim', UnionFindAnim)
    app.component('SweepLineAnim', SweepLineAnim)
    app.component('DivideConquerAnim', DivideConquerAnim)
    app.component('QuickselectAnim', QuickselectAnim)
    app.component('BacktrackingAnim', BacktrackingAnim)
    app.component('DpFillAnim', DpFillAnim)
    app.component('TrieWalkAnim', TrieWalkAnim)
    app.component('BinarySearchAnim', BinarySearchAnim)
    app.component('HeapAnim', HeapAnim)
    app.component('Breadcrumbs', Breadcrumbs)
    app.component('ReadingTime', ReadingTime)
    app.component('RecentUpdates', RecentUpdates)
    app.component('Quiz', Quiz)
    app.component('StepStrip', StepStrip)
    app.component('TwoSumStepStrip', TwoSumStepStrip)
    app.component('Icon', Icon)
    installSolvedCountBadges(router)
  }
}
