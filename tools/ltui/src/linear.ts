import fs from 'node:fs';
import path from 'node:path';
import { getCachedValue, setCachedValue } from './cache.js';

const CACHE_TTL_SECONDS = 300;
const UUID_REGEX = /^[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}$/i;

export function isUuid(value: string): boolean {
  return UUID_REGEX.test(value);
}

export function readTextOrPath(value: string): string {
  if (value.startsWith('@')) {
    const filePath = value.slice(1);
    const resolvedPath = path.resolve(process.cwd(), filePath);
    try {
      return fs.readFileSync(resolvedPath, 'utf8');
    } catch {
      throw new Error(`validation_error Unable to read file '${filePath}'`);
    }
  }
  return value;
}

const TEAM_LOOKUP_QUERY = `
  query TeamLookup($filter: TeamFilter) {
    teams(first: 1, filter: $filter) {
      nodes {
        id
        key
        name
        description
      }
    }
  }
`;

export async function findTeamByKeyOrId(client: any, ref: string): Promise<any | null> {
  const normalized = ref.trim().toLowerCase();
  const cachedTeam = getCachedValue<any>('teams', normalized);
  if (cachedTeam) {
    return cachedTeam;
  }

  const orClauses: any[] = [{ key: { eq: ref.toUpperCase() } }, { name: { eq: ref } }];
  if (isUuid(ref)) {
    orClauses.unshift({ id: { eq: ref } });
  }
  const filter = { or: orClauses };

  let team: any | null = null;
  try {
    if (client?.client?.request) {
      const response = await client.client.request(TEAM_LOOKUP_QUERY, { filter });
      team = response?.teams?.nodes?.[0] ?? null;
    } else {
      const connection = await client.teams({ first: 1, filter });
      team = connection.nodes[0] ?? null;
    }
  } catch (error) {
    throw error;
  }

  if (team?.id) {
    setCachedValue('teams', normalized, team, CACHE_TTL_SECONDS);
  }
  return team;
}

export async function findProjectByKeyOrId(client: any, ref: string): Promise<any | null> {
  const normalized = ref.trim().toLowerCase();
  const cachedId = getCachedValue<string>('projects', normalized);
  if (cachedId) {
    try {
      const project = await client.project(cachedId);
      if (project) return project;
    } catch {
      // ignore stale cache
    }
  }

  const projectFilters: any[] = [{ slugId: { eq: ref } }, { name: { eq: ref } }];
  if (isUuid(ref)) {
    projectFilters.unshift({ id: { eq: ref } });
  }

  const connection = await client.projects({
    first: 1,
    filter: {
      or: projectFilters,
    },
  });
  const project = connection.nodes[0] ?? null;
  if (project?.id) {
    setCachedValue('projects', normalized, project.id, CACHE_TTL_SECONDS);
  }
  return project;
}

export async function findWorkflowStateByNameOrId(
  client: any,
  teamId: string,
  ref: string
): Promise<any | null> {
  const normalized = ref.trim().toLowerCase();
  const cacheKey = `${teamId}:${normalized}`;
  const cachedId = getCachedValue<string>('workflowStates', cacheKey);
  if (cachedId) {
    try {
      const state = await client.workflowState(cachedId);
      if (state) return state;
    } catch {
      // ignore stale cache entry
    }
  }

  const connection = await client.workflowStates({
    first: 1,
    filter: {
      and: [
        { team: { id: { eq: teamId } } },
        {
          or: [
            ...(isUuid(ref) ? [{ id: { eq: ref } }] : []),
            { name: { eq: ref } },
          ],
        },
      ],
    },
  });
  const state = connection.nodes[0] ?? null;
  if (state?.id) {
    setCachedValue('workflowStates', cacheKey, state.id, CACHE_TTL_SECONDS);
  }
  return state;
}

