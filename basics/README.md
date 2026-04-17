# Ansible 기초 학습 가이드

> 처음 접하는 분도 이해할 수 있게 최대한 쉽게 작성했습니다.

---

## 학습 순서

| 순서 | 파일 | 내용 | 난이도 |
|------|------|------|--------|
| 1 | [01_what_is_ansible.md](01_what_is_ansible.md) | Ansible이 뭔지, 왜 쓰는지 | ★☆☆ |
| 2 | [02_inventory.md](02_inventory.md) | 어느 서버에 실행할지 | ★☆☆ |
| 3 | [03_playbook_basics.md](03_playbook_basics.md) | 플레이북 구조 이해 | ★★☆ |
| 4 | [04_variables.md](04_variables.md) | 변수 선언 및 사용법 | ★★☆ |
| 5 | [05_conditionals_loops.md](05_conditionals_loops.md) | when / loop | ★★☆ |
| 6 | [06_handlers.md](06_handlers.md) | 변경 시에만 실행 | ★★☆ |
| 7 | [07_roles.md](07_roles.md) | 재사용 가능한 묶음 | ★★★ |
| 8 | [08_templates.md](08_templates.md) | 동적 설정 파일 생성 | ★★★ |
| 9 | [09_common_modules.md](09_common_modules.md) | 핵심 모듈 치트시트 | ★★☆ |

---

## 실전 예제 목록

| 파일 | 내용 |
|------|------|
| [examples/01_hello_world.yml](examples/01_hello_world.yml) | 첫 플레이북 — ping + 메시지 출력 |
| [examples/02_package_install.yml](examples/02_package_install.yml) | Nginx, Git 설치 |
| [examples/03_file_deploy.yml](examples/03_file_deploy.yml) | 파일/디렉토리 생성 및 배포 |
| [examples/04_service_management.yml](examples/04_service_management.yml) | 서비스 시작/중지/재시작 |
| [examples/05_user_management.yml](examples/05_user_management.yml) | 계정 생성, sudo 권한, SSH 키 |
| [examples/06_webserver_setup.yml](examples/06_webserver_setup.yml) | Nginx + 가상호스트 + 방화벽 |
| [examples/07_conditionals_loops.yml](examples/07_conditionals_loops.yml) | when / loop 실전 패턴 |
| [examples/hosts_example.ini](examples/hosts_example.ini) | 인벤토리 예제 |

---

## Ansible 한 줄 요약

```
"여러 서버에 동일한 작업을 자동으로 실행해주는 도구"
```

SSH만 되면 대상 서버에 아무것도 설치하지 않아도 됩니다.

---

## 빠른 시작 (5분)

```bash
# 1. 설치
pip install ansible

# 2. 연결 테스트
ansible all -i "192.168.1.10," -m ping -u ec2-user --private-key ~/.ssh/key.pem

# 3. 첫 플레이북 실행
ansible-playbook -i examples/hosts_example.ini examples/01_hello_world.yml
```
