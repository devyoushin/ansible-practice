# 06. 핸들러 (Handlers)

> "변경이 발생했을 때만 실행되는 특수 태스크"

---

## 왜 핸들러가 필요한가?

**문제 상황:**
```yaml
tasks:
  - name: Nginx 설정 변경
    copy:
      src: nginx.conf
      dest: /etc/nginx/nginx.conf

  - name: Nginx 재시작  # ← 설정이 안 바뀌어도 매번 재시작됨 (비효율적)
    service:
      name: nginx
      state: restarted
```

**핸들러 사용:**
```yaml
tasks:
  - name: Nginx 설정 변경
    copy:
      src: nginx.conf
      dest: /etc/nginx/nginx.conf
    notify: Nginx 재시작    # ← "변경되면 핸들러 호출해줘"

handlers:
  - name: Nginx 재시작      # ← 실제 변경이 있을 때만 실행
    service:
      name: nginx
      state: restarted
```

---

## 핵심 동작 방식

```
태스크 실행
    │
    ├── 변경 없음 (ok) → notify 무시 → 핸들러 실행 안 됨
    │
    └── 변경 발생 (changed) → notify 발동 → 플레이 끝에 핸들러 실행
```

**중요: 핸들러는 플레이가 끝날 때 한 번만 실행됩니다.**

```yaml
tasks:
  - name: 설정 1 변경
    copy: ...
    notify: Nginx 재시작    # 1번째 호출

  - name: 설정 2 변경
    copy: ...
    notify: Nginx 재시작    # 2번째 호출 (중복)

handlers:
  - name: Nginx 재시작
    service:
      name: nginx
      state: restarted
    # → 위에서 2번 notify 해도 실제로는 딱 1번만 재시작됨
```

---

## 전체 예제

```yaml
---
- name: Nginx 구성
  hosts: webservers
  become: true

  handlers:
    # handlers 섹션을 tasks 위에 쓰는 것도 가능 (관례상 tasks 아래에 쓰기도 함)
    - name: Nginx 재시작
      service:
        name: nginx
        state: restarted

    - name: Nginx 설정 리로드
      service:
        name: nginx
        state: reloaded    # 재시작 없이 설정만 다시 읽음

    - name: firewalld 재로드
      service:
        name: firewalld
        state: reloaded

  tasks:
    - name: Nginx 설치
      dnf:
        name: nginx
        state: present

    - name: nginx.conf 배포
      copy:
        src: nginx.conf
        dest: /etc/nginx/nginx.conf
      notify: Nginx 재시작         # 파일 변경 시 재시작

    - name: 가상 호스트 설정 배포
      template:
        src: vhost.conf.j2
        dest: /etc/nginx/conf.d/myapp.conf
      notify: Nginx 설정 리로드    # 가상 호스트는 리로드로 충분

    - name: 방화벽 HTTP 허용
      firewalld:
        service: http
        permanent: true
        state: enabled
      notify: firewalld 재로드
```

---

## 여러 핸들러를 한번에 notify

```yaml
tasks:
  - name: 핵심 설정 변경
    copy:
      src: app.conf
      dest: /etc/myapp/app.conf
    notify:
      - 앱 재시작
      - 모니터링 알림 발송

handlers:
  - name: 앱 재시작
    service:
      name: myapp
      state: restarted

  - name: 모니터링 알림 발송
    uri:
      url: "{{ slack_webhook }}"
      method: POST
      body_format: json
      body:
        text: "{{ inventory_hostname }} 앱 설정 변경됨"
```

---

## 즉시 실행 (flush_handlers)

기본적으로 핸들러는 플레이 끝에 실행되지만, 중간에 즉시 실행하고 싶을 때:

```yaml
tasks:
  - name: Nginx 설정 변경
    copy:
      src: nginx.conf
      dest: /etc/nginx/nginx.conf
    notify: Nginx 재시작

  - name: 핸들러 즉시 실행
    meta: flush_handlers    # 여기서 바로 핸들러 실행

  - name: Nginx 정상 동작 확인 (재시작 후)
    uri:
      url: http://localhost/health
      status_code: 200
```

---

## 핸들러가 실행되지 않는 경우

```yaml
# 1. changed가 아니면 실행 안 됨
- name: 이미 최신 파일이면 notify 발동 안 됨
  copy:
    src: nginx.conf
    dest: /etc/nginx/nginx.conf
  notify: Nginx 재시작
  # → 파일이 동일하면 ok 상태 → 핸들러 실행 안 됨 (정상)

# 2. 이전 태스크 실패 시 핸들러 실행 안 됨
# 해결책: --force-handlers 옵션
ansible-playbook site.yml --force-handlers
```

---

## 다음 단계

롤 — 재사용 가능한 태스크 묶음 → [07_roles.md](07_roles.md)
