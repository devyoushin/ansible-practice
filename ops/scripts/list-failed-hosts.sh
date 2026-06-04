#!/usr/bin/env bash
set -euo pipefail

script_dir="$(cd "$(dirname "$0")" && pwd)"
ops_dir="$(cd "$script_dir/.." && pwd)"
log_file="${1:-$ops_dir/runtime/logs/ansible.log}"

if [[ ! -f "$log_file" ]]; then
  echo "log file not found: $log_file"
  exit 2
fi

grep -Ei 'fatal:|failed=|unreachable=|FAILED!|UNREACHABLE!' "$log_file" || true
