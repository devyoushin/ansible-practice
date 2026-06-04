# CLAUDE.md — ansible-practice 프로젝트 가이드

Terraform으로 프로비저닝된 AWS 인프라를 Ansible로 구성 관리하는 실전 예제 프로젝트.

---

## 디렉토리 구조

```
ansible-practice/
├── CLAUDE.md                  # 이 파일 (자동 로드)
├── AGENTS.md -> CLAUDE.md     # Codex 작업 지침 링크
├── docs/
│   ├── README.md              # 문서 보조 자료 안내
│   ├── agents/                # 전문 에이전트 정의
│   │   ├── doc-writer.md      # Ansible 문서 작성 전문가
│   │   ├── playbook-reviewer.md
│   │   ├── security-auditor.md
│   │   └── role-designer.md
│   ├── basics/                # Ansible 기초 학습 문서
│   ├── checklists/            # 배포 전 점검, 롤 리뷰 기준
│   ├── examples/              # ops/examples 실행 예제 설명
│   ├── runbooks/              # 실패 대응, Vault 회전 등 운영 절차
│   ├── templates/             # 문서 템플릿
│   │   ├── service-doc.md
│   │   ├── runbook.md
│   │   └── incident-report.md
│   └── rules/                 # Claude 작성 규칙
│       ├── doc-writing.md
│       ├── ansible-conventions.md
│       ├── security-checklist.md
│       └── monitoring.md
└── ops/                       # 실제 Ansible 실행 자산
    ├── ansible.cfg            # Ansible 전역 설정
    ├── requirements.yml       # Galaxy 컬렉션 의존성
    ├── inventories/           # dev/staging/prod/aws 인벤토리
    ├── playbooks/             # 배포, 운영, 장애 대응 플레이북
    ├── roles/                 # 재사용 가능한 롤
    ├── tests/molecule/        # Molecule 등 롤 단위 테스트
    ├── scripts/               # 반복 점검용 보조 스크립트
    ├── runtime/               # 로그, dry-run 결과, 임시 파일
    ├── ci/                    # GitHub Actions 워크플로 예시
    └── filter_plugins/        # 커스텀 Jinja2 필터
```

AI 작업 지침은 `CLAUDE.md`를 원본으로 관리하고, `AGENTS.md`는 심볼릭 링크로만 유지합니다.

---

## 운영 보조 자료

`ops/README.md`를 운영 실행 가이드의 기준 문서로 사용합니다.

| 경로 | 용도 |
|------|------|
| `ops/scripts/` | syntax-check, dry-run, 실패 로그 추출 보조 스크립트 |
| `ops/runtime/` | 로그, dry-run 결과, 임시 파일 등 실행 산출물 |
| `docs/checklists/` | 배포 전 점검과 롤 리뷰 체크리스트 |
| `docs/runbooks/` | 플레이북 실패 대응, Vault 회전 런북 |
| `docs/rules/` | 문서와 Ansible 코드 작성 규칙 |
| `docs/agents/` | 문서 작성, 롤 설계, 보안 감사용 작업 지침 |
| `docs/templates/` | 서비스 문서와 런북 템플릿 |

## 문서 시작 순서

1. `docs/getting-started.md`
2. `docs/service-build-guide.md`
3. `docs/basics/README.md`
4. `docs/examples/README.md`
5. `docs/checklists/pre-deploy.md`
6. `docs/runbooks/playbook-failure.md`
7. `docs/rules/README.md`
8. `docs/agents/README.md`

---

## 커스텀 슬래시 명령어

| 명령어 | 설명 | 사용 예시 |
|--------|------|---------|
| `/new-doc` | 새 롤/플레이북 문서 생성 | `/new-doc ops/roles/kafka` |
| `/new-runbook` | 새 운영 런북 생성 | `/new-runbook MariaDB 페일오버` |
| `/review-doc` | 롤/플레이북 검토 | `/review-doc ops/roles/database` |
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
ansible-playbook -i ops/inventories/prod/hosts.ini ops/playbooks/site.yml \
  --check --diff --ask-vault-pass

# 전체 배포
ansible-playbook -i ops/inventories/prod/hosts.ini ops/playbooks/site.yml \
  --ask-vault-pass

# 롤링 업데이트 (v2.1.0)
ansible-playbook -i ops/inventories/prod/hosts.ini ops/playbooks/rolling_update.yml \
  -e "app_version=2.1.0" --ask-vault-pass

# 장애 대응 (디스크 풀만)
ansible-playbook -i ops/inventories/prod/hosts.ini ops/playbooks/incident_response.yml \
  --tags disk_full

# 유지보수 (로그 정리)
ansible-playbook -i ops/inventories/prod/hosts.ini ops/playbooks/maintenance.yml \
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
