<script setup lang="ts">
const props = defineProps<{
  companies: string
}>()

const list = () => (props.companies || '')
  .split(',')
  .map(s => s.trim())
  .filter(Boolean)

const COLORS: Record<string, string> = {
  meta: '#0668E1',
  google: '#EA4335',
  amazon: '#FF9900',
  microsoft: '#00A4EF',
  apple: '#000000',
  netflix: '#E50914',
  uber: '#000000',
  linkedin: '#0A66C2',
  adobe: '#FA0F00',
  atlassian: '#0052CC',
  bloomberg: '#000000',
  oracle: '#F80000',
  salesforce: '#00A1E0',
  tesla: '#CC0000',
  twitter: '#1DA1F2',
  x: '#000000',
  paypal: '#003087',
  stripe: '#635BFF',
  airbnb: '#FF5A5F',
  goldman: '#7399C6',
  jpmorgan: '#005EB8',
  citadel: '#000000',
  visa: '#1A1F71',
  ibm: '#054ADA',
  intel: '#0071C5',
  nvidia: '#76B900',
  cisco: '#1BA0D7',
  sap: '#0FAAFF',
  spotify: '#1DB954',
  yelp: '#D32323',
  yahoo: '#5F01D1',
  snap: '#FFFC00',
  robinhood: '#00C805',
  reddit: '#FF4500',
  pinterest: '#E60023',
  zoom: '#2D8CFF',
  slack: '#4A154B',
  square: '#3E4348',
  docusign: '#FFCC22',
  vmware: '#7B7B7B',
  intuit: '#365EBF',
  ebay: '#E53238',
  dropbox: '#0061FF',
  lyft: '#FF00BF',
  pinterest_alt: '#E60023',
  workday: '#0A5A9E',
  servicenow: '#81B5A1',
  quora: '#B92B27',
  splunk: '#00A2D4',
  akamai: '#0091C7',
  huawei: '#EF3B24',
  bytedance: '#000000',
  tiktok: '#000000',
  tencent: '#0F44FF',
  alibaba: '#FF6A00',
  baidu: '#2932E1',
  didi: '#FF6633',
  wechat: '#09B83E',
  jd: '#E1251B',
  meituan: '#FFC300',
  xiaomi: '#FF6900',
  swiggy: '#FC8019',
  zomato: '#E23744',
  flipkart: '#2874F0',
  paytm: '#20336B',
  ola: '#000000',
  freshworks: '#2986FE',
  razorpay: '#1D3AB9',
  cred: '#000000',
  phonepe: '#5F259F',
  makemytrip: '#EB2226',
}

function colorFor(name: string) {
  const key = name.toLowerCase().replace(/[^a-z]/g, '')
  return COLORS[key] || '#64748b'
}
</script>

<template>
  <div class="ct-row">
    <span class="ct-label">Asked at</span>
    <span
      v-for="c in list()"
      :key="c"
      class="ct-tag"
      :style="{
        color: colorFor(c),
        borderColor: colorFor(c) + '40',
        background: colorFor(c) + '10',
      }"
    >{{ c }}</span>
  </div>
</template>

<style scoped>
.ct-row {
  display: inline-flex;
  align-items: center;
  gap: 6px;
  flex-wrap: wrap;
  margin: 4px 0 12px;
  padding: 6px 10px;
  background: var(--vp-c-bg-soft);
  border-radius: 8px;
  border: 1px dashed var(--vp-c-divider);
}
.ct-label {
  font-size: 10px;
  text-transform: uppercase;
  letter-spacing: 0.06em;
  color: var(--vp-c-text-3);
  font-weight: 600;
}
.ct-tag {
  font-size: 11px;
  font-weight: 700;
  padding: 3px 8px;
  border: 1.5px solid;
  border-radius: 999px;
  white-space: nowrap;
}
</style>
