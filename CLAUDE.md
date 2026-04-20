# CLAUDE.md — ansible-practice 프로젝트 가이드

Terraform으로 프로비저닝된 AWS 인프라를 Ansible로 구성 관리하는 실전 예제 프로젝트.

---

## 디렉토리 구조

```
ansible-practice/
├── CLAUDE.md                  # 이 파일 (자동 로드)
├── .claude/
│   ├── settings.json          # 권한 설정 (prod 실행 차단) + PostToolUse 훅
│   └── commands/              # 커스텀 슬래시 명령어
│       ├── new-doc.md         # /new-doc — 새 롤/플레이북 문서 생성
│       ├── new-runbook.md     # /new-runbook — 새 운영 런북 생성
│       ├── review-doc.md      # /review-doc — 롤/플레이북 검토
│       ├── add-troubleshooting.md  # /add-troubleshooting — 트러블슈팅 추가
│       └── search-kb.md       # /search-kb — 지식베이스 검색
├── agents/                    # 전문 에이전트 정의
│   ├── doc-writer.md          # Ansible 문서 작성 전문가
│   ├── playbook-reviewer.md   # 플레이북 코드 리뷰 전문가
│   ├── security-auditor.md    # 보안 감사 전문가
│   └── role-designer.md       # 롤 설계 전문가
├── templates/                 # 문서 템플릿
│   ├── service-doc.md         # 롤 README 템플릿
│   ├── runbook.md             # 운영 런북 템플릿
│   └── incident-report.md     # 장애 분석 보고서 템플릿
├── rules/                     # Claude 작성 규칙
│   ├── doc-writing.md         # 문서 작성 원칙
│   ├── ansible-conventions.md # Ansible 코드 표준
│   ├── security-checklist.md  # 보안 체크리스트
│   └── monitoring.md          # 모니터링 지침
├── ansible.cfg                # Ansible 전역 설정
├── requirements.yml           # Galaxy 컬렉션 의존성
├── inventories/
│   ├── dev/                   # dev 환경 인벤토리 + group_vars
│   ├── staging/               # staging 환경
│   ├── prod/                  # prod 환경 (HA 구성)
│   └── aws/ec2.yml            # AWS 동적 인벤토리 (EC2 태그 기반)
├── playbooks/                 # 플레이북
│   ├── site.yml               # 전체 오케스트레이션 (메인 진입점)
│   ├── rolling_update.yml     # 무중단 롤링 업데이트 (25% serial)
│   ├── blue_green_deploy.yml  # Blue-Green 배포
│   ├── os_upgrade.yml         # RHEL/Rocky OS 버전 업그레이드
│   ├── maintenance.yml        # 운영 유지보수
│   ├── incident_response.yml  # 장애 자동 대응
│   └── data_migration.yml     # 대용량 데이터 마이그레이션
├── roles/                     # 롤
│   ├── common/                # 공통 초기화 (패키지, NTP, sysctl, ulimit)
│   ├── security/              # 보안 강화 (SSH, firewalld, auditd)
│   ├── webserver/             # Nginx
│   ├── ssl/                   # TLS 인증서
│   ├── database/              # MariaDB
│   ├── app/                   # Spring Boot
│   ├── haproxy/               # HAProxy 로드밸런서
│   ├── monitoring/            # Node Exporter + Prometheus
│   ├── redis/                 # Redis 7 + Sentinel
│   ├── tomcat/                # WAR 배포용 Tomcat
│   ├── os_upgrade/            # RHEL/Rocky OS 업그레이드
│   └── data_migration/        # 대용량 데이터 이전
├── molecule/default/          # 롤 단위 테스트 (Docker)
└── filter_plugins/            # 커스텀 Jinja2 필터
```

---

## 커스텀 슬래시 명령어

