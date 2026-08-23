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
import CodeTrace from './CodeTrace.vue'
import TrapTrace from './TrapTrace.vue'
import Icon from './Icon.vue'
import ComplexityCurve from './ComplexityCurve.vue'
import PlaybookPhases from './PlaybookPhases.vue'
import DsStateMachine from './DsStateMachine.vue'
import StackQueueOps from './StackQueueOps.vue'
import HeapOps from './HeapOps.vue'
import BstOps from './BstOps.vue'
import TrieOps from './TrieOps.vue'
import UnionFindOps from './UnionFindOps.vue'
import ExamplePreview from './ExamplePreview.vue'
import Hints from './Hints.vue'
import CompanyTags from './CompanyTags.vue'
import EmailCapture from './EmailCapture.vue'
import UserProfile from './UserProfile.vue'
import PatternVideo from './PatternVideo.vue'
import AiCompanion from './AiCompanion.vue'
import PatternProgress from './PatternProgress.vue'
import RelatedPatterns from './RelatedPatterns.vue'
import DueForReview from './DueForReview.vue'
import RelatedProblems from './RelatedProblems.vue'
import FeedbackWidget from './FeedbackWidget.vue'
import ShortcutHint from './ShortcutHint.vue'
import OnboardingTour from './OnboardingTour.vue'
import PageAnalytics from './PageAnalytics.vue'
import MarkSolved from './MarkSolved.vue'
import StorageManager from './StorageManager.vue'
import SocialProof from './SocialProof.vue'
import SupportPanel from './SupportPanel.vue'
import StreakTracker from './StreakTracker.vue'
import ShareButtons from './ShareButtons.vue'
import ReadingProgressBar from './ReadingProgressBar.vue'
import BackToTop from './BackToTop.vue'
import NotFound from './NotFound.vue'
import ProblemStats from './ProblemStats.vue'
import NotificationBell from './NotificationBell.vue'
import PrintButton from './PrintButton.vue'
import InterviewTimer from './InterviewTimer.vue'
import { installSolvedCountBadges } from './SolvedCountBadge'
import './style.css'

export default {
  extends: DefaultTheme,
  NotFound,
  Layout: () => {
    return h(DefaultTheme.Layout, null, {
      'doc-before': () => h(Breadcrumbs),
      'layout-top': () => h(ReadingProgressBar),
      'layout-bottom': () => [h(ShortcutHint), h(OnboardingTour), h(PageAnalytics), h(BackToTop), h(NotificationBell)],
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
    app.component('CodeTrace', CodeTrace)
    app.component('TrapTrace', TrapTrace)
    app.component('Icon', Icon)
    app.component('ComplexityCurve', ComplexityCurve)
    app.component('PlaybookPhases', PlaybookPhases)
    app.component('DsStateMachine', DsStateMachine)
    app.component('StackQueueOps', StackQueueOps)
    app.component('HeapOps', HeapOps)
    app.component('BstOps', BstOps)
    app.component('TrieOps', TrieOps)
    app.component('UnionFindOps', UnionFindOps)
    app.component('ExamplePreview', ExamplePreview)
    app.component('Hints', Hints)
    app.component('CompanyTags', CompanyTags)
    app.component('EmailCapture', EmailCapture)
    app.component('UserProfile', UserProfile)
    app.component('PatternVideo', PatternVideo)
    app.component('AiCompanion', AiCompanion)
    app.component('PatternProgress', PatternProgress)
    app.component('RelatedPatterns', RelatedPatterns)
    app.component('DueForReview', DueForReview)
    app.component('RelatedProblems', RelatedProblems)
    app.component('FeedbackWidget', FeedbackWidget)
    app.component('ShortcutHint', ShortcutHint)
    app.component('OnboardingTour', OnboardingTour)
    app.component('PageAnalytics', PageAnalytics)
    app.component('MarkSolved', MarkSolved)
    app.component('StorageManager', StorageManager)
    app.component('SocialProof', SocialProof)
    app.component('SupportPanel', SupportPanel)
    app.component('StreakTracker', StreakTracker)
    app.component('ShareButtons', ShareButtons)
    app.component('ReadingProgressBar', ReadingProgressBar)
    app.component('BackToTop', BackToTop)
    app.component('NotFound', NotFound)
    app.component('ProblemStats', ProblemStats)
    app.component('NotificationBell', NotificationBell)
    app.component('PrintButton', PrintButton)
    app.component('InterviewTimer', InterviewTimer)
    installSolvedCountBadges(router)
  }
}
