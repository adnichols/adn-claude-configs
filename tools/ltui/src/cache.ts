import fs from 'node:fs';
import path from 'node:path';
import { getConfigDirectory } from './config.js';

interface CacheEntry {
  value: unknown;
  expiresAt: number;
}

interface CacheData {
  [bucket: string]: Record<string, CacheEntry>;
}

const CACHE_FILE = path.join(getConfigDirectory(), 'cache.json');
let memoryCache: CacheData | null = null;
let loaded = false;

function ensureCacheLoaded(): CacheData {
  if (memoryCache && loaded) return memoryCache;
  try {
    const raw = fs.readFileSync(CACHE_FILE, 'utf8');
    memoryCache = JSON.parse(raw) as CacheData;
  } catch {
    memoryCache = {};
  }
  loaded = true;
  return memoryCache;
}

function persist(cache: CacheData): void {
  const dir = path.dirname(CACHE_FILE);
  fs.mkdirSync(dir, { recursive: true });
  fs.writeFileSync(CACHE_FILE, JSON.stringify(cache, null, 2), { mode: 0o600 });
}

function purgeExpired(cache: CacheData): void {
  const now = Date.now();
  for (const [bucket, entries] of Object.entries(cache)) {
    for (const key of Object.keys(entries)) {
      if (entries[key].expiresAt <= now) {
        delete entries[key];
      }
    }
    if (Object.keys(entries).length === 0) {
      delete cache[bucket];
    }
  }
}

export function getCachedValue<T>(bucket: string, key: string): T | undefined {
  const cache = ensureCacheLoaded();
  purgeExpired(cache);
  const entry = cache[bucket]?.[key];
  return entry ? (entry.value as T) : undefined;
}

export function setCachedValue(bucket: string, key: string, value: unknown, ttlSeconds: number): void {
  if (ttlSeconds <= 0) return;
  const cache = ensureCacheLoaded();
  if (!cache[bucket]) cache[bucket] = {};
  cache[bucket][key] = {
    value,
    expiresAt: Date.now() + ttlSeconds * 1000,
  };
  purgeExpired(cache);
  persist(cache);
}

export function clearCacheBucket(bucket: string): void {
  const cache = ensureCacheLoaded();
  if (cache[bucket]) {
    delete cache[bucket];
    persist(cache);
  }
}
