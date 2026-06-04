# Roles

재사용 가능한 구성 관리 단위입니다. 플레이북은 여기의 role을 조합해서 서비스나 운영 작업을 수행합니다.

| Role | 목적 |
|------|------|
| `common` | 공통 패키지, 계정, 기본 설정 |
| `security` | SSH, 방화벽, 보안 기준 |
| `webserver` | Nginx/웹서버 구성 |
| `haproxy` | L4/L7 로드밸런서 구성 |
| `tomcat` | Tomcat 애플리케이션 서버 구성 |
| `app` | 애플리케이션 배포 |
| `database` | 데이터베이스 서버 구성 |
| `redis` | Redis 캐시/Sentinel 구성 |
| `monitoring` | 모니터링 에이전트/Exporter 구성 |
| `ssl` | 인증서 발급과 배포 |
| `os_upgrade` | OS 패키지 업데이트와 재부팅 흐름 |
| `data_migration` | 데이터 이관과 검증 |

role 변경 시 `../../docs/checklists/role-review.md`를 기준으로 변수, idempotency, handler, 보안 값을 확인합니다.

