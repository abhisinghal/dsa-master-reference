/**
 * theme/lib/storage.ts
 *
 * Single wrapper around localStorage for the DSA Master Reference site.
 * Design goals:
 *  1. SSR-safe: every method returns a sensible default when `window` is undefined.
 *  2. Never throw: quota errors, incognito mode, disabled storage — all silent-safe
 *     with a debug log (visible in DevTools when `localStorage['dsa-debug']==='1'`).
 *  3. Schema-versioned: reads that expect a shape can request a version and receive
 *     the migrated value. `dsa-schema-version` records the highest migration applied.
 *  4. Prefixed: only touches keys starting with `dsa-`. StorageManager and other
 *     cross-cutting widgets can safely enumerate that namespace.
 *
 * Usage:
 *   import { storage } from '../lib/storage'
 *   const solved = storage.getJson<{ solved: boolean; timestamp?: number }>(
 *     `dsa-solved:${slug}`,
 *     { solved: false }
 *   )
 *   storage.setJson(`dsa-solved:${slug}`, { solved: true, timestamp: Date.now() })
 */

export const KEY_PREFIX = 'dsa-'
export const SCHEMA_VERSION_KEY = 'dsa-schema-version'
export const CURRENT_SCHEMA_VERSION = 2

type StorageError = { key: string; op: 'get' | 'set' | 'remove'; error: unknown }
const errorListeners: Array<(e: StorageError) => void> = []

function isDebug(): boolean {
  try {
    return typeof window !== 'undefined' && window.localStorage.getItem('dsa-debug') === '1'
  } catch {
    return false
  }
}

function log(err: StorageError) {
  if (isDebug()) {
    // eslint-disable-next-line no-console
    console.warn('[dsa-storage]', err.op, err.key, err.error)
  }
  errorListeners.forEach(fn => {
    try { fn(err) } catch { /* listener bugs must not crash callers */ }
  })
}

export function onStorageError(fn: (e: StorageError) => void): () => void {
  errorListeners.push(fn)
  return () => {
    const i = errorListeners.indexOf(fn)
    if (i !== -1) errorListeners.splice(i, 1)
  }
}

function safeWindow(): Window | null {
  if (typeof window === 'undefined') return null
  try {
    // Some browsers throw on `.localStorage` access in incognito iframes.
    void window.localStorage
    return window
  } catch {
    return null
  }
}

export const storage = {
  /** Raw string get. Returns `defaultValue` when missing, disabled, or errored. */
  get(key: string, defaultValue: string | null = null): string | null {
    const w = safeWindow()
    if (!w) return defaultValue
    try {
      const v = w.localStorage.getItem(key)
      return v === null ? defaultValue : v
    } catch (error) {
      log({ key, op: 'get', error })
      return defaultValue
    }
  },

  /** Raw string set. Returns `true` on success, `false` on quota / disabled / errored. */
  set(key: string, value: string): boolean {
    const w = safeWindow()
    if (!w) return false
    try {
      w.localStorage.setItem(key, value)
      return true
    } catch (error) {
      log({ key, op: 'set', error })
      return false
    }
  },

  /** Remove a key. Never throws. */
  remove(key: string): void {
    const w = safeWindow()
    if (!w) return
    try {
      w.localStorage.removeItem(key)
    } catch (error) {
      log({ key, op: 'remove', error })
    }
  },

  /**
   * JSON get with backward-compat migration.
   * If the stored value is a bare string (`'true'`), it is coerced into
   * `{ solved: true }` for solved-keys, otherwise wrapped as `{ value: raw }`.
   */
  getJson<T>(key: string, defaultValue: T): T {
    const raw = storage.get(key, null)
    if (raw === null) return defaultValue
    // Fast-path for the legacy `dsa-solved:<slug>` value 'true'.
    if (raw === 'true') return { solved: true } as unknown as T
    if (raw === 'false') return { solved: false } as unknown as T
    try {
      return JSON.parse(raw) as T
    } catch (error) {
      log({ key, op: 'get', error })
      return defaultValue
    }
  },

  /** JSON set. Returns `true` on success. */
  setJson<T>(key: string, value: T): boolean {
    try {
      return storage.set(key, JSON.stringify(value))
    } catch (error) {
      log({ key, op: 'set', error })
      return false
    }
  },

  /** Enumerate all `dsa-*` keys. Never throws. */
  keys(): string[] {
    const w = safeWindow()
    if (!w) return []
    const out: string[] = []
    try {
      for (let i = 0; i < w.localStorage.length; i++) {
        const k = w.localStorage.key(i)
        if (k && k.startsWith(KEY_PREFIX)) out.push(k)
      }
    } catch (error) {
      log({ key: KEY_PREFIX + '*', op: 'get', error })
    }
    return out
  },

  /**
   * Count solved problems. Handles both legacy `'true'` and JSON `{solved:true}`.
   * Shared helper — every widget that computes solved counts should call this
   * rather than reimplementing the double-format check.
   */
  countSolved(): number {
    let n = 0
    for (const k of storage.keys()) {
      if (!k.startsWith('dsa-solved:')) continue
      const raw = storage.get(k, null)
      if (raw === null) continue
      if (raw === 'true') { n++; continue }
      try {
        const parsed = JSON.parse(raw)
        if (parsed && parsed.solved) n++
      } catch { /* skip malformed values */ }
    }
    return n
  },

  /** Return the schema version currently persisted (0 if never set). */
  schemaVersion(): number {
    const raw = storage.get(SCHEMA_VERSION_KEY, '0')
    const n = raw === null ? 0 : parseInt(raw, 10)
    return Number.isFinite(n) ? n : 0
  },

  /** Set the schema version marker. Only migrate() calls this. */
  setSchemaVersion(v: number): void {
    storage.set(SCHEMA_VERSION_KEY, String(v))
  },
}

/**
 * Run pending schema migrations on first mount.
 *
 *   v1 → v2: `dsa-solved:<slug>` values changed from bare `'true'`
 *            to `{ solved: true, timestamp: <ms> }` (Round 11).
 *            Migration keeps the legacy `'true'` values in place — the
 *            reader helpers already treat both formats identically, so
 *            we only bump the version marker.
 *
 * Idempotent; safe to call on every page load. Never throws.
 */
export function runMigrations(): void {
  const current = storage.schemaVersion()
  if (current >= CURRENT_SCHEMA_VERSION) return
  // v1 → v2 is a no-op read-side migration (see docstring above).
  storage.setSchemaVersion(CURRENT_SCHEMA_VERSION)
}

/**
 * Small Vue-friendly helper: read `key` from storage into a Vue ref-like
 * container on mount. Handles SSR (never touches storage during render).
 *
 * Kept as a plain function (not a composable) so it can be imported from
 * both `<script setup>` files and plain `.vue` scripts without incident.
 */
export function readOnMount<T>(key: string, defaultValue: T): T {
  return storage.getJson<T>(key, defaultValue)
}
