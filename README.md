# Ansible Practice — 실전 인프라 자동화

Terraform으로 프로비저닝된 AWS 인프라를 Ansible로 구성 관리하는 실전 예제 프로젝트.

---

## 디렉토리 구조

```
ansible-practice/
├── ansible.cfg                    # Ansible 전역 설정 (vault, forks, callback 등)
├── requirements.yml               # Galaxy 컬렉션/롤 의존성
├── .yamllint                      # YAML 린트 규칙
│
├── inventories/
│   ├── dev/
│   │   ├── hosts.ini              # 정적 인벤토리 (dev)
│   │   └── group_vars/
│   │       ├── all.yml            # 환경 변수
│   │       └── vault.yml          # 암호화 시크릿 (ansible-vault)
│   ├── staging/  (동일 구조)
│   ├── prod/     (동일 구조)
│   └── aws/
│       └── ec2.yml                # AWS 동적 인벤토리 (EC2 태그 기반)
│
├── playbooks/
│   ├── site.yml                   # 전체 오케스트레이션 (메인)
│   ├── database.yml               # DB 단독 배포
│   ├── app.yml                    # 앱 단독 배포
│   ├── monitoring.yml             # 모니터링 배포
│   ├── rolling_update.yml         # 무중단 롤링 업데이트
│   └── maintenance.yml            # 운영 유지보수 (디스크/로그/패키지)
│
├── roles/
│   ├── common/                    # 공통 초기화 (패키지, NTP, sysctl)
│   ├── security/                  # 보안 강화 (SSH, firewalld, auditd)
│   ├── webserver/                 # Nginx 웹서버
│   ├── database/                  # MariaDB (replication, backup)
│   ├── app/                       # Spring Boot 앱 (systemd, health check)
│   ├── haproxy/                   # 로드밸런서
│   └── monitoring/                # Node Exporter + Prometheus
│
├── molecule/
│   └── default/                   # 롤 단위 테스트 (Docker)
│
├── filter_plugins/
│   └── custom_filters.py          # 커스텀 Jinja2 필터
│
└── .github/
    └── workflows/
        ├── ci.yml                 # PR: lint → syntax-check → molecule
        └── deploy.yml             # CD: dev 자동배포, prod 수동승인
```

---

## 환경 구성

| 환경 | 인벤토리 | 웹서버 | 앱서버 | DB | LB | 모니터링 |
|------|----------|--------|--------|-----|-----|----------|
| dev | `inventories/dev` | 2 | 1 | 1 | 1 | 1 |
| staging | `inventories/staging` | 2 | 2 | 1 | 1 | 1 |
| prod | `inventories/prod` | 3 | 3 | 2(+replica) | 2(HA) | 1 |

---

## 빠른 시작

### 1. 의존성 설치

```bash
pip install ansible boto3
ansible-galaxy install -r requirements.yml
```

### 2. Vault 비밀번호 설정

```bash
# vault 비밀번호 파일 생성
echo "your-vault-password" > ~/.vault_pass
chmod 600 ~/.vault_pass

# vault.yml 암호화 (시크릿 파일)
ansible-vault encrypt inventories/dev/group_vars/vault.yml
```

### 3. 전체 배포

```bash
# dev 전체 배포
ansible-playbook -i inventories/dev/hosts.ini playbooks/site.yml

# prod 전체 배포 (vault 자동 복호화)
ansible-playbook -i inventories/prod/hosts.ini playbooks/site.yml
```

---

## 주요 실행 예시

### 태그로 선택 실행

```bash
# 웹서버만 재배포
ansible-playbook -i inventories/dev/hosts.ini playbooks/site.yml --tags webserver

# 보안 설정만 갱신
ansible-playbook -i inventories/prod/hosts.ini playbooks/site.yml --tags security

# 특정 서버만 실행
ansible-playbook -i inventories/prod/hosts.ini playbooks/site.yml --limit prod-web-01
```

### 무중단 롤링 업데이트

```bash
# 앱 v2.1.0 으로 롤링 업데이트 (25%씩 순차)
ansible-playbook -i inventories/prod/hosts.ini playbooks/rolling_update.yml \
  -e "app_version=2.1.0"
```

### 운영 유지보수

```bash
# 디스크 공간 점검
ansible-playbook -i inventories/prod/hosts.ini playbooks/maintenance.yml --tags disk_check

# 오래된 로그 정리
ansible-playbook -i inventories/prod/hosts.ini playbooks/maintenance.yml --tags log_cleanup

# 보안 패키지 업데이트 (webserver만)
ansible-playbook -i inventories/prod/hosts.ini playbooks/maintenance.yml \
  --tags pkg_update --limit webservers
```

