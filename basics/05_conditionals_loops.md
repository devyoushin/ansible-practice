# 05. 조건문(when)과 반복문(loop)

---

## 조건문 — when

> "이 조건일 때만 실행해라"

### 기본 형태

```yaml
tasks:
  - name: RHEL에서만 실행
    dnf:
      name: nginx
      state: present
    when: ansible_distribution == "RedHat"    # 조건

  - name: Ubuntu에서만 실행
    apt:
      name: nginx
      state: present
    when: ansible_distribution == "Ubuntu"
```

### 자주 쓰는 조건 패턴

```yaml
vars:
  env: prod
  app_port: 8080
  features: [ssl, cache, monitoring]

tasks:
  # 문자열 비교
  - name: 운영 환경에서만
    debug: msg="운영 환경 실행"
    when: env == "prod"

  # 부정
  - name: 운영 환경이 아닐 때
    debug: msg="개발/스테이징 실행"
    when: env != "prod"

  # 숫자 비교
  - name: 포트가 443이면
    debug: msg="HTTPS 설정"
    when: app_port == 443

  # 값 포함 여부
  - name: ssl 기능 활성화된 경우
    debug: msg="SSL 설정 적용"
    when: "'ssl' in features"

  # 변수 존재 여부
  - name: 버전 변수가 있을 때만
    debug: msg="버전: {{ app_version }}"
    when: app_version is defined

  # 변수 없을 때
  - name: 버전 미정의 시 기본 처리
    debug: msg="버전 없음"
    when: app_version is not defined

  # OS 버전으로 분기
  - name: RHEL 8 이상에서만
    debug: msg="RHEL 8+"
    when: ansible_distribution_major_version | int >= 8
```

### 여러 조건 AND / OR

```yaml
tasks:
  # AND — 둘 다 만족해야 실행
  - name: 운영 환경의 웹서버에서만
    debug: msg="운영 웹서버"
    when:
      - env == "prod"
      - "'webservers' in group_names"

  # OR — 하나라도 만족하면 실행
  - name: RHEL 또는 Rocky
    debug: msg="RedHat 계열"
    when: >
      ansible_distribution == "RedHat" or
      ansible_distribution == "Rocky"
```

### register 결과로 조건 분기

```yaml
tasks:
  - name: Nginx 상태 확인
    command: systemctl is-active nginx
    register: nginx_status
    failed_when: false    # 실패해도 계속 진행

  - name: Nginx 중지 상태면 시작
    service:
      name: nginx
      state: started
    when: nginx_status.stdout == "inactive"

  - name: 파일 존재 여부 확인
    stat:
      path: /etc/nginx/nginx.conf
    register: nginx_conf

  - name: 파일 없으면 기본 파일 복사
    copy:
      src: nginx.conf.default
      dest: /etc/nginx/nginx.conf
    when: not nginx_conf.stat.exists
```

---

## 반복문 — loop

> "같은 작업을 여러 값으로 반복"

### 기본 형태

```yaml
tasks:
  # 패키지 여러 개 한꺼번에 설치
  - name: 패키지 설치
    dnf:
      name: "{{ item }}"     # item = 현재 반복 값
      state: present
    loop:
      - nginx
      - git
      - curl
      - vim
```

### 딕셔너리 반복

```yaml
tasks:
  # 사용자 여러 명 생성
  - name: 사용자 생성
    user:
      name: "{{ item.name }}"
      shell: "{{ item.shell }}"
      groups: "{{ item.groups }}"
    loop:
      - { name: alice, shell: /bin/bash,  groups: wheel }
      - { name: bob,   shell: /bin/bash,  groups: users }
      - { name: carol, shell: /sbin/nologin, groups: users }

  # 디렉토리 여러 개 생성
  - name: 디렉토리 생성
    file:
      path: "{{ item.path }}"
      owner: "{{ item.owner }}"
      mode: "{{ item.mode }}"
      state: directory
    loop:
      - { path: /var/log/myapp,  owner: myapp, mode: "0750" }
      - { path: /var/run/myapp,  owner: myapp, mode: "0755" }
      - { path: /etc/myapp/conf, owner: root,  mode: "0644" }
```

### 변수 리스트 반복

```yaml
vars:
  packages:
    - name: nginx
      version: latest
    - name: mariadb
      version: "10.5"
    - name: redis
      version: latest

tasks:
  - name: 패키지 설치
    dnf:
      name: "{{ item.name }}-{{ item.version }}"
      state: present
    loop: "{{ packages }}"
    when: item.version != "skip"    # loop 안에서도 when 사용 가능
```

### loop_control — 반복 출력 제어

```yaml
tasks:
  - name: 사용자 생성
    user:
      name: "{{ item.name }}"
    loop:
      - { name: alice, password: secret1 }
      - { name: bob,   password: secret2 }
    loop_control:
      label: "{{ item.name }}"   # 로그에 item 전체 대신 name만 표시
      # (비밀번호가 로그에 노출되지 않도록)
```

### with_items (구버전 문법 — 참고용)

```yaml
# 예전 방식 (Ansible 2.5 이전)
- name: 패키지 설치
  dnf:
    name: "{{ item }}"
    state: present
  with_items:
    - nginx
    - git

# 현재 권장 방식 (loop 사용)
- name: 패키지 설치
  dnf:
    name: "{{ item }}"
    state: present
  loop:
    - nginx
    - git
```

---

## 조건문 + 반복문 함께 쓰기

```yaml
vars:
  services:
    - { name: nginx,    enabled: true  }
    - { name: postfix,  enabled: false }
    - { name: mariadb,  enabled: true  }

tasks:
  # enabled: true 인 서비스만 시작
  - name: 활성화된 서비스만 시작
    service:
      name: "{{ item.name }}"
      state: started
      enabled: true
    loop: "{{ services }}"
    when: item.enabled    # false면 skip
```

---

## 실전 예제: OS별 패키지 설치

```yaml
---
- name: 웹서버 설치 (OS 자동 감지)
  hosts: webservers
  become: true

  tasks:
    - name: RHEL/Rocky — Nginx 설치
      dnf:
        name: nginx
        state: present
      when: ansible_os_family == "RedHat"

    - name: Ubuntu/Debian — Nginx 설치
      apt:
        name: nginx
        state: present
        update_cache: true
      when: ansible_os_family == "Debian"

    - name: 공통 패키지 설치
      package:              # OS 자동 감지 모듈
        name: "{{ item }}"
        state: present
      loop:
        - curl
        - vim
        - git
```

---

## 다음 단계

핸들러 — 변경 시에만 실행하는 특수 태스크 → [06_handlers.md](06_handlers.md)
