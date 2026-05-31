# Ansible Outputs

이 디렉터리는 실행 산출물을 임시 또는 날짜별로 보관하는 위치입니다.

보관 예시:

- `YYYYMMDD/dev-dry-run.txt`
- `YYYYMMDD/prod-dry-run.txt`
- `YYYYMMDD/failed-hosts.txt`
- `YYYYMMDD/incident-response.log`

Vault 값, 호스트 접속 정보, 민감한 로그는 커밋하지 않습니다.
