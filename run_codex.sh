#!/usr/bin/env bash

# Wrapper script to launch Codex with workspace-write sandboxing, no approval prompts,
# and workspace network access allowed. Forwards all arguments to Codex.

set -euo pipefail

exec codex \
  --full-auto \
  -c sandbox_workspace_write.network_access=true \
  "$@"
