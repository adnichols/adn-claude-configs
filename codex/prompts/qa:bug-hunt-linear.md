Run a focused visual QA sweep, concentrating on bugs introduced or surfaced within the last 7 days, and log each validated issue directly to Linear without implementing fixes.

## Investigation Scope
- Prioritize areas touched by recent commits (`git log --since=7.days`, `git diff --stat`) and any high-traffic UI flows.
- Exercise end-to-end happy paths, edge cases, and responsive breakpoints. Emphasize usability defects (layout breakage, misaligned components, inaccessible interactions, blocking validation, unreadable copy, incorrect theming).
- Ignore pure performance issues, micro-optimizations, or speculative security concerns unless they obviously affect baseline usage.

## Evidence Collection
- For every suspected bug, reproduce it twice to confirm determinism; capture console/network logs and screenshots or recordings when helpful.
- Document environment (branch/commit, browser/device, viewport, feature flags) so another engineer can replay.
- Track blockers preventing investigation; note partial coverage when timeboxes expire.

## Linear Issue Workflow
- Operate on the Linear workspace directly via MCP tools. Before creating issues, ensure the `AIFound` label exists (create it if missing) and reference the canonical `bug` label.
- File each issue in the "Doc Thingy" project, backlog state. Title format: `[Bug] <Area> - <Short Symptom>`.
- Issue body must include:
  - **Summary**: one–two sentences describing the visual defect and user impact.
  - **Environment**: commit hash, browser/device, viewport, relevant flags.
  - **Steps to Reproduce**: numbered list from clean start to failure.
  - **Expected vs Actual**: bullet pair.
  - **Assets**: embed screenshot/video references or attach uploaded files.
  - **Suspected Cause**: optional hypothesis referencing code files or recent PRs (no fixes).
- Create issues as soon as each bug is confirmed—do not batch at the end. Verify each API call succeeds and capture the returned issue identifier.

## Completion Criteria
- Surface up to 10 highest-impact visual/UX bugs. If fewer than 10 exist, explain coverage gaps and remaining areas to audit.
- Produce a final report summarizing:
  - Total issues filed with Linear IDs/URLs.
  - Key themes or modules affected.
  - Outstanding risks or follow-up investigations.
- Leave repository in its original state (no code changes committed or staged) and provide next-step recommendations for manual engineers returning in the morning.
