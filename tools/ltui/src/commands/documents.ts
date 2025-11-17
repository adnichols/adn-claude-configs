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
  truncateMultiline,
} from '../format.js';
import { getGlobalOptions } from '../options.js';
import { findProjectByKeyOrId, parseLinearError } from '../linear.js';

interface DocumentRow {
  id: string;
  title: string;
  project: string;
  updatedAt: string;
}

export function runDocumentsCommands(program: Command): void {
  const documents = program.command('documents').description('Document commands');

  documents
    .command('list')
    .description('List documents in the workspace')
    .option('--project <key-or-id>', 'Filter by project')
    .option('--search <term>', 'Search document content')
    .action(async options => {
      try {
        const globalOpts = getGlobalOptions(program);
        const resolved = resolveConfig(program.opts<{ profile?: string }>().profile);
        const client = createLinearClient(resolved);

        let filter: Record<string, unknown> | undefined;
        if (options.project) {
          const project = await findProjectByKeyOrId(client, options.project);
          if (!project) {
            const out = emitError('not_found', `Project '${options.project}' not found`);
            process.stderr.write(out + '\n');
            process.exitCode = 1;
            return;
          }
          filter = { project: { id: { eq: project.id } } };
        }

        if (options.search) {
          const payload = await client.searchDocuments(options.search, {
            first: globalOpts.limit,
            after: globalOpts.cursor,
          });
          const rows = payload.nodes.map((doc: any) => mapDocumentRow(doc));
          const columns = documentColumns();
          const meta = emitPaginationMeta(
            payload.pageInfo?.endCursor ?? null,
            payload.pageInfo?.startCursor ?? null,
            rows.length
          );
          const body = renderList(rows, columns, { format: globalOpts.format, fields: globalOpts.fields });
          process.stdout.write(`${meta}\n${body}\n`);
          return;
        }

        const data = await client.documents({
          first: globalOpts.limit,
          after: globalOpts.cursor,
          filter,
        });
        const rows = data.nodes.map((doc: any) => mapDocumentRow(doc));
        const columns = documentColumns();
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

  documents
    .command('view')
    .description('View document detail')
    .argument('<id>', 'Document id')
    .option('--max-content-chars <n>', 'Maximum content characters', parseCount, 4000)
    .action(async (id: string, options) => {
      try {
        const resolved = resolveConfig(program.opts<{ profile?: string }>().profile);
        const client = createLinearClient(resolved);
        const document = await client.document(id);
        if (!document) {
          const out = emitError('not_found', `Document '${id}' not found`);
          process.stderr.write(out + '\n');
          process.exitCode = 1;
          return;
        }

        const [project, creator] = await Promise.all([
          document.project ? document.project : undefined,
          document.creator ? document.creator : undefined,
        ]);

        const fields: Record<string, string> = {
          DOCUMENT: `${document.id ?? ''}`,
          TITLE: document.title ?? '',
          PROJECT: project?.name ?? '',
          UPDATED_AT: document.updatedAt?.toISOString?.() ?? '',
          AUTHOR: creator?.name ?? '',
          URL: document.url ?? '',
        };

        let output = emitDetailBlock('DOCUMENT_DETAIL', fields);
        const contentInfo = truncateMultiline(document.content ?? '', options.maxContentChars);
        output += `\nCONTENT_START\n${contentInfo.text}\nCONTENT_END\n`;
        if (contentInfo.truncated) {
          output += 'CONTENT_TRUNCATED: true\n';
        }
        process.stdout.write(output);
      } catch (error) {
        const parsed = parseLinearError(error);
        const out = emitError(parsed.code, parsed.message);
        process.stderr.write(out + '\n');
        process.exitCode = 1;
      }
    });
}

function documentColumns(): ColumnDefinition<DocumentRow>[] {
  return [
    { key: 'id', header: 'id', value: row => row.id },
    { key: 'title', header: 'title', value: row => row.title },
    { key: 'project', header: 'project', value: row => row.project },
    { key: 'updatedAt', header: 'updatedAt', value: row => row.updatedAt },
  ];
}

function mapDocumentRow(doc: any): DocumentRow {
  return {
    id: doc.id ?? '',
    title: sanitizeSingleLine(doc.title ?? ''),
    project: doc.projectId ?? '-',
    updatedAt: doc.updatedAt?.toISOString?.() ?? doc.createdAt?.toISOString?.() ?? '',
  };
}

function parseCount(value: string): number {
  const parsed = parseInt(value, 10);
  return Number.isNaN(parsed) ? 0 : parsed;
}
