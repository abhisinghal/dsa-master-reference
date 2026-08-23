<script setup lang="ts">
import { ref } from 'vue'

const props = defineProps<{
  title?: string
  duration?: string
  youtubeId?: string
  loomEmbed?: string
  patternName?: string
}>()

const playing = ref(false)

function play() { playing.value = true }
</script>

<template>
  <div class="video-panel">
    <div v-if="!playing" class="video-thumb" @click="play">
      <div class="video-overlay">
        <div class="play-btn">▶</div>
        <div v-if="props.duration" class="video-duration">{{ props.duration }}</div>
      </div>
      <div class="video-info">
        <div class="video-badge">Pattern Video</div>
        <div class="video-title">{{ props.title || `${props.patternName} — Interactive Walkthrough` }}</div>
        <div class="video-desc">
          <template v-if="props.youtubeId || props.loomEmbed">
            Click to play the walkthrough.
          </template>
          <template v-else>
            🎬 Video walkthrough coming soon.
            <a href="/dsa-master-reference/" @click.stop>Subscribe</a>
            to be notified when it drops.
          </template>
        </div>
      </div>
    </div>
    <div v-else class="video-player">
      <iframe
        v-if="props.youtubeId"
        :src="`https://www.youtube.com/embed/${props.youtubeId}?autoplay=1`"
        title="YouTube"
        frameborder="0"
        allow="autoplay; encrypted-media; picture-in-picture"
        allowfullscreen
      ></iframe>
      <div v-else-if="props.loomEmbed" v-html="props.loomEmbed"></div>
      <div v-else class="video-tbd">
        <div class="tbd-icon">📼</div>
        <div class="tbd-text">Video is being produced.</div>
      </div>
    </div>
  </div>
</template>

<style scoped>
.video-panel {
  border: 1px solid var(--vp-c-divider);
  border-radius: 12px;
  margin: 24px 0;
  overflow: hidden;
  background: var(--vp-c-bg-soft);
}
.video-thumb {
  position: relative;
  cursor: pointer;
  background: linear-gradient(135deg, #1e293b, #0f172a);
  display: flex;
  flex-direction: column;
  transition: transform 0.15s;
}
.video-thumb:hover { transform: scale(1.005); }
.video-overlay {
  position: relative;
  height: 180px;
  display: flex;
  align-items: center;
  justify-content: center;
  background: radial-gradient(ellipse at center, rgba(59,130,246,0.35), transparent 70%);
}
.play-btn {
  width: 72px;
  height: 72px;
  border-radius: 50%;
  background: rgba(255,255,255,0.95);
  color: #ef4444;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 30px;
  padding-left: 6px;
  box-shadow: 0 8px 24px rgba(0,0,0,0.4);
}
.video-duration {
  position: absolute;
  bottom: 12px;
  right: 12px;
  padding: 3px 8px;
  background: rgba(0,0,0,0.75);
  color: white;
  font-size: 11px;
  font-weight: 600;
  border-radius: 4px;
}
.video-info {
  padding: 14px 18px;
  background: var(--vp-c-bg);
}
.video-badge {
  display: inline-block;
  font-size: 10px;
  letter-spacing: 0.08em;
  text-transform: uppercase;
  padding: 3px 8px;
  border-radius: 999px;
  background: rgba(239,68,68,0.15);
  color: #ef4444;
  font-weight: 700;
  margin-bottom: 6px;
}
.video-title {
  font-size: 15px;
  font-weight: 700;
  color: var(--vp-c-text-1);
}
.video-desc {
  font-size: 12.5px;
  color: var(--vp-c-text-2);
  margin-top: 4px;
}
.video-desc a { color: var(--vp-c-brand-1); font-weight: 500; }
.video-player {
  aspect-ratio: 16 / 9;
  background: black;
}
.video-player iframe { width: 100%; height: 100%; border: 0; }
.video-tbd {
  height: 100%;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  color: white;
  gap: 12px;
}
.tbd-icon { font-size: 48px; }
.tbd-text { font-size: 14px; color: rgba(255,255,255,0.7); }
</style>
