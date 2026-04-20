ansible-practice 지식베이스에서 관련 내용을 검색합니다.

**사용법**: `/search-kb <검색어>`

**예시**: `/search-kb 롤링 업데이트 serial`

다음 단계를 수행하세요:

1. 검색어와 관련된 롤/플레이북을 파악하세요:
   - **롤**: common, security, webserver, ssl, database, app, haproxy, monitoring, redis, tomcat, os_upgrade, data_migration
   - **플레이북**: site.yml, rolling_update.yml, blue_green_deploy.yml, os_upgrade.yml, maintenance.yml, incident_response.yml, data_migration.yml

2. 관련 파일들을 읽어 답변을 구성하세요:
   - `roles/<이름>/tasks/main.yml` — 태스크 로직
   - `roles/<이름>/defaults/main.yml` — 기본 변수
   - `playbooks/<이름>.yml` — 플레이북 구조

3. 결과를 다음 형식으로 제시하세요:
   - **관련 파일**: 경로 목록
   - **핵심 내용**: 검색어와 관련된 설명
   - **예시 명령어**: `ansible-playbook` 실행 예시
   - **주의사항**: 알려진 이슈 또는 환경별 차이
