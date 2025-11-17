import test from 'node:test';
import assert from 'node:assert/strict';
import { mkdtempSync, rmSync } from 'node:fs';
import os from 'node:os';
import path from 'node:path';
import { spawnSync } from 'node:child_process';

type HelpCase = {
  title: string;
  args: string[];
  expectOptions: string[];
};

function withTempConfig<T>(fn: (configDir: string) => T): T {
  const dir = mkdtempSync(path.join(os.tmpdir(), 'ltui-config-'));
  try {
    return fn(dir);
  } finally {
    rmSync(dir, { recursive: true, force: true });
  }
}

function runLtui(args: string[], env?: Record<string, string | undefined>) {
  return spawnSync('node', ['bin/ltui', ...args], {
    cwd: process.cwd(),
    encoding: 'utf8',
    env: {
      ...process.env,
      ...env,
    },
  });
}

const globalHelpCase: HelpCase = {
  title: 'global options',
  args: ['--help'],
  expectOptions: ['--profile <name>', '--format <fmt>', '--fields <fields>', '--limit <n>', '--cursor <cursor>', '--agent', '--no-agent'],
};

const helpCases: HelpCase[] = [
  globalHelpCase,
  { title: 'auth root', args: ['auth', '--help'], expectOptions: [] },
  { title: 'auth list', args: ['auth', 'list', '--help'], expectOptions: [] },
  { title: 'auth add', args: ['auth', 'add', '--help'], expectOptions: ['--profile <name>', '--workspace <slug>', '--api-key <key>'] },
  { title: 'auth remove', args: ['auth', 'remove', '--help'], expectOptions: ['--profile <name>'] },
  { title: 'auth test', args: ['auth', 'test', '--help'], expectOptions: ['--profile <name>'] },
  { title: 'issues list', args: ['issues', 'list', '--help'], expectOptions: ['--team <key-or-id>', '--project <key-or-id>', '--state <name-or-id>', '--assignee <me|email|id>', '--label <name-or-id>', '--search <query>', '--updated-since <iso>', '--created-since <iso>', '--saved <name>'] },
  { title: 'issues view', args: ['issues', 'view', '--help'], expectOptions: ['--include-comments', '--include-history', '--max-description-chars <n>', '--max-comment-chars <n>'] },
  { title: 'issues create', args: ['issues', 'create', '--help'], expectOptions: ['--team <key>', '--project <key-or-id>', '--title <title>', '--description <text-or-@path>', '--state <name-or-id>', '--label <name-or-id>', '--assignee <me|email|id>', '--priority <0-4>'] },
  { title: 'issues update', args: ['issues', 'update', '--help'], expectOptions: ['--team <key>', '--project <key-or-id>', '--title <title>', '--description <text-or-@path>', '--state <name-or-id>', '--label <name-or-id>', '--add-label <name-or-id>', '--remove-label <name-or-id>', '--assignee <me|email|id>', '--priority <0-4>', '--estimate <number>', '--due <iso>'] },
  { title: 'issues comment', args: ['issues', 'comment', '--help'], expectOptions: ['--body <text-or-@path>'] },
  { title: 'issues link', args: ['issues', 'link', '--help'], expectOptions: ['--url <url>', '--title <title>', '--branch <branch>', '--commit <sha>'] },
  { title: 'issues relate', args: ['issues', 'relate', '--help'], expectOptions: ['--parent <parent-id-or-key>'] },
  { title: 'issues block', args: ['issues', 'block', '--help'], expectOptions: ['--blocked-by <other-id-or-key>'] },
  { title: 'issues saved add', args: ['issues', 'saved', 'add', '--help'], expectOptions: ['--name <name>', '--search <query>', '--team <key-or-id>', '--project <key-or-id>', '--state <name-or-id>', '--assignee <me|email|id>', '--label <name-or-id>', '--updated-since <iso>', '--created-since <iso>'] },
  { title: 'issues saved remove', args: ['issues', 'saved', 'remove', '--help'], expectOptions: ['--name <name>'] },
  { title: 'teams list', args: ['teams', 'list', '--help'], expectOptions: [] },
  { title: 'teams view', args: ['teams', 'view', '--help'], expectOptions: [] },
  { title: 'projects list', args: ['projects', 'list', '--help'], expectOptions: ['--team <key-or-id>', '--state <state>'] },
  { title: 'projects view', args: ['projects', 'view', '--help'], expectOptions: [] },
  { title: 'projects align', args: ['projects', 'align', '--help'], expectOptions: ['--profile <name>', '--team <key-or-id>', '--state <name>', '--label <name>', '--assignee <me|email|id>'] },
  { title: 'cycles list', args: ['cycles', '--help'], expectOptions: ['--team <key-or-id>'] },
  { title: 'labels list', args: ['labels', '--help'], expectOptions: ['--team <key-or-id>'] },
  { title: 'users list', args: ['users', '--help'], expectOptions: ['--active-only'] },
  { title: 'documents list', args: ['documents', 'list', '--help'], expectOptions: ['--project <key-or-id>', '--search <term>'] },
  { title: 'documents view', args: ['documents', 'view', '--help'], expectOptions: ['--max-content-chars <n>'] },
  { title: 'roadmaps list', args: ['roadmaps', 'list', '--help'], expectOptions: [] },
  { title: 'roadmaps view', args: ['roadmaps', 'view', '--help'], expectOptions: [] },
  { title: 'milestones list', args: ['milestones', 'list', '--help'], expectOptions: ['--project <id-or-key>'] },
  { title: 'milestones view', args: ['milestones', 'view', '--help'], expectOptions: [] },
  { title: 'notifications list', args: ['notifications', '--help'], expectOptions: ['--unread-only'] },
];

for (const helpCase of helpCases) {
  test(`help output lists options for ${helpCase.title}`, () => {
    withTempConfig(dir => {
      const result = runLtui(helpCase.args, { LTUI_CONFIG_DIR: dir, LINEAR_API_KEY: 'lin_api_test' });
      assert.equal(result.status, 0, result.stderr || result.stdout);
      for (const option of helpCase.expectOptions) {
        const escaped = option.replace(/[.*+?^${}()|[\]\\]/g, '\\$&');
        assert.match(result.stdout, new RegExp(escaped));
      }
    });
  });
}
