import fs from 'node:fs';
import path from 'node:path';
import { pathToFileURL } from 'node:url';
import type { Command } from 'commander';
import { getConfigDirectory, resolveConfig } from './config.js';
import { createLinearClient } from './client.js';
import { emitDetailBlock, emitError, renderList } from './format.js';

interface ExtensionConfigEntry {
  name: string;
  path: string;
  enabled?: boolean;
}

export interface ExtensionHelpers {
  resolveConfig: typeof resolveConfig;
  createLinearClient: typeof createLinearClient;
  emitDetailBlock: typeof emitDetailBlock;
  emitError: typeof emitError;
  renderList: typeof renderList;
}

const helpers: ExtensionHelpers = {
  resolveConfig,
  createLinearClient,
  emitDetailBlock,
  emitError,
  renderList,
};

let loaded = false;

export async function loadExtensions(program: Command): Promise<void> {
  if (loaded) return;
  const file = path.join(getConfigDirectory(), 'extensions.json');
  let entries: ExtensionConfigEntry[] = [];
  try {
    const raw = fs.readFileSync(file, 'utf8');
    entries = JSON.parse(raw) as ExtensionConfigEntry[];
  } catch {
    loaded = true;
    return;
  }

  for (const entry of entries) {
    if (entry.enabled === false) continue;
    try {
      const absolutePath = path.isAbsolute(entry.path)
        ? entry.path
        : path.join(getConfigDirectory(), entry.path);
      const moduleUrl = pathToFileURL(absolutePath).href;
      const mod = await import(moduleUrl);
      const register = mod.register ?? mod.default?.register;
      if (typeof register === 'function') {
        await register(program, helpers);
      }
    } catch (error) {
      const err = error as Error;
      const out = emitError('extension_error', `Failed to load extension '${entry.name}': ${err.message}`);
      process.stderr.write(out + '\n');
      process.exitCode = 1;
    }
  }

  loaded = true;
}
