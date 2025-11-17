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
import {
  findProjectByKeyOrId,
  findTeamByKeyOrId,
  findWorkflowStateByNameOrId,
  parseLinearError,
  readTextOrPath,
  resolveAssigneeId,
  resolveIssueByIdOrKey,
  resolveLabelIds,
  isUuid,
} from '../linear.js';
import { getSavedQuery, listSavedQueries, removeQuery, saveQuery, SavedQueryDefinition } from '../queries.js';

interface IssueListRow {
  id: string;
  key: string;
  identifier: string;
  title: string;
  state: string;
  priority: string;
  assignee: string;
  labels: string;
  project: string;
  updatedAt: string;
}

interface IssueListCommandOptions {
  team?: string;
  project?: string;
  state?: string;
  assignee?: string;
  label?: string[];
  search?: string;
  saved?: string;
  updatedSince?: string;
  createdSince?: string;
}

export function runIssuesCommands(program: Command): void {
  const issues = program.command('issues').description('Issue operations');

  issues
    .command('list')
    .description('List issues')
    .option('--team <key-or-id>', 'Team key or id')
    .option('--project <key-or-id>', 'Project key or id')
    .option('--state <name-or-id>', 'State name or id')
    .option('--assignee <me|email|id>', 'Assignee')
    .option('--label <name-or-id>', 'Label', collect, [])
    .option('--search <query>', 'Search query')
    .option('--updated-since <iso>', 'Updated since ISO timestamp')
    .option('--created-since <iso>', 'Created since ISO timestamp')
    .option('--saved <name>', 'Saved query name to apply')
    .action(async options => {
      try {
        const globalOpts = getGlobalOptions(program);
        const resolved = resolveConfig(program.opts<{ profile?: string }>().profile);
        const client = createLinearClient(resolved);

        const effectiveOptions = mergeSavedQueryOptions(options);
        const filter = await buildIssueFilter(effectiveOptions);
        const params: Record<string, unknown> = {
          first: globalOpts.limit,
          after: globalOpts.cursor,
          filter,
          sort: { updatedAt: { order: 'Descending' } },
        };

        const data = effectiveOptions.search
          ? await client.searchIssues(effectiveOptions.search, params)
          : await client.issues(params);

        const issueNodes = effectiveOptions.search
          ? await Promise.all(data.nodes.map((node: any) => client.issue(node.id)))
          : data.nodes;

        const rows: IssueListRow[] = await Promise.all(
          issueNodes.map((node: any) => mapIssueToRow(node))
        );
        const columns: ColumnDefinition<IssueListRow>[] = [
          { key: 'id', header: 'id', value: row => row.id },
          { key: 'key', header: 'key', value: row => row.key },
          { key: 'identifier', header: 'identifier', value: row => row.identifier },
          { key: 'title', header: 'title', value: row => row.title },
          { key: 'state', header: 'state', value: row => row.state },
          { key: 'priority', header: 'priority', value: row => row.priority },
          { key: 'assignee', header: 'assignee', value: row => row.assignee },
          { key: 'labels', header: 'labels', value: row => row.labels },
          { key: 'project', header: 'project', value: row => row.project },
          { key: 'updatedAt', header: 'updatedAt', value: row => row.updatedAt },
        ];

        const meta = emitPaginationMeta(
          data.pageInfo?.endCursor ?? null,
          data.pageInfo?.startCursor ?? null,
          rows.length
        );
        const body = renderList(rows, columns, {
          format: globalOpts.format,
          fields: globalOpts.fields,
        });
        process.stdout.write(`${meta}\n${body}\n`);
      } catch (error) {
        writeError(error);
      }
    });

  issues
    .command('view')
    .description('View an issue')
    .argument('<id>', 'Issue id or key')
    .option('--include-comments', 'Include comments')
    .option('--include-history', 'Include history')
    .option('--max-description-chars <n>', 'Max description chars', parseNumber, 4000)
    .option('--max-comment-chars <n>', 'Max comment chars', parseNumber, 500)
    .action(async (ref: string, options) => {
      try {
        const resolved = resolveConfig(program.opts<{ profile?: string }>().profile);
        const client = createLinearClient(resolved);
        const issue = await resolveIssueByIdOrKey(client, ref);
        if (!issue) {
          const out = emitError('not_found', `Issue '${ref}' not found`);
          process.stderr.write(out + '\n');
          process.exitCode = 1;
          return;
        }

        const descriptionInfo = truncateMultiline(issue.description ?? '', options.maxDescriptionChars);
        const fields: Record<string, string> = {
          ISSUE: `${issue.identifier ?? ''} (${issue.id ?? ''})`,
          TITLE: issue.title ?? '',
          STATE: issue.state?.name ?? '',
          PRIORITY: issue.priority?.toString() ?? '',
          TEAM: issue.team?.key ?? '',
          PROJECT: issue.project?.name ?? '',
          ASSIGNEE: issue.assignee?.name ?? '',
          LABELS: extractLabelNames(issue).join(','),
          CREATED_AT: issue.createdAt?.toISOString?.() ?? '',
          UPDATED_AT: issue.updatedAt?.toISOString?.() ?? '',
        };

        let output = emitDetailBlock('ISSUE_DETAIL', fields);
        output += `\nDESCRIPTION_START\n${descriptionInfo.text}\nDESCRIPTION_END\n`;
        if (descriptionInfo.truncated) {
          output += 'DESCRIPTION_TRUNCATED: true\n';
        }

        if (options.includeComments) {
          const comments = await issue.comments({ first: 50 });
          const lines: string[] = ['COMMENTS_START'];
          for (const comment of comments.nodes) {
            const truncated = truncateMultiline(comment.body ?? '', options.maxCommentChars);
            const row = [
              comment.id,
              comment.user?.name ?? '',
              comment.createdAt?.toISOString() ?? '',
              sanitizeSingleLine(truncated.text),
            ];
            lines.push(row.join('\t'));
            if (truncated.truncated) {
              lines.push(`COMMENT_TRUNCATED: ${comment.id}`);
            }
          }
          lines.push('COMMENTS_END');
          output += `${lines.join('\n')}\n`;
        }

        if (options.includeHistory) {
          const historyConnection = await issue.history({
            first: 50,
            sort: { createdAt: { order: 'Ascending' } },
          });
          const lines: string[] = ['HISTORY_START'];
          for (const entry of historyConnection.nodes) {
            const actor = entry.actor?.name ?? entry.actorId ?? '';
            const changeType = determineHistoryType(entry);
            const fromValue = historyFromValue(entry);
            const toValue = historyToValue(entry);
            const row = [
              entry.createdAt?.toISOString() ?? '',
              sanitizeSingleLine(actor),
              changeType,
              sanitizeSingleLine(fromValue),
              sanitizeSingleLine(toValue),
            ];
            lines.push(row.join('\t'));
          }
          lines.push('HISTORY_END');
          output += `${lines.join('\n')}\n`;
        }

        process.stdout.write(output);
      } catch (error) {
        writeError(error);
      }
    });

  issues
    .command('create')
    .description('Create an issue')
    .option('--team <key>', 'Team key (default from .ltui.json)')
    .option('--project <key-or-id>', 'Project key or id (default from .ltui.json)')
    .requiredOption('--title <title>', 'Issue title')
    .option('--description <text-or-@path>', 'Description text or @path')
    .option('--state <name-or-id>', 'State name or id')
    .option('--label <name-or-id>', 'Label', collect, [])
    .option('--assignee <me|email|id>', 'Assignee')
    .option('--priority <0-4>', 'Priority', parseNumber)
    .action(async options => {
      try {
        const resolved = resolveConfig(program.opts<{ profile?: string }>().profile);
        const client = createLinearClient(resolved);

        const configDefaults = resolved.projectConfig ?? {};
        const teamRef: string | undefined = options.team ?? configDefaults.teamKey;
        if (!teamRef) {
          const out = emitError(
            'validation_error',
            'Team is required to create an issue (use --team or configure .ltui.json)'
          );
          process.stderr.write(out + '\n');
          process.exitCode = 1;
          return;
        }

        const team = await findTeamByKeyOrId(client, teamRef);
        if (!team) {
          const out = emitError('not_found', `Team '${teamRef}' not found`);
          process.stderr.write(out + '\n');
          process.exitCode = 1;
          return;
        }

        let projectId: string | undefined;
        const projectRef: string | undefined = options.project ?? configDefaults.projectId;
        if (projectRef) {
          const project = await findProjectByKeyOrId(client, projectRef);
          if (!project) {
            const out = emitError('not_found', `Project '${projectRef}' not found`);
            process.stderr.write(out + '\n');
            process.exitCode = 1;
            return;
          }
          projectId = project.id;
        }

        let description: string | undefined;
        if (options.description) {
          description = readTextOrPath(options.description);
        }

        const desiredState = options.state ?? configDefaults.defaultIssueState;
        let stateId: string | undefined;
        if (desiredState) {
          const state = await findWorkflowStateByNameOrId(client, team.id, desiredState);
          if (!state) {
            const out = emitError('not_found', `Workflow state '${desiredState}' not found`);
            process.stderr.write(out + '\n');
            process.exitCode = 1;
            return;
          }
          stateId = state.id;
        }

        const labelNames = [...(configDefaults.defaultLabels ?? []), ...(options.label ?? [])];
        const labelIds = await resolveLabelIds(client, labelNames, team.id);

        const assigneeRef: string | undefined = options.assignee ?? configDefaults.defaultAssignee;
        let assigneeId: string | undefined;
        if (assigneeRef) {
          assigneeId = await resolveAssigneeId(client, assigneeRef);
          if (!assigneeId) {
            const out = emitError('not_found', `Assignee '${assigneeRef}' not found`);
            process.stderr.write(out + '\n');
            process.exitCode = 1;
            return;
          }
        }

        const input: Record<string, unknown> = {
          teamId: team.id,
          title: options.title as string,
        };
        if (projectId) input.projectId = projectId;
        if (description !== undefined) input.description = description;
        if (stateId) input.stateId = stateId;
        if (labelIds.length > 0) input.labelIds = labelIds;
        if (assigneeId) input.assigneeId = assigneeId;
        if (typeof options.priority === 'number' && !Number.isNaN(options.priority)) {
          input.priority = options.priority;
        }

        const payload = await client.createIssue(input as any);
        const issue = payload.issue ? await payload.issue : null;
        if (!issue) {
          const out = emitError('api_error', 'Failed to load created issue');
          process.stderr.write(out + '\n');
          process.exitCode = 1;
          return;
        }
        const block = await formatIssueSummaryBlock('ISSUE_CREATED', issue);
        process.stdout.write(block + '\n');
      } catch (error) {
        writeError(error);
      }
    });

  issues
    .command('update')
    .description('Update an issue')
    .argument('<issue-id-or-key>', 'Issue id or key')
    .option('--team <key>', 'Team key override')
    .option('--project <key-or-id>', 'Project key or id')
    .option('--title <title>', 'Updated title')
    .option('--description <text-or-@path>', 'Description text or @path')
    .option('--state <name-or-id>', 'State name or id')
    .option('--label <name-or-id>', 'Replace labels with these', collect, [])
    .option('--add-label <name-or-id>', 'Labels to add', collect, [])
    .option('--remove-label <name-or-id>', 'Labels to remove', collect, [])
    .option('--assignee <me|email|id>', 'Assignee')
    .option('--priority <0-4>', 'Priority', parseNumber)
    .option('--estimate <number>', 'Estimate', parseNumber)
    .option('--due <iso>', 'Due date ISO string')
    .action(async (ref: string, options) => {
      try {
        const resolved = resolveConfig(program.opts<{ profile?: string }>().profile);
        const client = createLinearClient(resolved);
        const issue = await resolveIssueByIdOrKey(client, ref);
        if (!issue) {
          const out = emitError('not_found', `Issue '${ref}' not found`);
          process.stderr.write(out + '\n');
          process.exitCode = 1;
          return;
        }

        const input: Record<string, unknown> = {};
        let changed = false;

        let effectiveTeamId: string | undefined = issue.team?.id;
        if (options.team) {
          const team = await findTeamByKeyOrId(client, options.team);
          if (!team) {
            const out = emitError('not_found', `Team '${options.team}' not found`);
            process.stderr.write(out + '\n');
            process.exitCode = 1;
            return;
          }
          input.teamId = team.id;
          effectiveTeamId = team.id;
          changed = true;
        }

        if (options.project) {
          const project = await findProjectByKeyOrId(client, options.project);
          if (!project) {
            const out = emitError('not_found', `Project '${options.project}' not found`);
            process.stderr.write(out + '\n');
            process.exitCode = 1;
            return;
          }
          input.projectId = project.id;
          changed = true;
        }

        if (options.title) {
          input.title = options.title;
          changed = true;
        }

        if (options.description) {
          input.description = readTextOrPath(options.description);
          changed = true;
        }

        if (options.state) {
          if (!effectiveTeamId) {
            const out = emitError('validation_error', 'Cannot change state without team context');
            process.stderr.write(out + '\n');
            process.exitCode = 1;
            return;
          }
          const state = await findWorkflowStateByNameOrId(client, effectiveTeamId, options.state);
          if (!state) {
            const out = emitError('not_found', `Workflow state '${options.state}' not found`);
            process.stderr.write(out + '\n');
            process.exitCode = 1;
            return;
          }
          input.stateId = state.id;
          changed = true;
        }

        if (options.assignee) {
          const assigneeId = await resolveAssigneeId(client, options.assignee);
          if (!assigneeId) {
            const out = emitError('not_found', `Assignee '${options.assignee}' not found`);
            process.stderr.write(out + '\n');
            process.exitCode = 1;
            return;
          }
          input.assigneeId = assigneeId;
          changed = true;
        }

        if (typeof options.priority === 'number' && !Number.isNaN(options.priority)) {
          input.priority = options.priority;
          changed = true;
        }

        if (typeof options.estimate === 'number' && !Number.isNaN(options.estimate)) {
          input.estimate = options.estimate;
          changed = true;
        }

        if (options.due) {
          input.dueDate = options.due;
          changed = true;
        }

        const replaceLabels: string[] = options.label ?? [];
        const addLabels: string[] = options.addLabel ?? [];
        const removeLabels: string[] = options.removeLabel ?? [];
        if (replaceLabels.length || addLabels.length || removeLabels.length) {
          if (!effectiveTeamId) {
            const out = emitError(
              'validation_error',
              'Cannot modify labels without determining the team'
            );
            process.stderr.write(out + '\n');
            process.exitCode = 1;
            return;
          }

          const labelConnection =
            typeof issue.labels === 'function'
              ? await issue.labels({ first: 50 })
              : { nodes: issue.labels ?? [] };
          const currentLabels = labelConnection.nodes ?? [];
          let working: string[] = replaceLabels.length
            ? await resolveLabelIds(client, replaceLabels, effectiveTeamId)
            : (currentLabels.map((label: any) => label.id) ?? []);

          if (removeLabels.length > 0) {
            for (const name of removeLabels) {
              const label = currentLabels.find((item: any) => item.name === name);
              if (!label) {
                const out = emitError('not_found', `Label '${name}' is not on the issue`);
                process.stderr.write(out + '\n');
                process.exitCode = 1;
                return;
              }
              working = working.filter(id => id !== label.id);
            }
          }

          if (addLabels.length > 0) {
            const addIds = await resolveLabelIds(client, addLabels, effectiveTeamId);
            for (const id of addIds) {
              if (!working.includes(id)) working.push(id);
            }
          }

          input.labelIds = working;
          changed = true;
        }

        if (!changed) {
          const out = emitError('validation_error', 'No updates specified');
          process.stderr.write(out + '\n');
          process.exitCode = 1;
          return;
        }

        await client.updateIssue(issue.id, input as any);
        const updatedIssue = await client.issue(issue.id);
        const block = await formatIssueSummaryBlock('ISSUE_UPDATED', updatedIssue);
        process.stdout.write(block + '\n');
      } catch (error) {
        writeError(error);
      }
    });

  issues
    .command('comment')
    .description('Add a comment to an issue')
    .argument('<issue-id-or-key>', 'Issue id or key')
    .requiredOption('--body <text-or-@path>', 'Comment body or @path')
    .action(async (ref: string, options) => {
      try {
        const resolved = resolveConfig(program.opts<{ profile?: string }>().profile);
        const client = createLinearClient(resolved);
        const issue = await resolveIssueByIdOrKey(client, ref);
        if (!issue) {
          const out = emitError('not_found', `Issue '${ref}' not found`);
          process.stderr.write(out + '\n');
          process.exitCode = 1;
          return;
        }

        const body = readTextOrPath(options.body);
        const payload = await client.createComment({ issueId: issue.id, body });
        const comment = payload.comment ? await payload.comment : undefined;
        const author = comment?.user ? await comment.user : undefined;
        const block = emitDetailBlock('COMMENT_CREATED', {
          COMMENT: `${comment?.id ?? ''}`,
          AUTHOR: author?.name ?? '',
          CREATED_AT: comment?.createdAt?.toISOString?.() ?? '',
          ISSUE: issue.identifier ?? issue.id,
        });
        process.stdout.write(block + '\n');
      } catch (error) {
        writeError(error);
      }
    });

  issues
    .command('link')
    .description('Attach a link to an issue')
    .argument('<issue-id-or-key>', 'Issue id or key')
    .requiredOption('--url <url>', 'URL to attach')
    .option('--title <title>', 'Title for the attachment')
    .option('--branch <branch>', 'Branch name metadata')
    .option('--commit <sha>', 'Commit SHA metadata')
    .action(async (ref: string, options) => {
      try {
        const resolved = resolveConfig(program.opts<{ profile?: string }>().profile);
        const client = createLinearClient(resolved);
        const issue = await resolveIssueByIdOrKey(client, ref);
        if (!issue) {
          const out = emitError('not_found', `Issue '${ref}' not found`);
          process.stderr.write(out + '\n');
          process.exitCode = 1;
          return;
        }

        const attachmentInput: Record<string, unknown> = {
          issueId: issue.id,
          url: options.url,
          title: options.title ?? options.url,
        };
        const metadata: Record<string, string> = {};
        if (options.branch) metadata.branch = options.branch;
        if (options.commit) metadata.commit = options.commit;
        if (Object.keys(metadata).length > 0) {
          attachmentInput.metadata = metadata;
          const subtitleParts: string[] = [];
          if (options.branch) subtitleParts.push(`branch:${options.branch}`);
          if (options.commit) subtitleParts.push(`commit:${options.commit}`);
          attachmentInput.subtitle = subtitleParts.join(' ');
        }

        const payload = await client.createAttachment(attachmentInput as any);
        const attachment = payload.attachment ? await payload.attachment : undefined;
        const block = emitDetailBlock('LINK_ATTACHED', {
          ATTACHMENT: `${attachment?.id ?? ''}`,
          TITLE: attachment?.title ?? '',
          URL: attachment?.url ?? '',
          ISSUE: issue.identifier ?? issue.id,
          BRANCH: options.branch ?? '',
          COMMIT: options.commit ?? '',
        });
        process.stdout.write(block + '\n');
      } catch (error) {
        writeError(error);
      }
    });

  issues
    .command('relate')
    .description('Relate a child issue to a parent')
    .argument('<child-id-or-key>', 'Child issue id or key')
    .requiredOption('--parent <parent-id-or-key>', 'Parent issue id or key')
    .action(async (childRef: string, options) => {
      try {
        const resolved = resolveConfig(program.opts<{ profile?: string }>().profile);
        const client = createLinearClient(resolved);
        const child = await resolveIssueByIdOrKey(client, childRef);
        const parent = await resolveIssueByIdOrKey(client, options.parent);
        if (!child || !parent) {
          const out = emitError('not_found', 'Could not resolve child or parent issue');
          process.stderr.write(out + '\n');
          process.exitCode = 1;
          return;
        }

        await client.updateIssue(child.id, { parentId: parent.id });
        const block = emitDetailBlock('RELATIONSHIP_UPDATED', {
          CHILD: `${child.identifier ?? child.id}`,
          PARENT: `${parent.identifier ?? parent.id}`,
          RELATION: 'parent-child',
        });
        process.stdout.write(block + '\n');
      } catch (error) {
        writeError(error);
      }
    });

  issues
    .command('block')
    .description('Mark an issue as blocked by another issue')
    .argument('<issue-id-or-key>', 'Issue id or key')
    .requiredOption('--blocked-by <other-id-or-key>', 'Issue causing the block')
    .action(async (issueRef: string, options) => {
      try {
        const resolved = resolveConfig(program.opts<{ profile?: string }>().profile);
        const client = createLinearClient(resolved);
        const issue = await resolveIssueByIdOrKey(client, issueRef);
        const blocker = await resolveIssueByIdOrKey(client, options.blockedBy);
        if (!issue || !blocker) {
          const out = emitError('not_found', 'Could not resolve issue or blocker');
          process.stderr.write(out + '\n');
          process.exitCode = 1;
          return;
        }

        await client.createIssueRelation({
          issueId: blocker.id,
          relatedIssueId: issue.id,
          type: 'blocks' as any,
        });

        const block = emitDetailBlock('RELATIONSHIP_UPDATED', {
          ISSUE: `${issue.identifier ?? issue.id}`,
          BLOCKED_BY: `${blocker.identifier ?? blocker.id}`,
          RELATION: 'blocks',
        });
        process.stdout.write(block + '\n');
      } catch (error) {
        writeError(error);
      }
    });

  const saved = issues.command('saved').description('Manage saved issue queries');

  saved
    .command('list')
    .description('List saved issue queries')
    .action(() => {
      const savedQueries = listSavedQueries();
      const globalOpts = getGlobalOptions(program);
      const columns: ColumnDefinition<SavedQueryDefinition>[] = [
        { key: 'name', header: 'name', value: row => row.name },
        { key: 'search', header: 'search', value: row => row.search ?? '' },
        { key: 'team', header: 'team', value: row => row.team ?? '' },
        { key: 'project', header: 'project', value: row => row.project ?? '' },
        { key: 'state', header: 'state', value: row => row.state ?? '' },
        {
          key: 'labels',
          header: 'labels',
          value: row => (row.labels ?? []).join(','),
        },
      ];
      const meta = emitPaginationMeta(null, null, savedQueries.length);
      const body = renderList(savedQueries, columns, {
        format: globalOpts.format,
        fields: globalOpts.fields,
      });
      process.stdout.write(`${meta}\n${body}\n`);
    });

  saved
    .command('add')
    .description('Add or update a saved query')
    .requiredOption('--name <name>', 'Query name')
    .option('--search <query>', 'Search term')
    .option('--team <key-or-id>', 'Team filter')
    .option('--project <key-or-id>', 'Project filter')
    .option('--state <name-or-id>', 'Workflow state')
    .option('--assignee <me|email|id>', 'Assignee filter')
    .option('--label <name-or-id>', 'Label filter', collect, [])
    .option('--updated-since <iso>', 'Updated since ISO timestamp')
    .option('--created-since <iso>', 'Created since ISO timestamp')
    .action(options => {
      const definition: SavedQueryDefinition = {
        name: options.name,
        search: options.search,
        team: options.team,
        project: options.project,
        state: options.state,
        assignee: options.assignee,
        labels: options.label && options.label.length > 0 ? options.label : undefined,
        updatedSince: options.updatedSince,
        createdSince: options.createdSince,
      };
      saveQuery(definition);
      const block = emitDetailBlock('SAVED_QUERY_ADDED', {
        NAME: definition.name,
        TEAM: definition.team ?? '',
        PROJECT: definition.project ?? '',
        STATE: definition.state ?? '',
        LABELS: (definition.labels ?? []).join(','),
      });
      process.stdout.write(block + '\n');
    });

  saved
    .command('remove')
    .description('Remove a saved query')
    .requiredOption('--name <name>', 'Query name')
    .action(options => {
      removeQuery(options.name);
      const block = emitDetailBlock('SAVED_QUERY_REMOVED', {
        NAME: options.name,
      });
      process.stdout.write(block + '\n');
    });
}

