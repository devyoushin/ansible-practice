# Ansible Docs

이 디렉터리는 Ansible 학습 문서와 운영 절차를 함께 관리합니다.

## 어디서 시작할까

| 순서 | 문서 | 내용 |
|------|------|------|
| 1 | `getting-started.md` | 어디서부터 읽고 무엇을 실행할지 |
| 2 | `service-build-guide.md` | 서비스를 어떻게 분해해 구축할지 볼 때 |
| 3 | `basics/README.md` | Ansible 개념을 처음 익힐 때 |
| 4 | `examples/README.md` | 짧은 예제로 실습할 때 |
| 5 | `checklists/pre-deploy.md` | 배포 전 점검 |
| 6 | `runbooks/playbook-failure.md` | 실패 대응 |
| 7 | `rules/doc-writing.md` | 문서 작성 규칙 |
| 8 | `../ops/README.md` | 실제 실행 자산과 운영 방법 |

## 구성

| 폴더 | 내용 |
|------|------|
| `agents/` | Ansible 문서 작성, 플레이북 리뷰, 롤 설계, 보안 감사용 AI 작업 지침 |
| `basics/` | Ansible 기초 학습 문서와 짧은 예제 |
| `checklists/` | 배포 전 점검과 롤 리뷰 기준 |
| `examples/` | `ops/examples/` 실행 예제 설명 |
| `service-build-guide.md` | 서비스별 구축 패턴과 롤 분해 기준 |
| `runbooks/` | 플레이북 실패 대응, Vault 회전 운영 절차 |
| `rules/` | 문서 작성 규칙, Ansible 컨벤션, 보안/모니터링 체크리스트 |
| `templates/` | 서비스 문서, 런북, 장애 보고서 템플릿 |

## 코드 위치

| 경로 | 내용 |
|------|------|
| `../ops/inventories/` | dev/staging/prod 정적 인벤토리와 AWS 동적 인벤토리 |
| `../ops/playbooks/` | 배포, 롤링 업데이트, 장애 대응, 유지보수 플레이북 |
| `../ops/roles/` | 공통 초기화, 보안, 웹서버, DB, 앱, 모니터링 등 재사용 롤 |
| `../ops/molecule/` | 롤 단위 테스트 |
| `../ops/filter_plugins/` | 커스텀 Jinja2 필터 |
| `../ops/examples/` | 실습 예제 코드 |
| `../ops/scripts/` | 반복 점검용 보조 스크립트 |
| `../ops/outputs/` | dry-run, 점검 결과, 장애 대응 로그 보관 위치 |

## 작업 기준

- 처음에는 `getting-started.md`를 읽고, 그 다음 `basics/README.md`로 넘어갑니다.
- 실제 배포는 `ops/README.md`의 절차를 따릅니다.
- 설명 문서, 규칙, 템플릿은 `docs/` 아래에 둡니다.
- 플레이북과 롤은 `ops/` 아래의 기존 역할 경계 안에서 수정합니다.
- `AGENTS.md`는 `CLAUDE.md`를 가리키는 심볼릭 링크입니다. AI 작업 지침은 `CLAUDE.md`를 원본으로 관리합니다.
