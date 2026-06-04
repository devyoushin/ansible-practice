# Ansible Ops

Ansible 실행 자산과 운영 보조 자료를 모아둔 디렉터리입니다. 최상위 `README.md`는 학습 로드맵과 전체 구조를 설명하고, 이 문서는 실제 실행과 운영 점검 기준을 다룹니다.

## 구성

| 경로 | 내용 |
|------|------|
| `ansible.cfg` | inventory, roles_path, log_path 등 Ansible 기본 설정 |
| `requirements.yml` | Galaxy 컬렉션과 롤 의존성 |
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
ansible-galaxy install -r requirements.yml
ansible-playbook -i inventories/dev/hosts.ini playbooks/site.yml --check --diff
ansible-playbook -i inventories/dev/hosts.ini playbooks/site.yml
```

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
