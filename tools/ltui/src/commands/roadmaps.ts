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
import { parseLinearError } from '../linear.js';

interface RoadmapRow {
  id: string;
  name: string;
  owner: string;
  url: string;
}

export function runRoadmapsCommands(program: Command): void {
  const roadmaps = program.command('roadmaps').description('Roadmap commands');

  roadmaps
    .command('list')
    .description('List roadmaps')
    .action(async () => {
      try {
        const globalOpts = getGlobalOptions(program);
        const resolved = resolveConfig(program.opts<{ profile?: string }>().profile);
        const client = createLinearClient(resolved);

        const data = await client.roadmaps({ first: globalOpts.limit, after: globalOpts.cursor });
        const rows: RoadmapRow[] = await Promise.all(
          data.nodes.map(async (roadmap: any) => {
            let ownerName = '-';
            if (roadmap.owner) {
              try {
                const owner = await roadmap.owner;
                ownerName = owner?.name ?? '-';
              } catch {
                ownerName = '-';
              }
            }
            return {
              id: roadmap.id ?? '',
              name: sanitizeSingleLine(roadmap.name ?? ''),
              owner: ownerName,
              url: roadmap.url ?? '',
            };
          })
        );

        const columns: ColumnDefinition<RoadmapRow>[] = [
          { key: 'id', header: 'id', value: row => row.id },
          { key: 'name', header: 'name', value: row => row.name },
          { key: 'owner', header: 'owner', value: row => row.owner },
          { key: 'url', header: 'url', value: row => row.url },
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

  roadmaps
    .command('view')
    .description('View roadmap detail')
    .argument('<id>', 'Roadmap id')
    .action(async (id: string) => {
      try {
        const resolved = resolveConfig(program.opts<{ profile?: string }>().profile);
        const client = createLinearClient(resolved);
        const roadmap = await client.roadmap(id);
        if (!roadmap) {
          const out = emitError('not_found', `Roadmap '${id}' not found`);
          process.stderr.write(out + '\n');
          process.exitCode = 1;
          return;
        }

        const owner = roadmap.owner ? await roadmap.owner : undefined;
        const fields: Record<string, string> = {
          ROADMAP: `${roadmap.name ?? ''} (${roadmap.id})`,
          OWNER: owner?.name ?? '',
          UPDATED_AT: roadmap.updatedAt?.toISOString?.() ?? '',
          URL: roadmap.url ?? '',
        };
        let output = emitDetailBlock('ROADMAP_DETAIL', fields);

        const projectsConnection = await roadmap.projects({ first: 20 });
        const lines: string[] = ['PROJECTS_START'];
        for (const project of projectsConnection.nodes) {
          lines.push(
            `${project.id}\t${sanitizeSingleLine(project.name ?? '')}\t${project.state ?? ''}`
          );
        }
        lines.push('PROJECTS_END');
        output += `\n${lines.join('\n')}\n`;
        process.stdout.write(output);
      } catch (error) {
        const parsed = parseLinearError(error);
        const out = emitError(parsed.code, parsed.message);
        process.stderr.write(out + '\n');
        process.exitCode = 1;
      }
    });
}
