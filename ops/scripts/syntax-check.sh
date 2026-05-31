#!/usr/bin/env bash
set -euo pipefail

cd "$(dirname "$0")/.."
ansible-playbook -i inventories/dev/hosts.ini playbooks/site.yml --syntax-check
