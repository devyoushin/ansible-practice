# ansible-practice

Terraform 프로젝트(terraform-ec2, terraform-eks, terraform-tgw)의 구조를 참고하여 구성한 Ansible 연습 프로젝트입니다.

## 디렉토리 구조

```
ansible-practice/
├── ansible.cfg                          # Ansible 기본 설정 (terraform의 provider + backend 역할)
├── inventories/                         # 환경별 인벤토리 (terraform의 envs/ 역할)
│   ├── dev/
│   │   ├── hosts.ini                    # 호스트 목록 (terraform.tfvars 역할)
│   │   └── group_vars/
│   │       └── all.yml                  # 환경 변수 (variables.tf 역할)
│   ├── staging/
│   │   ├── hosts.ini
│   │   └── group_vars/
│   │       └── all.yml
│   └── prod/
│       ├── hosts.ini
│       └── group_vars/
│           └── all.yml
├── roles/                               # 재사용 가능한 롤 (terraform의 modules/ 역할)
│   ├── common/                          # 공통 서버 초기화
│   │   ├── tasks/main.yml
│   │   ├── handlers/main.yml
│   │   ├── defaults/main.yml            # 기본 변수 (variables.tf 역할)
│   │   └── templates/
│   ├── security/                        # 보안 강화 (terraform EC2 Security Group 역할)
│   │   ├── tasks/main.yml
│   │   ├── handlers/main.yml
│   │   ├── defaults/main.yml
│   │   └── templates/
│   └── webserver/                       # Nginx 웹서버
│       ├── tasks/main.yml
│       ├── handlers/main.yml
│       ├── defaults/main.yml
│       └── templates/
└── playbooks/                           # 플레이북 (terraform의 main.tf 오케스트레이션 역할)
    ├── site.yml                         # 전체 실행 (envs/prod/main.tf 역할)
    ├── common.yml                       # 공통 설정만 실행
    └── webserver.yml                    # 웹서버만 실행
```

## Terraform ↔ Ansible 구조 대응표

| Terraform | Ansible | 역할 |
|-----------|---------|------|
| `modules/` | `roles/` | 재사용 가능한 컴포넌트 |
| `envs/dev/`, `envs/prod/` | `inventories/dev/`, `inventories/prod/` | 환경별 설정 |
| `terraform.tfvars` | `group_vars/all.yml` | 환경별 변수값 |
| `variables.tf` | `defaults/main.yml` | 변수 정의 및 기본값 |
| `outputs.tf` | `register` + `debug` | 결과값 출력 |
| `provider.tf` + `backend.tf` | `ansible.cfg` | 도구 설정 |
| `main.tf` (envs) | `playbooks/site.yml` | 전체 오케스트레이션 |

## 실행 방법

```bash
# 개발 환경 전체 배포
ansible-playbook -i inventories/dev/hosts.ini playbooks/site.yml

# 스테이징 환경 전체 배포
ansible-playbook -i inventories/staging/hosts.ini playbooks/site.yml

# 프로덕션 환경 전체 배포 (dry-run 먼저)
ansible-playbook -i inventories/prod/hosts.ini playbooks/site.yml --check
ansible-playbook -i inventories/prod/hosts.ini playbooks/site.yml

# 웹서버만 배포
ansible-playbook -i inventories/dev/hosts.ini playbooks/webserver.yml

# 특정 태그만 실행
ansible-playbook -i inventories/dev/hosts.ini playbooks/site.yml --tags "security"

# 특정 호스트만 실행
ansible-playbook -i inventories/dev/hosts.ini playbooks/site.yml --limit "webservers"

# 변수 확인 (dry-run)
ansible-playbook -i inventories/dev/hosts.ini playbooks/site.yml --check --diff
```

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
