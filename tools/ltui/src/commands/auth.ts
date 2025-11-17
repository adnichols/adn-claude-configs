import type { Command } from 'commander';
import {
  loadGlobalConfig,
  saveGlobalConfig,
  loadProfilesFile,
  saveProfilesFile,
  resolveConfig,
} from '../config.js';
import { emitDetailBlock, emitError } from '../format.js';

export function runAuthCommands(program: Command): void {
  const auth = program.command('auth').description('Authentication and profile management');

  auth
    .command('list')
    .description('List configured profiles')
    .action(() => {
      const config = loadGlobalConfig();
      const profiles = loadProfilesFile();
      const lines: string[] = [];
      lines.push('id\tworkspace\thasKey');
      const entries = config.profiles ?? {};
      for (const [name, profile] of Object.entries(entries)) {
        const hasKey = profiles[name]?.apiKey ? 'true' : 'false';
        lines.push(`${name}\t${profile.workspace}\t${hasKey}`);
      }
      process.stdout.write(lines.join('\n') + '\n');
    });

  auth
    .command('add')
    .description('Add or update a profile')
    .requiredOption('--profile <name>', 'Profile name')
    .option('--workspace <slug>', 'Workspace slug')
    .option('--api-key <key>', 'API key (optional, or use LINEAR_API_KEY)')
    .action(options => {
      const { profile, workspace, apiKey } = options as {
        profile: string;
        workspace?: string;
        apiKey?: string;
      };
      const config = loadGlobalConfig();
      if (!config.profiles) config.profiles = {};
      const existing = config.profiles[profile] ?? { workspace: workspace ?? '', keyRef: profile };
      const updated = {
        workspace: workspace ?? existing.workspace,
        keyRef: existing.keyRef,
      };
      config.profiles[profile] = updated;
      if (!config.defaultProfile) {
        config.defaultProfile = profile;
      }
      saveGlobalConfig(config);

      const profiles = loadProfilesFile();
      const key = apiKey || process.env.LINEAR_API_KEY;
      if (key) {
        profiles[profile] = { apiKey: key };
        saveProfilesFile(profiles);
      }

      const block = emitDetailBlock('PROFILE_SAVED', {
        PROFILE: profile,
        WORKSPACE: updated.workspace,
        KEY_STORED: key ? 'true' : 'false',
      });
      process.stdout.write(block + '\n');
    });

  auth
    .command('remove')
    .description('Remove a profile')
    .requiredOption('--profile <name>', 'Profile name')
    .action(options => {
      const { profile } = options as { profile: string };
      const config = loadGlobalConfig();
      if (config.profiles && config.profiles[profile]) {
        delete config.profiles[profile];
        saveGlobalConfig(config);
      }
      const profiles = loadProfilesFile();
      if (profiles[profile]) {
        delete profiles[profile];
        saveProfilesFile(profiles);
      }
      const block = emitDetailBlock('PROFILE_REMOVED', {
        PROFILE: profile,
      });
      process.stdout.write(block + '\n');
    });

  auth
    .command('test')
    .description('Test auth for a profile')
    .option('--profile <name>', 'Profile name')
    .action(options => {
      try {
        const resolved = resolveConfig(options.profile as string | undefined);
        const block = emitDetailBlock('AUTH_OK', {
          PROFILE: resolved.profileName || '',
        });
        process.stdout.write(block + '\n');
      } catch (error) {
        const err = error as Error;
        const message = err.message || 'Unknown error';
        const out = emitError('auth_error', message);
        process.stderr.write(out + '\n');
        process.exitCode = 1;
      }
    });
}