### 드라이런 (변경사항 미리 확인)

```bash
# --check: 실제 변경 없이 무엇이 바뀌는지 확인
# --diff: 파일 변경 내용 diff 출력
ansible-playbook -i inventories/prod/hosts.ini playbooks/site.yml --check --diff
```

### AWS 동적 인벤토리

```bash
# EC2 태그 기반 인벤토리 목록 확인
ansible-inventory -i inventories/aws/ec2.yml --graph

# 동적 인벤토리로 배포
ansible-playbook -i inventories/aws/ec2.yml playbooks/site.yml
```

### Ad-hoc 커맨드

```bash
# 전체 서버 디스크 확인
ansible all -i inventories/prod/hosts.ini -m shell -a "df -h"

# 서비스 상태 확인
ansible webservers -i inventories/prod/hosts.ini -m service -a "name=nginx state=started"

# Fact 수집 (서버 정보 조회)
ansible prod-web-01 -i inventories/prod/hosts.ini -m setup -a "filter=ansible_memory_mb"
```

---

## 핵심 개념 가이드

### Ansible Vault (시크릿 관리)

```bash
# 파일 암호화
ansible-vault encrypt inventories/prod/group_vars/vault.yml

# 암호화된 파일 확인/편집
ansible-vault view inventories/prod/group_vars/vault.yml
ansible-vault edit inventories/prod/group_vars/vault.yml

# 단일 값 암호화 (변수 값으로 사용)
ansible-vault encrypt_string 'my-secret-password' --name 'db_password'
```

### 롤 구조

```
roles/database/
├── defaults/main.yml    # 기본값 (우선순위 최하위, 오버라이드 가능)
├── vars/main.yml        # 고정값 (오버라이드 불가)
├── tasks/
│   ├── main.yml         # 진입점 (import_tasks/include_tasks)
│   ├── install.yml
│   └── configure.yml
├── handlers/main.yml    # notify로 호출, 플레이 마지막에 1번만 실행
└── templates/           # Jinja2 템플릿 (.j2)
```

### 변수 우선순위 (낮음 → 높음)

```
role defaults → inventory group_vars → inventory host_vars
→ playbook vars → extra vars (-e)
```

### Molecule 테스트

```bash
pip install molecule molecule-docker

# 특정 롤 테스트
cd roles/common
molecule test         # 전체 (create → converge → verify → destroy)
molecule converge     # 롤 적용만
molecule verify       # 검증만
molecule destroy      # 컨테이너 삭제
```

---

## CI/CD 흐름

```
PR 생성
  → yamllint (YAML 문법)
  → ansible-lint (모범 사례)
  → syntax-check (각 플레이북)
  → molecule test (각 롤)
  → dry-run --check (dev 환경)

main 머지
  → dev 자동 배포
  → staging 배포 (수동 트리거)
  → prod 배포 (수동 승인 필수)
```

---

## Terraform ↔ Ansible 역할 비교

| Terraform | Ansible | 역할 |
|-----------|---------|------|
| `modules/` | `roles/` | 재사용 가능한 컴포넌트 |
| `envs/dev/`, `envs/prod/` | `inventories/dev/`, `inventories/prod/` | 환경별 설정 |
| `terraform.tfvars` | `group_vars/all.yml` | 환경별 변수값 |
| `variables.tf` | `defaults/main.yml` | 변수 정의 및 기본값 |
| `outputs.tf` | `register` + `debug` | 결과값 출력 |
| `provider.tf` + `backend.tf` | `ansible.cfg` | 도구 설정 |
| `main.tf` (envs) | `playbooks/site.yml` | 전체 오케스트레이션 |
| Terraform Cloud / AWS Secrets Manager | Ansible Vault | 시크릿 관리 |

---

## 사전 요구사항

- Ansible >= 2.14
- Python >= 3.8
- 대상 서버에 SSH 키 등록 완료
- 대상 서버에 sudo 권한 보유

## 환경별 네트워크 (terraform-vpc 참고)

| 환경 | VPC CIDR | 용도 |
|------|----------|------|
| dev | 10.20.0.0/16 | 개발 환경 |
| staging | 10.30.0.0/16 | 스테이징 환경 |
| prod | 10.0.0.0/16 | 프로덕션 환경 |
