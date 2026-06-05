#!/usr/bin/env bash
set -euo pipefail

cd "$(dirname "$0")/.."
export ANSIBLE_CONFIG="${ANSIBLE_CONFIG:-config/ansible.cfg}"
ansible-playbook -i inventories/dev/hosts.ini playbooks/site.yml --syntax-check
