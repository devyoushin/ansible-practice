# 02. 인벤토리 (Inventory)

> "어느 서버에 실행할지 알려주는 목록"

---

## 가장 쉬운 형태 (INI 파일)

```ini
# hosts.ini

# 서버 IP 또는 도메인을 그냥 나열
192.168.1.10
192.168.1.11
web.mycompany.com
```

---

## 그룹으로 묶기

```ini
# hosts.ini

# [그룹이름] 으로 서버를 묶을 수 있음
[webservers]
192.168.1.10
192.168.1.11

[dbservers]
192.168.1.20

[appservers]
192.168.1.30
192.168.1.31
```

```bash
# 웹서버 그룹에만 실행
ansible-playbook -i hosts.ini site.yml --limit webservers

# DB 서버에만 ping
ansible dbservers -i hosts.ini -m ping
```

---

## 서버별 접속 정보 추가

```ini
[webservers]
# 호스트명          사용자              SSH 키 경로
web1 ansible_host=192.168.1.10  ansible_user=ec2-user  ansible_ssh_private_key_file=~/.ssh/key.pem
web2 ansible_host=192.168.1.11  ansible_user=ec2-user  ansible_ssh_private_key_file=~/.ssh/key.pem

[dbservers]
db1  ansible_host=192.168.1.20  ansible_user=centos    ansible_port=2222
```

---

## 자주 쓰는 접속 변수

| 변수 | 설명 | 예시 |
|------|------|------|
| `ansible_host` | 실제 접속 IP/도메인 | `192.168.1.10` |
| `ansible_user` | SSH 접속 계정 | `ec2-user`, `root` |
| `ansible_port` | SSH 포트 | `22` (기본값) |
| `ansible_ssh_private_key_file` | SSH 개인키 경로 | `~/.ssh/key.pem` |
| `ansible_password` | SSH 비밀번호 | `mypassword` (Vault로 암호화 권장) |
| `ansible_become` | sudo 사용 여부 | `true` |
| `ansible_become_user` | sudo 대상 계정 | `root` |

---

## 그룹 공통 변수 설정 ([그룹:vars])

```ini
[webservers]
web1 ansible_host=192.168.1.10
web2 ansible_host=192.168.1.11

# 그룹 전체에 적용되는 변수
[webservers:vars]
ansible_user=ec2-user
ansible_ssh_private_key_file=~/.ssh/key.pem
ansible_become=true

[dbservers]
db1 ansible_host=192.168.1.20

[dbservers:vars]
ansible_user=centos
ansible_become=true
```

---

## 그룹 안에 그룹 넣기 ([상위그룹:children])

```ini
[webservers]
web1 ansible_host=192.168.1.10
web2 ansible_host=192.168.1.11

[appservers]
app1 ansible_host=192.168.1.30

[dbservers]
db1 ansible_host=192.168.1.20

# "production" 그룹 = 위 세 그룹 전체
[production:children]
webservers
appservers
dbservers
```

```bash
# 전체 프로덕션 서버에 실행
ansible production -i hosts.ini -m ping
```

---

## YAML 형식 인벤토리 (더 구조적)

```yaml
# hosts.yml

all:
  children:
    webservers:
      hosts:
        web1:
          ansible_host: 192.168.1.10
        web2:
          ansible_host: 192.168.1.11
      vars:
        ansible_user: ec2-user

    dbservers:
      hosts:
        db1:
          ansible_host: 192.168.1.20
      vars:
        ansible_user: centos
```

---

## 환경별로 인벤토리 분리 (실무 패턴)

```
inventories/
├── dev/
│   ├── hosts.ini         # 개발 서버 목록
│   └── group_vars/
│       └── all.yml       # 개발 환경 변수
├── staging/
│   └── hosts.ini
└── prod/
    ├── hosts.ini         # 운영 서버 목록
    └── group_vars/
        └── all.yml       # 운영 환경 변수
```

```bash
# 개발 환경에 배포
ansible-playbook -i inventories/dev/hosts.ini site.yml

# 운영 환경에 배포
ansible-playbook -i inventories/prod/hosts.ini site.yml
```

---

## 인벤토리 확인 명령어

```bash
# 인벤토리에 등록된 호스트 목록 확인
ansible-inventory -i hosts.ini --list

# 트리 형태로 보기
ansible-inventory -i hosts.ini --graph

# 출력 예시
@all:
  |--@webservers:
  |  |--web1
  |  |--web2
  |--@dbservers:
  |  |--db1
```

---

## 특수 그룹 2가지

```ini
# all     = 인벤토리의 모든 서버
# ungrouped = 어떤 그룹에도 속하지 않은 서버

192.168.1.99    # 이 서버는 ungrouped에 자동 포함
```

```bash
# 전체 서버에 실행
ansible all -i hosts.ini -m ping
```

---

## 다음 단계

이제 "무엇을 할지" 작성하는 플레이북을 배워보세요 → [03_playbook_basics.md](03_playbook_basics.md)
