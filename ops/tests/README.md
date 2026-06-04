# Tests

Ansible role 검증 자산을 보관합니다.

| 경로 | 목적 |
|------|------|
| `molecule/default/` | Molecule 기본 시나리오 |

실행 예시:

```bash
cd ops/tests
ANSIBLE_ROLES_PATH=../roles molecule test -s default
```

role별 시나리오가 필요하면 `tests/molecule/<role-name>/` 형태로 추가합니다.
