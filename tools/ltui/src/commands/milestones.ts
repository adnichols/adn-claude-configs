import type { Command } from 'commander';
import { resolveConfig } from '../config.js';
import { createLinearClient } from '../client.js';
import {
  ColumnDefinition,
  emitDetailBlock,
  emitError,
  emitPaginationMeta,
  renderList,
  sanitizeSingleLine,
} from '../format.js';
import { getGlobalOptions } from '../options.js';
import { findProjectByKeyOrId, parseLinearError } from '../linear.js';

interface MilestoneRow {
  id: string;
  name: string;
  status: string;
  targetDate: string;
}

export function runMilestonesCommands(program: Command): void {
  const milestones = program.command('milestones').description('Project milestone commands');

  milestones
    .command('list')
    .description('List project milestones')
    .option('--project <id-or-key>', 'Filter by project')
    .action(async options => {
      try {
        const globalOpts = getGlobalOptions(program);
        const resolved = resolveConfig(program.opts<{ profile?: string }>().profile);
        const client = createLinearClient(resolved);

        const filter: Record<string, unknown> = {};
        if (options.project) {
          const project = await findProjectByKeyOrId(client, options.project);
          if (!project) {
            const out = emitError('not_found', `Project '${options.project}' not found`);
            process.stderr.write(out + '\n');
            process.exitCode = 1;
            return;
          }
          filter.project = { id: { eq: project.id } };
        }

        const data = await client.projectMilestones({
          first: globalOpts.limit,
          after: globalOpts.cursor,
          filter,
        });

        const rows: MilestoneRow[] = data.nodes.map((milestone: any) => ({
          id: milestone.id ?? '',
          name: sanitizeSingleLine(milestone.name ?? ''),
          status: milestone.archivedAt ? 'archived' : 'active',
          targetDate: milestone.targetDate ?? '',
        }));

        const columns: ColumnDefinition<MilestoneRow>[] = [
          { key: 'id', header: 'id', value: row => row.id },
          { key: 'name', header: 'name', value: row => row.name },
          { key: 'status', header: 'status', value: row => row.status },
          { key: 'targetDate', header: 'targetDate', value: row => row.targetDate },
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

  milestones
    .command('view')
    .description('View a milestone')
    .argument('<id>', 'Milestone id')
    .action(async (id: string) => {
      try {
        const resolved = resolveConfig(program.opts<{ profile?: string }>().profile);
        const client = createLinearClient(resolved);
        const milestone = await client.projectMilestone(id);
        if (!milestone) {
          const out = emitError('not_found', `Milestone '${id}' not found`);
          process.stderr.write(out + '\n');
          process.exitCode = 1;
          return;
        }

        const project = milestone.project ? await milestone.project : undefined;
        const fields: Record<string, string> = {
          MILESTONE: `${milestone.name ?? ''} (${milestone.id})`,
          PROJECT: project?.name ?? '',
          STATUS: milestone.archivedAt ? 'archived' : 'active',
          TARGET_DATE: milestone.targetDate ?? '',
        };
        const output = emitDetailBlock('MILESTONE_DETAIL', fields);
        process.stdout.write(output + '\n');
      } catch (error) {
        const parsed = parseLinearError(error);
        const out = emitError(parsed.code, parsed.message);
        process.stderr.write(out + '\n');
        process.exitCode = 1;
      }
    });
}
