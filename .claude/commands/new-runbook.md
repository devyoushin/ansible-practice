새 Ansible 운영 런북을 생성합니다.

**사용법**: `/new-runbook <작업명>`

**예시**: `/new-runbook MariaDB 페일오버`

다음 단계를 수행하세요:

1. `templates/runbook.md`를 읽어 템플릿 구조를 확인하세요.
2. 작업 유형을 분류하세요:
   - `배포`: 롤링/블루그린/카나리 배포
   - `유지보수`: 패키지 업데이트, 로그 정리
   - `긴급 대응`: 장애 자동 대응 (`incident_response.yml`)
   - `마이그레이션`: 데이터 이전 (`data_migration.yml`)
3. `playbooks/<작업명>_runbook.md`를 생성하세요:
   - 사전 체크리스트 (Vault 비밀번호, 인벤토리 확인)
   - 환경 변수 및 Vault 설정
   - 단계별 `ansible-playbook` 명령어 (--check 드라이런 포함)
   - 태그(`--tags`) 활용 부분 실행 방법
   - serial/throttle 설정 주의사항
   - 롤백 절차
   - 성공 확인 명령어
