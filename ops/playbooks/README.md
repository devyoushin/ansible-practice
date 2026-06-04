# Playbooks

실제 실행 진입점입니다. 서비스 배포, 운영 작업, 장애 대응, 검증 목적별로 플레이북을 분리합니다.

| 구분 | 파일 | 목적 |
|------|------|------|
| 전체 배포 | `site.yml` | 공통, 보안, 웹, 앱, DB, 모니터링 전체 구성 |
| 서비스 단위 | `webserver.yml`, `app.yml`, `database.yml`, `monitoring.yml` | 역할별 단독 실행 |
| 배포 전략 | `rolling_update.yml`, `blue_green_deploy.yml` | 무중단/롤백 가능한 배포 |
| 운영 작업 | `maintenance.yml`, `os_upgrade.yml` | 유지보수와 OS 업그레이드 |
| 장애 대응 | `incident_response.yml` | 장애 진단과 복구 |
| 데이터 작업 | `data_migration.yml`, `data_migration_verify.yml`, `data_migration_examples.yml` | 데이터 이관과 검증 |

운영 실행 전에는 `../scripts/syntax-check.sh`와 `../scripts/dry-run.sh`로 먼저 검증합니다.

