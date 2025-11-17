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

interface LabelRow {
  id: string;
  name: string;
  group: string;
  color: string;
}

export function runLabelsCommands(program: Command): void {
  program
    .command('labels')
    .description('Label commands')
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

        const data = await client.issueLabels({
          first: globalOpts.limit,
          after: globalOpts.cursor,
          filter,
        });
        const rows: LabelRow[] = data.nodes.map((label: any) => ({
          id: label.id ?? '',
          name: label.name ?? '',
          group: label.parent?.name ?? (label.isGroup ? 'group' : ''),
          color: label.color ?? '',
        }));

        const columns: ColumnDefinition<LabelRow>[] = [
          { key: 'id', header: 'id', value: row => row.id },
          { key: 'name', header: 'name', value: row => row.name },
          { key: 'group', header: 'group', value: row => row.group },
          { key: 'color', header: 'color', value: row => row.color },
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
