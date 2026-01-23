#!/usr/bin/env bash
set -euo pipefail

# Default agent runner for Ralph. Override per user or project.
AGENT_CMD="${AGENT_CMD:-codex}"
