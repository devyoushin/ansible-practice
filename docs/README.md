# Ansible Practice Docs

Ansible 학습과 운영 보조 문서는 이 디렉터리에서 관리합니다.

| 폴더 | 내용 |
|------|------|
| `agents/` | Ansible 문서 작성, 플레이북 리뷰, 롤 설계, 보안 감사용 AI 작업 지침 |
| `rules/` | 문서 작성 규칙, Ansible 컨벤션, 보안/모니터링 체크리스트 |
| `templates/` | 서비스 문서, 런북, 장애 보고서 템플릿 |

실제 Ansible 실행 자산은 루트의 `inventories/`, `playbooks/`, `roles/`, `molecule/`, `filter_plugins/`에 둡니다.

## 코드 위치

| 경로 | 내용 |
|------|------|
| `../inventories/` | dev/staging/prod 정적 인벤토리와 AWS 동적 인벤토리 |
| `../playbooks/` | 배포, 롤링 업데이트, 장애 대응, 유지보수 플레이북 |
| `../roles/` | 공통 초기화, 보안, 웹서버, DB, 앱, 모니터링 등 재사용 롤 |
| `../molecule/` | 롤 단위 테스트 |
| `../filter_plugins/` | 커스텀 Jinja2 필터 |
| `../basics/` | Ansible 기초 학습 문서와 예제 |
| `../examples/` | 실습 예제 |

## 작업 기준

- 설명 문서, 규칙, 템플릿은 `docs/` 아래에 둡니다.
- 플레이북과 롤은 기존 역할 경계 안에서 수정합니다.
- `AGENTS.md`는 `CLAUDE.md`를 가리키는 심볼릭 링크입니다. AI 작업 지침은 `CLAUDE.md`를 원본으로 관리합니다.
