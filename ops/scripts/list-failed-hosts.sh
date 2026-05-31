#!/usr/bin/env bash
set -euo pipefail

log_file="${1:-logs/ansible.log}"

if [[ ! -f "$log_file" ]]; then
  echo "log file not found: $log_file"
  exit 2
fi

grep -Ei 'fatal:|failed=|unreachable=|FAILED!|UNREACHABLE!' "$log_file" || true