function mergeSavedQueryOptions(options: IssueListCommandOptions): IssueListCommandOptions {
  if (!options.saved) {
    return options;
  }
  const saved = getSavedQuery(options.saved);
  if (!saved) {
    throw new Error(`not_found Saved query '${options.saved}' not found`);
  }
  const labelValues = options.label && options.label.length > 0 ? options.label : saved.labels ?? [];
  return {
    ...options,
    team: options.team ?? saved.team,
    project: options.project ?? saved.project,
    state: options.state ?? saved.state,
    assignee: options.assignee ?? saved.assignee,
    label: labelValues,
    search: options.search ?? saved.search,
    updatedSince: options.updatedSince ?? saved.updatedSince,
    createdSince: options.createdSince ?? saved.createdSince,
  };
}

async function buildIssueFilter(options: Record<string, any>): Promise<Record<string, unknown>> {
  const filter: Record<string, unknown> = {};

  if (options.team) {
    const teamValue = String(options.team);
    const teamFilters: any[] = [
      { key: { eq: teamValue.toUpperCase() } },
      { name: { eq: teamValue } },
    ];
    if (isUuid(teamValue)) {
      teamFilters.unshift({ id: { eq: teamValue } });
    }
    filter.team = { or: teamFilters };
  }

  if (options.project) {
    const projectValue = String(options.project);
    const projectFilters: any[] = [
      { slugId: { eq: projectValue } },
      { name: { eq: projectValue } },
    ];
    if (isUuid(projectValue)) {
      projectFilters.unshift({ id: { eq: projectValue } });
    }
    filter.project = { or: projectFilters };
  }

  if (options.state) {
    const stateValue = String(options.state);
    const stateFilters: any[] = [{ name: { eq: stateValue } }];
    if (isUuid(stateValue)) {
      stateFilters.unshift({ id: { eq: stateValue } });
    }
    filter.state = { or: stateFilters };
  }

  if (options.assignee) {
    if (options.assignee === 'me') {
      filter.assignee = { isMe: { eq: true } };
    } else if (options.assignee.includes('@')) {
      filter.assignee = { email: { eq: options.assignee } };
    } else {
      const assigneeFilters: any[] = [{ name: { eq: options.assignee } }];
      if (isUuid(options.assignee)) {
        assigneeFilters.unshift({ id: { eq: options.assignee } });
      }
      filter.assignee = { or: assigneeFilters };
    }
  }

  if (options.label && options.label.length > 0) {
    filter.labels = {
      and: options.label.map((name: string) => ({ some: { name: { eq: name } } })),
    };
  }

  if (options.updatedSince) {
    filter.updatedAt = { gte: options.updatedSince };
  }

  if (options.createdSince) {
    filter.createdAt = { gte: options.createdSince };
  }

  return filter;
}

