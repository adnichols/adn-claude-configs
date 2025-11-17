import type { Command } from 'commander';
import type { OutputFormat } from './format.js';

export interface GlobalOptions {
  format: OutputFormat;
  fields?: string[];
  limit: number;
  cursor: string | null;
  agentMode: boolean;
}

export function getGlobalOptions(program: Command): GlobalOptions {
  const opts = program.opts<{
    format?: string;
    fields?: string;
    limit?: number;
    cursor?: string;
    agent?: boolean;
  }>();

  const format = (opts.format ?? 'tsv').toLowerCase() as OutputFormat;
  const fields = opts.fields
    ? opts.fields
        .split(',')
        .map(field => field.trim())
        .filter(Boolean)
    : undefined;

  const limit = typeof opts.limit === 'number' && !Number.isNaN(opts.limit) ? opts.limit : 20;
  const cursor = opts.cursor ?? null;
  const agentMode = opts.agent !== undefined ? opts.agent : true;

  return {
    format,
    fields,
    limit,
    cursor,
    agentMode,
  };
}
