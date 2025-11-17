import fs from 'node:fs';
import path from 'node:path';
import { getConfigDirectory } from './config.js';

export interface SavedQueryDefinition {
  name: string;
  search?: string;
  team?: string;
  project?: string;
  state?: string;
  labels?: string[];
  assignee?: string;
  updatedSince?: string;
  createdSince?: string;
}

interface SavedQueryFile {
  queries: Record<string, SavedQueryDefinition>;
}

function queriesFilePath(): string {
  return path.join(getConfigDirectory(), 'queries.json');
}

function loadQueriesFile(): SavedQueryFile {
  try {
    const raw = fs.readFileSync(queriesFilePath(), 'utf8');
    const parsed = JSON.parse(raw) as SavedQueryFile;
    return {
      queries: parsed.queries ?? {},
    };
  } catch {
    return { queries: {} };
  }
}

function saveQueriesFile(data: SavedQueryFile): void {
  const file = queriesFilePath();
  fs.mkdirSync(path.dirname(file), { recursive: true });
  fs.writeFileSync(file, JSON.stringify(data, null, 2), { mode: 0o600 });
}

export function listSavedQueries(): SavedQueryDefinition[] {
  const file = loadQueriesFile();
  return Object.values(file.queries).sort((a, b) => a.name.localeCompare(b.name));
}

export function getSavedQuery(name: string): SavedQueryDefinition | undefined {
  const file = loadQueriesFile();
  const entry = file.queries[name];
  if (!entry) return undefined;
  return { ...entry };
}

export function saveQuery(definition: SavedQueryDefinition): void {
  const file = loadQueriesFile();
  file.queries[definition.name] = { ...definition };
  saveQueriesFile(file);
}

export function removeQuery(name: string): void {
  const file = loadQueriesFile();
  if (file.queries[name]) {
    delete file.queries[name];
    saveQueriesFile(file);
  }
}
