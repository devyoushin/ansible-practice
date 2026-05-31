# Ansible 배포 전 체크리스트

## 공통

- 대상 inventory가 올바른 환경을 가리키는가?
- `ansible-playbook --syntax-check`가 통과했는가?
- prod 변경 전 `--check --diff` 결과를 확인했는가?
- `--limit`, `--tags`, `--skip-tags`가 의도한 범위로 설정되었는가?
- 필요한 Vault 비밀번호 또는 시크릿 접근 권한이 준비되었는가?

## prod 추가 확인

- 롤링 업데이트의 `serial`, drain, health check 조건이 맞는가?
- DB, Redis, HAProxy, SSL 변경은 롤백 절차가 준비되었는가?
- 변경 대상 호스트의 백업 또는 스냅샷이 확보되었는가?
- 배포 창과 알림 채널이 준비되었는가?
- dry-run 결과를 `ops/outputs/` 아래에 보관했는가?
