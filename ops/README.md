# Ansible Ops

Ansible 실행 자산과 운영 보조 자료를 모아둔 디렉터리입니다. 최상위 `README.md`는 학습 로드맵과 전체 구조를 설명하고, 이 문서는 실제 실행과 운영 점검 기준을 다룹니다.

## 구성

| 경로 | 내용 |
|------|------|
| `config/` | Ansible, yamllint 등 도구 설정 |
| `dependencies/` | Galaxy 컬렉션과 롤 의존성 |
| `inventories/` | 접속 대상 정의. dev/staging/prod 정적 인벤토리와 AWS 동적 인벤토리 |
| `playbooks/` | 실행 진입점. 배포, 롤링 업데이트, 장애 대응, 유지보수 플레이북 |
| `roles/` | 구현 단위. 공통 초기화, 보안, 웹서버, DB, 앱, 모니터링 등 재사용 롤 |
| `examples/` | 독립 실행 가능한 실습 예제 |
| `tests/` | Molecule 등 role 검증 자산 |
| `filter_plugins/` | 커스텀 Jinja2 필터 |
| `ci/` | GitHub Actions 등 CI/CD 예시 |
| `scripts/` | 반복 점검용 보조 스크립트 |
| `runtime/` | 로그, dry-run 결과, 임시 파일 등 실행 산출물 |

## 기본 실행 흐름

```bash
cd ops
ansible-galaxy install -r dependencies/requirements.yml
ANSIBLE_CONFIG=config/ansible.cfg ansible-playbook -i inventories/dev/hosts.ini playbooks/site.yml --check --diff
ANSIBLE_CONFIG=config/ansible.cfg ansible-playbook -i inventories/dev/hosts.ini playbooks/site.yml
```

## 운영 테마

| 테마 | 사용하는 경로 | 설명 |
|------|---------------|------|
| 환경 대상 관리 | `inventories/` | dev/staging/prod/aws 대상 서버와 그룹을 정의 |
| 공통 베이스라인 | `playbooks/common.yml`, `roles/common`, `roles/security` | 계정, 패키지, SSH, 방화벽, sysctl 같은 기본 운영 기준 적용 |
| 서비스 구축 | `playbooks/webserver.yml`, `playbooks/app.yml`, `playbooks/database.yml`, `roles/` | Nginx, Tomcat, Redis, DB, 앱 서버를 role 단위로 구축 |
| 전체 배포 | `playbooks/site.yml` | 환경별 전체 구성을 한 번에 적용하는 표준 진입점 |
| 배포 전략 | `playbooks/rolling_update.yml`, `playbooks/blue_green_deploy.yml` | 무중단 배포, 단계적 전환, 빠른 롤백 절차 |
| 운영 유지보수 | `playbooks/maintenance.yml`, `playbooks/os_upgrade.yml` | 로그 정리, 패키지 업데이트, OS 업그레이드 |
| 장애 대응 | `playbooks/incident_response.yml`, `scripts/list-failed-hosts.sh` | 장애 진단, 자동 복구, 실패 로그 추출 |
| 검증과 품질 | `scripts/`, `tests/`, `ci/` | syntax-check, dry-run, Molecule, CI 예시 |
| 실행 산출물 | `runtime/` | 로그, dry-run 결과, 임시 파일 보관 |

## 운영 기준

- prod 실행 전에는 `../docs/checklists/pre-deploy.md`를 먼저 확인합니다.
- 롤 변경은 `../docs/checklists/role-review.md` 기준으로 리뷰합니다.
- 실패한 배포는 `../docs/runbooks/playbook-failure.md` 흐름으로 원인을 분리합니다.
- Vault 비밀번호나 시크릿 교체는 `../docs/runbooks/vault-rotation.md`를 사용합니다.
- dry-run 결과, 장애 대응 로그, 변경 전후 비교 자료는 `runtime/outputs/` 아래에 날짜별로 저장합니다.

## 보조 스크립트

```bash
# 기본 site.yml 문법 검사
ops/scripts/syntax-check.sh

# dev/prod 드라이런
ops/scripts/dry-run.sh dev site.yml
ops/scripts/dry-run.sh prod site.yml

# Ansible 로그에서 실패 라인 추출
ops/scripts/list-failed-hosts.sh ops/runtime/logs/ansible.log
```