async function mapIssueToRow(issue: any): Promise<IssueListRow> {
  let labelNames: string[] = [];
  if (typeof issue.labels === 'function') {
    const connection = await issue.labels({ first: 25 });
    labelNames = connection.nodes.map((label: any) => label.name).filter(Boolean);
  } else {
    labelNames = extractLabelNames(issue);
  }
  const updatedAt =
    typeof issue.updatedAt?.toISOString === 'function'
      ? issue.updatedAt.toISOString()
      : issue.updatedAt ?? '';
  return {
    id: issue.id ?? '',
    key: issue.team?.key ?? '',
    identifier: issue.identifier ?? '',
    title: sanitizeSingleLine(issue.title ?? ''),
    state: issue.state?.name ?? '',
    priority: issue.priority?.toString() ?? '',
    assignee: issue.assignee?.name ?? '-',
    labels: labelNames.join(','),
    project: issue.project?.name ?? '-',
    updatedAt,
  };
}

function extractLabelNames(issue: any): string[] {
  if (Array.isArray(issue.labels)) {
    return issue.labels.map((label: any) => label.name).filter(Boolean);
  }
  if (issue.labels?.nodes) {
    return issue.labels.nodes.map((label: any) => label.name).filter(Boolean);
  }
  return [];
}

function determineHistoryType(entry: any): string {
  if (entry.toState || entry.fromState) return 'state';
  if (entry.toAssignee || entry.fromAssignee) return 'assignee';
  if (entry.toPriority || entry.fromPriority) return 'priority';
  if (entry.toProject || entry.fromProject) return 'project';
  if (entry.toTitle || entry.fromTitle) return 'title';
  return 'update';
}

