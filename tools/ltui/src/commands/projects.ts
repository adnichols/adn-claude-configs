import type { Command } from 'commander';
import { resolveConfig, loadProjectConfig, saveProjectConfig } from '../config.js';
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
import { findProjectByKeyOrId, findTeamByKeyOrId, parseLinearError } from '../linear.js';

interface ProjectRow {
  id: string;
  name: string;
  state: string;
  status: string;
  targetDate: string;
}

export function runProjectsCommands(program: Command): void {
  const projects = program.command('projects').description('Project commands');

  projects
    .command('list')
    .description('List projects')
    .option('--team <key-or-id>', 'Filter by team')
    .option('--state <state>', 'Filter by state')
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
          filter.accessibleTeams = {
            some: {
              id: { eq: team.id },
            },
          };
        }
        if (options.state) {
          filter.state = { eq: options.state };
        }

        const data = await client.projects({
          first: globalOpts.limit,
          after: globalOpts.cursor,
          filter,
        });

        // Await status as it's a promise in the Linear SDK
        const rows: ProjectRow[] = await Promise.all(
          data.nodes.map(async (project: any) => {
            const status = project.status ? await project.status : undefined;
            return {
              id: project.id ?? '',
              name: sanitizeSingleLine(project.name ?? ''),
              state: project.state ?? '',
              status: status?.name ?? '',
              targetDate: project.targetDate ?? '',
            };
          })
        );

        const columns: ColumnDefinition<ProjectRow>[] = [
          { key: 'id', header: 'id', value: row => row.id },
          { key: 'name', header: 'name', value: row => row.name },
          { key: 'state', header: 'state', value: row => row.state },
          { key: 'status', header: 'status', value: row => row.status },
          { key: 'targetDate', header: 'target_date', value: row => row.targetDate },
        ];

        const meta = emitPaginationMeta(
          data.pageInfo?.endCursor ?? null,
          data.pageInfo?.startCursor ?? null,
          rows.length
        );
        const body = renderList(rows, columns, { format: globalOpts.format, fields: globalOpts.fields });
        process.stdout.write(`${meta}\n${body}\n`);
      } catch (error) {
        writeProjectsError(error);
      }
    });

  projects
    .command('view')
    .description('View project details')
    .argument('<id-or-key>', 'Project id or slug')
    .action(async (ref: string) => {
      try {
        const resolved = resolveConfig(program.opts<{ profile?: string }>().profile);
        const client = createLinearClient(resolved);
        const project = await findProjectByKeyOrId(client, ref);
        if (!project) {
          const out = emitError('not_found', `Project '${ref}' not found`);
          process.stderr.write(out + '\n');
          process.exitCode = 1;
          return;
        }

        // Await status as it's a promise in the Linear SDK
        const status = project.status ? await project.status : undefined;

        const fields: Record<string, string> = {
          PROJECT: `${project.name ?? ''} (${project.id ?? ''})`,
          STATUS: status?.name ?? '',
          STATE: project.state ?? '',
          TARGET_DATE: project.targetDate ?? '',
          URL: project.url ?? '',
          HEALTH: project.health ?? '',
        };

        let output = emitDetailBlock('PROJECT_DETAIL', fields);

        const totalIssues = lastValue(project.issueCountHistory);
        const completedIssues = lastValue(project.completedIssueCountHistory);
        const openIssues = Math.max(0, totalIssues - completedIssues);
        const summaryLines = [
          'ISSUES_SUMMARY_START',
          `TOTAL: ${totalIssues}`,
          `COMPLETED: ${completedIssues}`,
          `OPEN: ${openIssues}`,
          `PROGRESS: ${(project.progress ?? 0).toFixed(2)}`,
          'ISSUES_SUMMARY_END',
        ];
        output += `\n${summaryLines.join('\n')}\n`;

        const milestonesConnection =
          typeof project.projectMilestones === 'function'
            ? await project.projectMilestones({ first: 20 })
            : { nodes: [] };
        const milestoneLines = ['MILESTONES_START'];
        for (const milestone of milestonesConnection.nodes) {
          milestoneLines.push(
            `${milestone.id}\t${sanitizeSingleLine(milestone.name ?? '')}\t${milestone.targetDate ?? ''}`
          );
        }
        milestoneLines.push('MILESTONES_END');
        output += `${milestoneLines.join('\n')}\n`;

        process.stdout.write(output);
      } catch (error) {
        writeProjectsError(error);
      }
    });

  projects
    .command('align')
    .description('Align current directory with a Linear project')
    .argument('<id-or-key>', 'Project id or slug')
    .option('--profile <name>', 'Profile to use when running in this directory')
    .option('--team <key-or-id>', 'Team key to set in config')
    .option('--state <name>', 'Default issue state')
    .option('--label <name>', 'Default labels', collect, [])
    .option('--assignee <me|email|id>', 'Default assignee reference')
    .action(async (ref: string, options) => {
      try {
        const resolved = resolveConfig(program.opts<{ profile?: string }>().profile);
        const client = createLinearClient(resolved);
        const project = await findProjectByKeyOrId(client, ref);
        if (!project) {
          const out = emitError('not_found', `Project '${ref}' not found`);
          process.stderr.write(out + '\n');
          process.exitCode = 1;
          return;
        }

        let teamKey = options.team;
        if (!teamKey) {
          const teamsConnection =
            typeof project.teams === 'function' ? await project.teams({ first: 1 }) : { nodes: [] };
          const team = teamsConnection.nodes?.[0];
          if (!team) {
            const out = emitError('not_found', 'Project has no associated teams to align with');
            process.stderr.write(out + '\n');
            process.exitCode = 1;
            return;
          }
          teamKey = team.key;
        } else {
          const team = await findTeamByKeyOrId(client, options.team);
          if (!team) {
            const out = emitError('not_found', `Team '${options.team}' not found`);
            process.stderr.write(out + '\n');
            process.exitCode = 1;
            return;
          }
          teamKey = team.key;
        }

        const existing = loadProjectConfig(process.cwd());
        const newConfig = {
          profile: options.profile ?? existing.profile ?? resolved.profileName,
          teamKey,
          projectId: project.id,
          defaultIssueState: options.state ?? existing.defaultIssueState,
          defaultLabels: options.label?.length ? options.label : existing.defaultLabels ?? [],
          defaultAssignee: options.assignee ?? existing.defaultAssignee,
        };

        saveProjectConfig(newConfig, process.cwd());

        const block = emitDetailBlock('PROJECT_ALIGNED', {
          PROFILE: newConfig.profile ?? '',
          TEAM: newConfig.teamKey ?? '',
          PROJECT_ID: newConfig.projectId ?? '',
          DEFAULT_STATE: newConfig.defaultIssueState ?? '',
          DEFAULT_LABELS: (newConfig.defaultLabels ?? []).join(','),
          DEFAULT_ASSIGNEE: newConfig.defaultAssignee ?? '',
        });
        process.stdout.write(block + '\n');
      } catch (error) {
        writeProjectsError(error);
      }
    });
}

function lastValue(values: Array<number>): number {
  if (!Array.isArray(values) || values.length === 0) return 0;
  return values[values.length - 1] ?? 0;
}

function collect(value: string, previous: string[]): string[] {
  return [...previous, value];
}

function writeProjectsError(error: unknown): void {
  const parsed = parseLinearError(error);
  const out = emitError(parsed.code, parsed.message);
  process.stderr.write(out + '\n');
  process.exitCode = 1;
}
