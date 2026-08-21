import { h } from 'vue'
import DefaultTheme from 'vitepress/theme'
import Callout from './Callout.vue'
import CodeTabs from './CodeTabs.vue'
import ProgressCheck from './ProgressCheck.vue'
import JavaRunner from './JavaRunner.vue'
import SlidingWindowAnim from './SlidingWindowAnim.vue'
import MonoStackAnim from './MonoStackAnim.vue'
import UnionFindAnim from './UnionFindAnim.vue'
import './style.css'

export default {
  extends: DefaultTheme,
  Layout: () => {
    return h(DefaultTheme.Layout, null, {})
  },
  enhanceApp({ app }) {
    app.component('Callout', Callout)
    app.component('CodeTabs', CodeTabs)
    app.component('ProgressCheck', ProgressCheck)
    app.component('JavaRunner', JavaRunner)
    app.component('SlidingWindowAnim', SlidingWindowAnim)
    app.component('MonoStackAnim', MonoStackAnim)
    app.component('UnionFindAnim', UnionFindAnim)
  }
}
