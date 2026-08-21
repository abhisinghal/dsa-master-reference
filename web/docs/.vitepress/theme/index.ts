import { h } from 'vue'
import DefaultTheme from 'vitepress/theme'
import Callout from './Callout.vue'
import CodeTabs from './CodeTabs.vue'
import ProgressCheck from './ProgressCheck.vue'
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
  }
}
