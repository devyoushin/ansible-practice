#!/usr/bin/env bash
set -euo pipefail

env_name="${1:-dev}"
playbook="${2:-site.yml}"

case "$env_name" in
  dev|staging|prod) ;;
  *)
    echo "usage: $0 <dev|staging|prod> [playbook.yml]"
    exit 2
    ;;
esac

cd "$(dirname "$0")/.."
ansible-playbook -i "inventories/${env_name}/hosts.ini" "playbooks/${playbook}" --check --diff
