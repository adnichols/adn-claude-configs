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
import { findTeamByKeyOrId, parseLinearError } from '../linear.js';

interface CycleRow {
  id: string;
  number: string;
  name: string;
  startsAt: string;
  endsAt: string;
  status: string;
}

export function runCyclesCommands(program: Command): void {
  program
    .command('cycles')
    .description('Cycle commands')
    .option('--team <key-or-id>', 'Filter by team')
    .action(async options => {
      try {
        const globalOpts = getGlobalOptions(program);
        const resolved = resolveConfig(program.opts<{ profile?: string }>().profile);
        const client = createLinearClient(resolved);

        const filter: Record<string, unknown> = {};
        if (options.team) {
          const team = await findTeamByKeyOrId(client, options.team);
          if (!team) {
            const out = emitError('not_found', `Team '${options.team}' not found`);
            process.stderr.write(out + '\n');
            process.exitCode = 1;
            return;
          }
          filter.team = { id: { eq: team.id } };
        }

        const data = await client.cycles({ first: globalOpts.limit, after: globalOpts.cursor, filter });
        const rows: CycleRow[] = data.nodes.map((cycle: any) => ({
          id: cycle.id ?? '',
          number: String(cycle.number ?? ''),
          name: cycle.name ?? '',
          startsAt: cycle.startsAt ?? '',
          endsAt: cycle.endsAt ?? '',
          status: cycle.status ?? '',
        }));

        const columns: ColumnDefinition<CycleRow>[] = [
          { key: 'id', header: 'id', value: row => row.id },
          { key: 'number', header: 'number', value: row => row.number },
          { key: 'name', header: 'name', value: row => row.name },
          { key: 'startsAt', header: 'startsAt', value: row => row.startsAt },
          { key: 'endsAt', header: 'endsAt', value: row => row.endsAt },
          { key: 'status', header: 'status', value: row => row.status },
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
