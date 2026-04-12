# CLAUDE.md — Ansible Practice 프로젝트 개요

Terraform으로 프로비저닝된 AWS 인프라를 Ansible로 구성 관리하는 실전 예제 프로젝트.

---

## 프로젝트 구조

```
ansible-practice/
├── ansible.cfg                    # Ansible 전역 설정 (vault, forks, callback)
├── requirements.yml               # Galaxy 컬렉션 의존성
├── .yamllint                      # YAML 린트 규칙
│
├── inventories/
│   ├── dev/                       # dev 환경 인벤토리 + group_vars
│   ├── staging/                   # staging 환경
│   ├── prod/                      # prod 환경 (HA 구성)
│   └── aws/ec2.yml                # AWS 동적 인벤토리 (EC2 태그 기반)
│
├── playbooks/
│   ├── site.yml                   # 전체 오케스트레이션 (메인 진입점)
│   ├── rolling_update.yml         # 무중단 롤링 업데이트 (25% serial)
│   ├── blue_green_deploy.yml      # Blue-Green 배포 (즉시 롤백 가능)
│   ├── os_upgrade.yml             # RHEL/Rocky OS 버전 업그레이드 (serial: 1)
│   ├── maintenance.yml            # 운영 유지보수 (디스크/로그/패키지)
│   ├── incident_response.yml      # 장애 자동 대응 (디스크/서비스/메모리)
│   ├── data_migration.yml         # 대용량 데이터 마이그레이션
│   ├── data_migration_examples.yml
│   ├── data_migration_verify.yml
│   ├── database.yml               # DB 단독 배포
│   ├── app.yml                    # 앱 단독 배포
│   ├── monitoring.yml             # 모니터링 배포
│   ├── webserver.yml              # 웹서버 단독 배포
│   └── common.yml                 # 공통 초기화 단독 실행
│
├── roles/
│   ├── common/                    # 공통 초기화 (패키지, NTP, sysctl, ulimit)
│   ├── security/                  # 보안 강화 (SSH, firewalld, auditd)
│   ├── webserver/                 # Nginx (가상 호스트, log rotation, health check)
│   ├── ssl/                       # TLS 인증서 (Let's Encrypt / 자체 서명)
│   ├── database/                  # MariaDB (replication, backup, 성능 튜닝)
│   ├── app/                       # Spring Boot (systemd, health check, JVM 옵션)
│   ├── haproxy/                   # HAProxy 로드밸런서 (stats, health check)
│   ├── monitoring/                # Node Exporter + Prometheus (alert rules)
│   ├── redis/                     # Redis 7 + Sentinel (HA, maxmemory, 보안)
│   ├── os_upgrade/                # RHEL/Rocky OS 버전 업그레이드 (leapp/dnf)
│   └── data_migration/            # 대용량 데이터 이전 (rsync/tar/parallel/db_dump)
│
├── molecule/default/              # 롤 단위 테스트 (Docker)
├── filter_plugins/custom_filters.py  # 커스텀 Jinja2 필터 7종
└── .github/workflows/
    ├── ci.yml                     # PR: lint → syntax-check → molecule
    └── deploy.yml                 # CD: dev 자동배포, prod 수동승인
```

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
| `os_upgrade` | RHEL leapp / Rocky dnf system-upgrade, 사전점검, 백업, 사후검증 |
| `data_migration` | rsync/tar_stream/parallel/db_dump, 체크섬 검증 |

---

## 주요 플레이북 실행 예시

```bash
# 전체 배포
ansible-playbook -i inventories/prod/hosts.ini playbooks/site.yml

# 롤링 업데이트 (v2.1.0)
ansible-playbook -i inventories/prod/hosts.ini playbooks/rolling_update.yml \
  -e "app_version=2.1.0"

# Blue-Green 배포 (즉시 롤백 가능)
ansible-playbook -i inventories/prod/hosts.ini playbooks/blue_green_deploy.yml \
  -e "app_version=2.1.0"

# Blue로 즉시 롤백
ansible-playbook -i inventories/prod/hosts.ini playbooks/blue_green_deploy.yml \
  -e "app_version=2.0.0 rollback=true"

# 장애 대응 (전체 진단)
ansible-playbook -i inventories/prod/hosts.ini playbooks/incident_response.yml

# 디스크 꽉 참만 대응
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

## 커스텀 Jinja2 필터 (filter_plugins/custom_filters.py)

| 필터 | 용도 | 예시 |
|------|------|------|
| `parse_memory_mb` | "512m" → 512 | `{{ "2g" \| parse_memory_mb }}` → 2048 |
| `to_haproxy_backend` | HAProxy backend 라인 생성 | |
| `days_since` | 날짜로부터 경과일 | |
| `mask_secret` | 로그에서 비밀번호 마스킹 | |
| `to_yaml_list` | 리스트 → YAML 형식 | |
| `filter_by_env` | 환경별 아이템 필터링 | |
| `sizeof_fmt` | 바이트 → 사람이 읽기 쉬운 단위 | |
