# 01. Ansible이란?

---

## 쉽게 비유하면

> **Ansible = 서버들에게 보내는 "작업 지시서"**

식당을 생각해보세요.
주방장(Ansible)이 레시피(플레이북)를 보고
여러 요리사(서버)에게 동시에 같은 요리를 만들도록 지시합니다.

```
내 PC (Ansible 설치)
     │
     ├─── SSH ──→  웹서버 1 (192.168.1.10)
     ├─── SSH ──→  웹서버 2 (192.168.1.11)
     └─── SSH ──→  DB 서버  (192.168.1.20)

"Nginx 설치해줘" → 3대 서버 동시 실행
```

---

## 왜 Ansible을 쓰는가?

### 기존 방식 (수동)
```bash
# 서버 1 접속 → 설치
ssh user@server1
sudo dnf install nginx -y
sudo systemctl enable --now nginx

# 서버 2 접속 → 또 설치
ssh user@server2
sudo dnf install nginx -y
sudo systemctl enable --now nginx

# 서버가 10대면? 20대면? 😩
```

### Ansible 방식
```yaml
# install_nginx.yml
- hosts: webservers       # 웹서버 그룹 전체
  tasks:
    - name: Nginx 설치
      dnf:
        name: nginx
        state: present
    - name: Nginx 시작
      service:
        name: nginx
        state: started
        enabled: true

# 서버가 100대여도 명령 1번으로 끝
ansible-playbook install_nginx.yml
```

---

## Ansible의 3가지 특징

### 1. 에이전트리스 (Agentless)
```
다른 도구들:  대상 서버에 에이전트 설치 필요
Ansible:      SSH만 되면 끝. 추가 설치 없음.
```

### 2. 멱등성 (Idempotency)
```
"몇 번 실행해도 결과가 같다"

처음 실행: Nginx 없음 → 설치함 ← 변경 발생
두 번째:   Nginx 있음 → 그냥 둠 ← 변경 없음

덕분에 "이미 설정했는지 확인" 코드를 따로 안 짜도 됨
```

### 3. YAML 문법
```yaml
# 사람이 읽기 쉬운 문법
- name: 사용자 생성
  user:
    name: deploy
    shell: /bin/bash
    groups: wheel

# 코드를 몰라도 "무슨 작업인지" 이해 가능
```

---

## Ansible의 구성 요소 한눈에 보기

```
┌─────────────────────────────────────────────────────┐
│                   Ansible 구성 요소                  │
│                                                      │
│  인벤토리         플레이북          롤                │
│  (어디서?)        (무엇을?)         (재사용 묶음)     │
│                                                      │
│  hosts.ini        site.yml          roles/           │
│  ┌──────────┐    ┌──────────┐       ├─ webserver/    │
│  │webservers│    │- hosts:  │       ├─ database/     │
│  │  srv1    │    │  tasks:  │       └─ common/       │
│  │  srv2    │    │    - ... │                        │
│  └──────────┘    └──────────┘                        │
│                                                      │
│  변수              모듈             핸들러            │
│  (설정값)          (실행단위)        (조건부실행)      │
│                                                      │
│  app_port: 8080    dnf:             notify: restart  │
│  db_name: mydb     copy:            handlers:        │
│                    service:           - name: restart │
└─────────────────────────────────────────────────────┘
```

---

## Ansible vs 쉘 스크립트 비교

| 항목 | 쉘 스크립트 | Ansible |
|------|-------------|---------|
| 멱등성 | 직접 구현해야 함 | 자동 보장 |
| 에러 처리 | if문 직접 작성 | 자동 처리 |
| 여러 서버 동시 | 반복문 직접 구현 | 인벤토리로 해결 |
| 가독성 | 낮음 | 높음 (YAML) |
| 재사용 | 어려움 | 롤로 쉽게 재사용 |

---

## 설치 방법

```bash
# Python pip으로 설치 (권장)
pip install ansible

# RHEL/CentOS
sudo dnf install ansible

# macOS
brew install ansible

# 설치 확인
ansible --version
```

---

## 다음 단계

인벤토리(어느 서버?)를 먼저 배우세요 → [02_inventory.md](02_inventory.md)
