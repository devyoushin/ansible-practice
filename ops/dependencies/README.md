# Dependencies

Ansible Galaxy 컬렉션과 외부 role 의존성을 관리합니다.

| 파일 | 목적 |
|------|------|
| `requirements.yml` | `amazon.aws`, `community.general`, `community.mysql` 등 컬렉션 의존성 |

설치:

```bash
cd ops
ansible-galaxy install -r dependencies/requirements.yml
```