function historyFromValue(entry: any): string {
  if (entry.fromState) return entry.fromState.name ?? '';
  if (entry.fromAssignee) return entry.fromAssignee.name ?? '';
  if (entry.fromPriority !== undefined) return String(entry.fromPriority);
  if (entry.fromProject) return entry.fromProject.name ?? '';
  if (entry.fromTitle) return entry.fromTitle;
  return '';
}

function historyToValue(entry: any): string {
  if (entry.toState) return entry.toState.name ?? '';
  if (entry.toAssignee) return entry.toAssignee.name ?? '';
  if (entry.toPriority !== undefined) return String(entry.toPriority);
  if (entry.toProject) return entry.toProject.name ?? '';
  if (entry.toTitle) return entry.toTitle;
  return '';
}

async function formatIssueSummaryBlock(header: string, issue: any): Promise<string> {
  const [state, team, project, assignee, labelsConnection] = await Promise.all([
    issue.state ? issue.state : undefined,
    issue.team ? issue.team : undefined,
    issue.project ? issue.project : undefined,
    issue.assignee ? issue.assignee : undefined,
    typeof issue.labels === 'function' ? issue.labels({ first: 25 }) : undefined,
  ]);

  const labelNames =
    labelsConnection?.nodes?.map((label: any) => label.name).filter(Boolean) ?? extractLabelNames(issue);

  const fields: Record<string, string> = {
    ISSUE: `${issue.identifier ?? ''} (${issue.id ?? ''})`,
    TITLE: issue.title ?? '',
    STATE: state?.name ?? '',
    PRIORITY: issue.priority?.toString() ?? '',
    TEAM: team?.key ?? '',
    PROJECT: project?.name ?? '',
    ASSIGNEE: assignee?.name ?? '',
    LABELS: labelNames.join(','),
  };

  return emitDetailBlock(header, fields);
}

function parseNumber(value: string): number {
  const parsed = parseInt(value, 10);
  return Number.isNaN(parsed) ? 0 : parsed;
}

function collect(value: string, previous: string[]): string[] {
  return [...previous, value];
}

function writeError(error: unknown): void {
  const parsed = parseLinearError(error);
  const out = emitError(parsed.code, parsed.message);
  process.stderr.write(out + '\n');
  process.exitCode = 1;
}
