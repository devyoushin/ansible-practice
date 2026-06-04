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
| 7 | `rules/README.md` | 문서와 Ansible 코드 규칙 |
| 8 | `agents/README.md` | Claude/Codex 작업 지침 |
| 9 | `../ops/README.md` | 실제 실행 자산과 운영 방법 |

## 문서 구조

이 저장소의 문서는 아래 4가지 성격으로 나뉩니다.

| 구분 | 위치 | 의미 |
|------|------|------|
| 학습 문서 | `basics/`, `service-build-guide.md`, `examples/` | Ansible을 이해하고 실습하는 문서 |
| 운영 문서 | `checklists/`, `runbooks/`, `templates/` | 배포 전 점검, 장애 대응, 문서 골격 |
| 규칙 문서 | `rules/` | 문서와 Ansible 코드 작성 기준 |
| AI 지침 | `agents/` | Claude/Codex가 참고하는 작업 지침 |

## 폴더 안내

| 폴더 | 내용 |
|------|------|
| `agents/` | AI 작업 지침. 각 에이전트의 역할과 사용 기준 |
| `basics/` | Ansible 기초 학습 문서와 짧은 예제 |
| `checklists/` | 배포 전 점검과 롤 리뷰 기준 |
| `examples/` | `ops/examples/` 실행 예제 설명 |
| `service-build-guide.md` | 서비스별 구축 패턴과 롤 분해 기준 |
| `runbooks/` | 플레이북 실패 대응, Vault 회전 운영 절차 |
| `rules/` | 문서 작성 규칙과 Ansible 컨벤션 |
| `templates/` | 서비스 문서, 런북, 장애 보고서 템플릿 |

## 문서 읽는 순서

처음 보는 경우에는 아래 순서가 가장 덜 흔들립니다.

1. `getting-started.md`
2. `service-build-guide.md`
3. `basics/README.md`
4. `examples/README.md`
5. `checklists/pre-deploy.md`
6. `runbooks/playbook-failure.md`
7. `rules/README.md`
8. `agents/README.md`
9. `../ops/README.md`

## 코드 위치

| 경로 | 내용 |
|------|------|
| `../ops/inventories/` | dev/staging/prod 정적 인벤토리와 AWS 동적 인벤토리 |
| `../ops/playbooks/` | 배포, 롤링 업데이트, 장애 대응, 유지보수 플레이북 |
| `../ops/roles/` | 공통 초기화, 보안, 웹서버, DB, 앱, 모니터링 등 재사용 롤 |
| `../ops/tests/` | Molecule 등 롤 단위 테스트 |
| `../ops/filter_plugins/` | 커스텀 Jinja2 필터 |
| `../ops/examples/` | 실습 예제 코드 |
| `../ops/scripts/` | 반복 점검용 보조 스크립트 |
| `../ops/runtime/` | 로그, dry-run 결과, 임시 파일 등 실행 산출물 |

## 작업 기준

- 처음에는 `getting-started.md`를 읽고, 작업 유형에 따라 `service-build-guide.md`, `basics/README.md`, `examples/README.md`로 이동합니다.
- 규칙은 `rules/README.md`, AI 지침은 `agents/README.md`에서 확인합니다.
- 실제 배포는 `ops/README.md`의 절차를 따릅니다.
- 설명 문서, 규칙, 템플릿은 `docs/` 아래에 둡니다.
- 플레이북과 롤은 `ops/` 아래의 기존 역할 경계 안에서 수정합니다.
- `AGENTS.md`는 `CLAUDE.md`를 가리키는 심볼릭 링크입니다. AI 작업 지침은 `CLAUDE.md`를 원본으로 관리합니다.
