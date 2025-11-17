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

interface NotificationRow {
  id: string;
  type: string;
  read: string;
  createdAt: string;
}

export function runNotificationsCommands(program: Command): void {
  program
    .command('notifications')
    .description('Notification commands')
    .option('--unread-only', 'Only include unread notifications')
    .action(async options => {
      try {
        const globalOpts = getGlobalOptions(program);
        const resolved = resolveConfig(program.opts<{ profile?: string }>().profile);
        const client = createLinearClient(resolved);

        const filter: Record<string, unknown> = {};
        if (options.unreadOnly) {
          filter.readAt = { isNull: true };
        }

        const data = await client.notifications({
          first: globalOpts.limit,
          after: globalOpts.cursor,
          filter,
        });

        const rows: NotificationRow[] = data.nodes.map((notification: any) => ({
          id: notification.id ?? '',
          type: notification.type ?? '',
          read: notification.readAt ? 'true' : 'false',
          createdAt: notification.createdAt?.toISOString?.() ?? '',
        }));

        const columns: ColumnDefinition<NotificationRow>[] = [
          { key: 'id', header: 'id', value: row => row.id },
          { key: 'type', header: 'type', value: row => row.type },
          { key: 'read', header: 'read', value: row => row.read },
          { key: 'createdAt', header: 'createdAt', value: row => row.createdAt },
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
