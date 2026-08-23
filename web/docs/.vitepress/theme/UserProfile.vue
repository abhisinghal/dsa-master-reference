<script setup lang="ts">
import { ref, computed, onMounted } from 'vue'

/**
 * Anonymous, browser-local user "account" that syncs progress across tabs
 * and pages via localStorage. No backend required. Provides the UX affordance
 * of accounts (display name, avatar initial, progress dashboard) without
 * needing Supabase/Firebase for the first release.
 */

const STORAGE_KEY = 'dsa-user-profile'

interface Profile {
  name: string
  createdAt: string
  progress: {
    solved: string[]
    quizzed: string[]
  }
}

function newProfile(name: string): Profile {
  return { name, createdAt: new Date().toISOString(), progress: { solved: [], quizzed: [] } }
}

const profile = ref<Profile | null>(null)
const nameInput = ref('')
const showEditor = ref(false)

onMounted(() => {
  try {
    const raw = localStorage.getItem(STORAGE_KEY)
    if (raw) profile.value = JSON.parse(raw)
  } catch (e) {}
})

function save(p: Profile) {
  profile.value = p
  try { localStorage.setItem(STORAGE_KEY, JSON.stringify(p)) } catch (e) {}
}

function createProfile() {
  if (!nameInput.value.trim()) return
  save(newProfile(nameInput.value.trim()))
  showEditor.value = false
  nameInput.value = ''
}

function signOut() {
  try { localStorage.removeItem(STORAGE_KEY) } catch (e) {}
  profile.value = null
}

const initial = computed(() => profile.value?.name?.[0]?.toUpperCase() ?? '?')
const solvedCount = computed(() => {
  const solved = [] as string[]
  try {
    for (let i = 0; i < localStorage.length; i++) {
      const k = localStorage.key(i) || ''
      if (k.startsWith('dsa-solved:') && localStorage.getItem(k) === 'true') solved.push(k)
    }
  } catch (e) {}
  return solved.length
})
</script>

<template>
  <div class="up-wrap">
    <template v-if="profile">
      <div class="up-card">
        <div class="up-avatar">{{ initial }}</div>
        <div class="up-info">
          <div class="up-name">{{ profile.name }}</div>
          <div class="up-meta">
            Solved: <strong>{{ solvedCount }}</strong> problems
            <span class="up-dot">·</span>
            Joined {{ new Date(profile.createdAt).toLocaleDateString() }}
          </div>
        </div>
        <button class="up-btn ghost" @click="signOut" title="Clear local profile">Sign out</button>
      </div>
    </template>
    <template v-else>
      <div class="up-empty">
        <div class="up-empty-icon">🎯</div>
        <div class="up-empty-text">
          <div class="up-empty-title">Track your progress</div>
          <div class="up-empty-sub">Create a browser-local profile — no email required. Progress syncs across all pages you visit.</div>
        </div>
        <button v-if="!showEditor" class="up-btn" @click="showEditor = true">Start tracking</button>
        <form v-else class="up-form" @submit.prevent="createProfile">
          <input v-model="nameInput" type="text" placeholder="Your name" class="up-input" autofocus />
          <button type="submit" class="up-btn">Create</button>
        </form>
      </div>
    </template>
  </div>
</template>

<style scoped>
.up-wrap { margin: 20px 0; }
.up-card {
  display: flex;
  gap: 14px;
  align-items: center;
  padding: 16px 20px;
  border: 1px solid var(--vp-c-divider);
  border-radius: 12px;
  background: var(--vp-c-bg-soft);
}
.up-avatar {
  width: 44px;
  height: 44px;
  border-radius: 50%;
  background: linear-gradient(135deg, var(--vp-c-brand-1), var(--vp-c-brand-2));
  color: white;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 18px;
  font-weight: 700;
  flex-shrink: 0;
}
.up-info { flex: 1; }
.up-name { font-size: 15px; font-weight: 700; color: var(--vp-c-text-1); }
.up-meta { font-size: 12px; color: var(--vp-c-text-2); margin-top: 3px; }
.up-dot { padding: 0 4px; color: var(--vp-c-text-3); }
.up-btn {
  padding: 8px 16px;
  border: 1px solid var(--vp-c-brand-1);
  border-radius: 6px;
  background: var(--vp-c-brand-1);
  color: white;
  font-size: 13px;
  font-weight: 500;
  cursor: pointer;
  transition: all 0.15s;
}
.up-btn.ghost { background: transparent; color: var(--vp-c-text-1); border-color: var(--vp-c-divider); }
.up-btn:hover:not(.ghost) { background: var(--vp-c-brand-2); border-color: var(--vp-c-brand-2); }
.up-btn.ghost:hover { border-color: var(--vp-c-brand-1); color: var(--vp-c-brand-1); }
.up-empty {
  display: flex;
  align-items: center;
  gap: 16px;
  padding: 20px;
  border: 1px dashed var(--vp-c-divider);
  border-radius: 12px;
  background: var(--vp-c-bg-soft);
  flex-wrap: wrap;
}
.up-empty-icon { font-size: 32px; }
.up-empty-text { flex: 1; min-width: 200px; }
.up-empty-title { font-size: 15px; font-weight: 700; color: var(--vp-c-text-1); }
.up-empty-sub { font-size: 12px; color: var(--vp-c-text-2); margin-top: 2px; }
.up-form { display: flex; gap: 6px; }
.up-input {
  padding: 8px 12px;
  border: 1px solid var(--vp-c-divider);
  border-radius: 6px;
  background: var(--vp-c-bg);
  color: var(--vp-c-text-1);
  font-size: 13px;
}
</style>
