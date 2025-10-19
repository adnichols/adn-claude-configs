# Repository Guidelines

## Project Structure & Module Organization
- `agents/` holds the production agent briefs; reuse templates in `agents/templates/` when introducing new roles so naming stays consistent (`<role>-<modifier>.md`).
- `commands/` defines the slash-command workflows consumed by Claude Code; mirror existing markdown structure when adding command docs.
- `tools/gen_agents.py` contains the Jinja-driven generator for agent variants; keep supporting helpers alongside it in `tools/`.
- Support docs, examples, and reports land in `docs/`, `examples/`, and `reports/` respectively; task outputs and specs belong in `tasks/`.
- Tests, fixtures, and validation data live under `test/` (fixtures only today—add new suites beside them), while workspace-specific editor settings live in `vscode/`.

## Build, Test, and Development Commands
- `pip install -r requirements.txt` — install dependencies for agent generation, linting, and validation.
- `./install.sh` — symlink this repo into `~/.claude/` with backups; rerun after structural changes to propagate updates.
- `pytest -q` — execute repository tests (add cases under `test/`); prefer `pytest --cov=tools --cov=agents` when validating coverage-sensitive work.
- `black .` or `black --check .` — format or verify Python sources; run before committing generator changes.
- `mypy tools/ agents/templates` — ensure type safety for generator scripts and any supporting utilities.

## Coding Style & Naming Conventions
- Python code uses 4-space indentation, `black` formatting, and `mypy` typing; keep functions small and pure because generators run inside automation.
- Favour `snake_case` for Python identifiers, kebab-case for agent and command filenames, and title-case headings inside markdown briefs.
- Store reusable prose snippets in templates rather than hand-editing generated files; when manual edits are required, note deviations in the file header.

## Testing Guidelines
- Organise new tests as `test_*.py` within `test/`; colocate reusable sample specs in `test/fixtures/`.
- Target generator behaviour with focused unit tests and add regression cases whenever updating templates or validation logic.
- Require a clean `pytest -q`, `black --check .`, and `mypy tools/` run before requesting review; include coverage output when it informs risk.

## Commit & Pull Request Guidelines
- Follow Conventional Commit prefixes observed in history (`feat:`, `fix:`, `docs:`, `chore:`); keep scope narrow and commits reviewable.
- Pull requests should outline intent, impacted agents/commands, and validation evidence (commands run, configs synced). Link relevant issues or tasks and attach before/after snippets when editing agent briefs.
- Double-check `sync-claude-config.sh --dry-run` when changes affect installation shape, and note any manual steps required for downstream consumers.
