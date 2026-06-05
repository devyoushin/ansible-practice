# Tool Config

Ansible 실행과 YAML 검증에 필요한 설정 파일을 모아둡니다.

| 파일 | 목적 |
|------|------|
| `ansible.cfg` | inventory, roles_path, filter_plugins, log_path, SSH 기본값 |
| `yamllint.yml` | YAML lint 규칙 |

`ansible.cfg` 안의 상대 경로는 이 파일이 있는 `ops/config/` 기준으로 작성합니다. 직접 실행할 때는 아래처럼 명시합니다.

```bash
cd ops
ANSIBLE_CONFIG=config/ansible.cfg ansible-playbook -i inventories/dev/hosts.ini playbooks/site.yml --check --diff
```
