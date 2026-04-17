# 07. 롤 (Roles)

> "재사용 가능한 작업 묶음 — 한 번 만들면 여러 프로젝트에서 사용"

---

## 롤이란?

플레이북이 커지면 관리가 어려워집니다.

```yaml
# 플레이북이 이렇게 길어지면 관리 힘듦
tasks:
  # 공통 설정 (50줄)
  # Nginx 설치 (80줄)
  # SSL 설정 (60줄)
  # 방화벽 설정 (30줄)
  # 모니터링 설정 (70줄)
  # 총 290줄... 😰
```

롤을 쓰면:
```yaml
# 짧고 명확한 플레이북
roles:
  - common
  - webserver
  - ssl
  - monitoring
```

---

## 롤 디렉토리 구조

```
roles/
└── webserver/           ← 롤 이름
    ├── tasks/
    │   └── main.yml     ← 핵심: 실행할 태스크 목록
    ├── handlers/
    │   └── main.yml     ← 핸들러
    ├── templates/
    │   └── nginx.conf.j2  ← Jinja2 템플릿 파일
    ├── files/
    │   └── index.html   ← 정적 파일 (그대로 배포)
    ├── vars/
    │   └── main.yml     ← 고정 변수 (덮어쓰기 어려움)
    ├── defaults/
    │   └── main.yml     ← 기본 변수 (쉽게 덮어쓰기 가능)
    └── meta/
        └── main.yml     ← 롤 메타정보, 의존 롤
```

**실제로 자주 쓰는 것: tasks/, handlers/, templates/, defaults/**

---

## 가장 간단한 롤 만들기

```bash
# 롤 기본 구조 자동 생성
ansible-galaxy role init roles/webserver
```

```yaml
# roles/webserver/tasks/main.yml
---
- name: Nginx 설치
  dnf:
    name: nginx
    state: present

- name: nginx.conf 배포
  template:
    src: nginx.conf.j2
    dest: /etc/nginx/nginx.conf
  notify: Nginx 재시작

- name: Nginx 시작
  service:
    name: nginx
    state: started
    enabled: true
```

```yaml
# roles/webserver/handlers/main.yml
---
- name: Nginx 재시작
  service:
    name: nginx
    state: restarted
```

```yaml
# roles/webserver/defaults/main.yml
---
nginx_port: 80
nginx_worker_processes: auto
nginx_keepalive_timeout: 65
```

---

## 롤 사용법

### 방법 1: roles 섹션

```yaml
# site.yml
---
- name: 웹서버 설정
  hosts: webservers
  become: true
  roles:
    - common      # roles/common 실행
    - webserver   # roles/webserver 실행
    - ssl         # roles/ssl 실행
```

### 방법 2: include_role (태스크 중간에 삽입)

```yaml
tasks:
  - name: 공통 설정 먼저
    include_role:
      name: common

  - name: 뭔가 다른 작업
    debug: msg="중간 작업"

  - name: 웹서버 설정
    include_role:
      name: webserver
```

### 방법 3: 변수 오버라이드

```yaml
roles:
  - role: webserver
    vars:
      nginx_port: 8080      # defaults 값을 여기서 덮어씀
      nginx_worker_processes: 4
```

---

## 롤 실행 순서

```
플레이 실행 순서:
1. pre_tasks       (롤 실행 전 태스크)
2. roles           (롤들)
3. tasks           (일반 태스크)
4. post_tasks      (마지막 태스크)
5. handlers        (notify된 핸들러들)
```

```yaml
---
- name: 서버 구성
  hosts: all
  become: true

  pre_tasks:
    - name: 업그레이드 전 알림
      debug: msg="설정 시작"

  roles:
    - common
    - webserver

  tasks:
    - name: 추가 설정
      debug: msg="추가 작업"

  post_tasks:
    - name: 완료 알림
      debug: msg="설정 완료"
```

---

## 롤 의존성 (meta/main.yml)

```yaml
# roles/webserver/meta/main.yml
---
dependencies:
  - role: common    # webserver 실행 전 common 자동 실행
  - role: firewall
    vars:
      open_ports: [80, 443]
```

---

## Galaxy — 공개 롤 가져오기

```bash
# 공개 Nginx 롤 설치
ansible-galaxy install nginxinc.nginx

# requirements.yml 로 관리 (권장)
```

```yaml
# requirements.yml
roles:
  - name: nginxinc.nginx
  - name: geerlingguy.mysql
    version: "3.0.0"

collections:
  - name: community.general
  - name: ansible.posix
```

```bash
# requirements.yml 에 적힌 것 한번에 설치
ansible-galaxy install -r requirements.yml
```

---

## 현재 프로젝트의 롤 구조

이 프로젝트(`ansible-practice`)는 다음 롤들로 구성되어 있습니다:

```
roles/
├── common/      패키지, NTP, sysctl, ulimit 공통 초기화
├── webserver/   Nginx 가상호스트, log rotation
├── ssl/         Let's Encrypt, 자체 서명 인증서
├── database/    MariaDB 복제, 백업, 성능 튜닝
├── app/         Spring Boot 배포, systemd
├── monitoring/  Prometheus, Node Exporter
└── redis/       Redis + Sentinel HA
```

각 롤을 읽어보면 실제 프로덕션 구성이 어떻게 작성되는지 참고할 수 있습니다.

---

## 다음 단계

동적 설정 파일 만들기 — 템플릿 → [08_templates.md](08_templates.md)
