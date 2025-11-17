import { Command } from 'commander';
import { runAuthCommands } from './commands/auth.js';
import { runIssuesCommands } from './commands/issues.js';
import { runTeamsCommands } from './commands/teams.js';
import { runProjectsCommands } from './commands/projects.js';
import { runCyclesCommands } from './commands/cycles.js';
import { runLabelsCommands } from './commands/labels.js';
import { runUsersCommands } from './commands/users.js';
import { runDocumentsCommands } from './commands/documents.js';
import { runRoadmapsCommands } from './commands/roadmaps.js';
import { runMilestonesCommands } from './commands/milestones.js';
import { runNotificationsCommands } from './commands/notifications.js';
import { loadExtensions } from './extensions.js';

export async function main(argv: string[] = process.argv.slice(2)) {
  const program = new Command();

  program
    .name('ltui')
    .description('Token-efficient Linear CLI for AI coding agents')
    .option('--profile <name>', 'profile name')
    .option('--format <fmt>', 'output format (tsv|table|detail|json)', 'tsv')
    .option('--fields <fields>', 'comma-separated list of fields')
    .option('--limit <n>', 'limit item count', (value: string) => parseInt(value, 10))
    .option('--cursor <cursor>', 'pagination cursor')
    .option('--agent', 'enable agent mode', true)
    .option('--no-agent', 'disable agent mode');
  program.enablePositionalOptions();

  runAuthCommands(program);
  runIssuesCommands(program);
  runTeamsCommands(program);
  runProjectsCommands(program);
  runCyclesCommands(program);
  runLabelsCommands(program);
  runUsersCommands(program);
  runDocumentsCommands(program);
  runRoadmapsCommands(program);
  runMilestonesCommands(program);
  runNotificationsCommands(program);

  await loadExtensions(program);

  await program.parseAsync(argv, { from: 'user' });
}