| 명령어 | 설명 | 사용 예시 |
|--------|------|---------|
| `/new-doc` | 새 롤/플레이북 문서 생성 | `/new-doc roles/kafka` |
| `/new-runbook` | 새 운영 런북 생성 | `/new-runbook MariaDB 페일오버` |
| `/review-doc` | 롤/플레이북 검토 | `/review-doc roles/database` |
| `/add-troubleshooting` | 트러블슈팅 케이스 추가 | `/add-troubleshooting 복제 지연` |
| `/search-kb` | 지식베이스 검색 | `/search-kb 롤링 업데이트 serial` |

---

## 환경 구성

| 환경 | 웹서버 | 앱서버 | DB | LB | 모니터링 |
|------|--------|--------|-----|-----|----------|
| dev | 2 | 1 | 1 | 1 | 1 |
| staging | 2 | 2 | 1 | 1 | 1 |
| prod | 3 | 3 | 2(+replica) | 2(HA) | 1 |

---

## 주요 롤 요약

| 롤 | 핵심 기능 |
|----|-----------|
| `common` | 패키지, NTP(chrony), sysctl, ulimit |
| `security` | SSH 강화, firewalld, auditd, 불필요 서비스 비활성화 |
| `webserver` | Nginx 가상호스트, gzip, health check, log rotation |
| `ssl` | Let's Encrypt certbot, 자체 서명 인증서, OCSP Stapling, HSTS |
| `database` | MariaDB 설치·복제·백업·성능 튜닝 |
| `app` | Spring Boot JAR 배포, systemd, actuator health check |
| `haproxy` | 로드밸런싱, stats, drain/enable 소켓 제어 |
| `monitoring` | Node Exporter, Prometheus, Alert Rules |
| `redis` | Redis 7, maxmemory-policy, Sentinel (HA), 보안 강화 |
| `tomcat` | WAR 배포용 독립 Tomcat, systemd, 버전 심볼릭링크 관리 |
| `os_upgrade` | RHEL leapp / Rocky dnf system-upgrade |
| `data_migration` | rsync/tar_stream/parallel/db_dump, 체크섬 검증 |

---

## 주요 플레이북 실행 예시

```bash
# 드라이런 (필수 — prod 실행 전)
ansible-playbook -i inventories/prod/hosts.ini playbooks/site.yml \
  --check --diff --ask-vault-pass

# 전체 배포
ansible-playbook -i inventories/prod/hosts.ini playbooks/site.yml \
  --ask-vault-pass

# 롤링 업데이트 (v2.1.0)
ansible-playbook -i inventories/prod/hosts.ini playbooks/rolling_update.yml \
  -e "app_version=2.1.0" --ask-vault-pass

# 장애 대응 (디스크 풀만)
ansible-playbook -i inventories/prod/hosts.ini playbooks/incident_response.yml \
  --tags disk_full

# 유지보수 (로그 정리)
ansible-playbook -i inventories/prod/hosts.ini playbooks/maintenance.yml \
  --tags log_cleanup
```

---

## Vault 시크릿 목록

| 변수 | 용도 |
|------|------|
| `vault_db_root_password` | MariaDB root 비밀번호 |
| `vault_db_app_password` | 앱용 DB 계정 |
| `vault_db_replication_password` | 복제 계정 |
| `vault_redis_password` | Redis 인증 비밀번호 |
| `vault_haproxy_stats_password` | HAProxy stats 페이지 |
| `vault_slack_webhook_url` | 알림용 Slack Webhook |

---

## 커스텀 Jinja2 필터

| 필터 | 용도 |
|------|------|
| `parse_memory_mb` | "512m" → 512 |
| `to_haproxy_backend` | HAProxy backend 라인 생성 |
| `days_since` | 날짜로부터 경과일 |
| `mask_secret` | 로그에서 비밀번호 마스킹 |
| `to_yaml_list` | 리스트 → YAML 형식 |
| `filter_by_env` | 환경별 아이템 필터링 |
| `sizeof_fmt` | 바이트 → 사람이 읽기 쉬운 단위 |
