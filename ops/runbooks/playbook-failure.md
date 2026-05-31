# Playbook 실패 대응 런북

## 1. 실패 범위 확인

```bash
cd ops
ansible-playbook -i inventories/prod/hosts.ini playbooks/site.yml --check --diff
scripts/list-failed-hosts.sh logs/ansible.log
```

## 2. 호스트 접근성 확인

```bash
ansible all -i inventories/prod/hosts.ini -m ping
ansible all -i inventories/prod/hosts.ini -m setup -a "filter=ansible_distribution*"
```

## 3. 실패 유형별 대응

| 유형 | 확인 항목 |
|------|-----------|
| SSH 접속 실패 | 키, bastion, security group, sudo 권한 |
| 패키지 설치 실패 | repository, lock, proxy, OS 버전 |
| template 검증 실패 | 변수 누락, Jinja2 필터, 서비스 설정 문법 |
| handler 실패 | 서비스 이름, systemd unit, 포트 충돌 |
| Vault 오류 | vault password, 암호화 파일 경로, 변수명 |

## 4. 재실행 기준

- 원인을 수정한 뒤 `--limit`으로 실패 호스트만 먼저 재실행합니다.
- 서비스 영향이 큰 변경은 `--check --diff`를 다시 확인한 뒤 실행합니다.
- 같은 오류가 반복되면 로그와 inventory/group_vars 차이를 함께 확인합니다.