export async function resolveLabelIds(
  client: any,
  names: string[],
  teamId: string
): Promise<string[]> {
  if (names.length === 0) return [];
  const uniqueNames = Array.from(new Set(names));
  const byName = new Map<string, string>();
  const missing: string[] = [];
  for (const name of uniqueNames) {
    const cached = getCachedValue<string>('labels', `${teamId}:${name.toLowerCase()}`);
    if (cached) {
      byName.set(name, cached);
    } else {
      missing.push(name);
    }
  }

  if (missing.length > 0) {
    const connection = await client.issueLabels({
      first: missing.length,
      filter: {
        and: [{ team: { id: { eq: teamId } } }, { name: { in: missing } }],
      },
    });
    for (const label of connection.nodes) {
      if (label.name && label.id) {
        byName.set(label.name, label.id);
        setCachedValue('labels', `${teamId}:${label.name.toLowerCase()}`, label.id, CACHE_TTL_SECONDS);
      }
    }
  }

  const unresolved = uniqueNames.filter(name => !byName.has(name));
  if (unresolved.length > 0) {
    throw new Error(`not_found Labels not found: ${unresolved.join(', ')}`);
  }
  return names.map(name => byName.get(name)!);
}

export async function resolveAssigneeId(client: any, ref: string): Promise<string | undefined> {
  if (ref === 'me') {
    const viewer = await client.viewer;
    return viewer?.id;
  }

  const normalized = ref.trim().toLowerCase();

  if (ref.includes('@')) {
    const cached = getCachedValue<string>('users', `email:${normalized}`);
    if (cached) return cached;
    const connection = await client.users({
      first: 1,
      filter: { email: { eq: ref } },
    });
    const user = connection.nodes[0];
    if (user) {
      if (user.email) {
        setCachedValue('users', `email:${user.email.toLowerCase()}`, user.id, CACHE_TTL_SECONDS);
      }
      if (user.name) {
        setCachedValue('users', `name:${user.name.toLowerCase()}`, user.id, CACHE_TTL_SECONDS);
      }
      return user.id;
    }
  }

  const cachedByName = getCachedValue<string>('users', `name:${normalized}`);
  if (cachedByName) return cachedByName;

  const assigneeFilters: any[] = [{ name: { eq: ref } }];
  if (isUuid(ref)) {
    assigneeFilters.unshift({ id: { eq: ref } });
  }

  const byId = await client.users({
    first: 1,
    filter: {
      or: assigneeFilters,
    },
  });
  const user = byId.nodes[0];
  if (user) {
    if (user.email) {
      setCachedValue('users', `email:${user.email.toLowerCase()}`, user.id, CACHE_TTL_SECONDS);
    }
    if (user.name) {
      setCachedValue('users', `name:${user.name.toLowerCase()}`, user.id, CACHE_TTL_SECONDS);
    }
    return user.id;
  }
  return undefined;
}

export async function resolveIssueByIdOrKey(client: any, ref: string): Promise<any | null> {
  try {
    const issue = await client.issue(ref);
    if (issue) return issue;
  } catch {
    // continue to key lookup
  }

  const match = /^([a-zA-Z0-9]+)-(\d+)$/.exec(ref);
  if (!match) return null;
  const [, teamKeyRaw, numberRaw] = match;
  const teamKey = teamKeyRaw.toUpperCase();
  const number = parseInt(numberRaw, 10);
  if (Number.isNaN(number)) return null;

  const connection = await client.issues({
    first: 1,
    filter: {
      and: [{ team: { key: { eq: teamKey } } }, { number: { eq: number } }],
    },
  });
  return connection.nodes[0] ?? null;
}

export function parseLinearError(error: unknown): { code: string; message: string } {
  const err = error as Error;
  const message = err?.message ?? 'Unknown error';
  const linearType = (error as { type?: string })?.type;
  if (linearType && String(linearType).toLowerCase().includes('rate')) {
    return { code: 'api_error', message: 'rate_limited' };
  }
  if (/rate.?limit/i.test(message)) {
    return { code: 'api_error', message: 'rate_limited' };
  }
  const parts = message.split(' ');
  if (parts.length > 1 && /^[a-z_]+$/i.test(parts[0])) {
    const code = parts.shift() as string;
    return { code, message: parts.join(' ') };
  }
  return { code: 'api_error', message };
}
