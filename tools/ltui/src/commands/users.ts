import type { Command } from 'commander';
import { resolveConfig } from '../config.js';
import { createLinearClient } from '../client.js';
import {
  ColumnDefinition,
  emitError,
  emitPaginationMeta,
  renderList,
} from '../format.js';
import { getGlobalOptions } from '../options.js';
import { parseLinearError } from '../linear.js';

interface UserRow {
  id: string;
  name: string;
  email: string;
  displayName: string;
}

export function runUsersCommands(program: Command): void {
  program
    .command('users')
    .description('User commands')
    .option('--active-only', 'Only include active users')
    .action(async options => {
      try {
        const globalOpts = getGlobalOptions(program);
        const resolved = resolveConfig(program.opts<{ profile?: string }>().profile);
        const client = createLinearClient(resolved);

        const filter: Record<string, unknown> = {};
        if (options.activeOnly) {
          filter.active = { eq: true };
        }

        const data = await client.users({
          first: globalOpts.limit,
          after: globalOpts.cursor,
          filter,
        });
        const rows: UserRow[] = data.nodes.map((user: any) => ({
          id: user.id ?? '',
          name: user.name ?? '',
          email: user.email ?? '',
          displayName: user.displayName ?? '',
        }));

        const columns: ColumnDefinition<UserRow>[] = [
          { key: 'id', header: 'id', value: row => row.id },
          { key: 'name', header: 'name', value: row => row.name },
          { key: 'email', header: 'email', value: row => row.email },
          { key: 'displayName', header: 'displayName', value: row => row.displayName },
        ];

        const meta = emitPaginationMeta(
          data.pageInfo?.endCursor ?? null,
          data.pageInfo?.startCursor ?? null,
          rows.length
        );
        const body = renderList(rows, columns, { format: globalOpts.format, fields: globalOpts.fields });
        process.stdout.write(`${meta}\n${body}\n`);
      } catch (error) {
        const parsed = parseLinearError(error);
        const out = emitError(parsed.code, parsed.message);
        process.stderr.write(out + '\n');
        process.exitCode = 1;
      }
    });
}
