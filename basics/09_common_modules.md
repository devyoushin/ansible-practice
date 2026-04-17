# 09. 자주 쓰는 모듈 치트시트

> 모듈 = Ansible의 기능 단위. "무엇을 할지"를 담당합니다.

---

## 패키지 관리

```yaml
# dnf (RHEL/Rocky/CentOS 8+)
- dnf:
    name: nginx           # 패키지명
    state: present        # present=설치, absent=제거, latest=최신
    enablerepo: epel      # 특정 레포 활성화

# 여러 패키지 한번에
- dnf:
    name:
      - nginx
      - git
      - curl
    state: present

# apt (Ubuntu/Debian)
- apt:
    name: nginx
    state: present
    update_cache: true    # apt-get update 먼저 실행

# OS 자동 감지 (RHEL/Ubuntu 모두 동작)
- package:
    name: nginx
    state: present
```

---

## 서비스 관리

```yaml
- service:
    name: nginx
    state: started      # started, stopped, restarted, reloaded
    enabled: true       # 부팅 시 자동 시작

# systemd 전용 (더 많은 옵션)
- systemd:
    name: nginx
    state: started
    enabled: true
    daemon_reload: true  # systemctl daemon-reload 먼저 실행
```

---

## 파일/디렉토리

```yaml
# 파일 생성, 권한, 소유자 설정
- file:
    path: /var/log/myapp
    state: directory     # directory=폴더, touch=빈파일, absent=삭제, link=심볼릭링크
    owner: myapp
    group: myapp
    mode: "0750"

# 심볼릭 링크
- file:
    src: /etc/nginx/sites-available/myapp
    dest: /etc/nginx/sites-enabled/myapp
    state: link

# 재귀적으로 권한 변경
- file:
    path: /var/www/html
    recurse: true
    owner: nginx
    group: nginx
```

---

## 파일 복사/배포

```yaml
# 로컬 파일 → 원격 서버
- copy:
    src: files/index.html
    dest: /var/www/html/index.html
    owner: nginx
    mode: "0644"

# 변수를 채운 설정 파일 생성
- template:
    src: nginx.conf.j2
    dest: /etc/nginx/nginx.conf
    mode: "0644"
    backup: true         # 기존 파일 백업 (.12345~ 형태)

# 파일에 내용 직접 쓰기
- copy:
    content: |
      line1
      line2
    dest: /etc/myapp/config.txt
```

---

## 파일 내용 편집

```yaml
# 특정 줄이 있는지 확인하고 없으면 추가
- lineinfile:
    path: /etc/hosts
    line: "192.168.1.10 web1.internal"
    state: present       # present=추가/유지, absent=제거

# 정규식으로 줄 교체
- lineinfile:
    path: /etc/ssh/sshd_config
    regexp: '^#?PermitRootLogin'
    line: 'PermitRootLogin no'

# 여러 줄 추가 (블록 단위)
- blockinfile:
    path: /etc/hosts
    block: |
      192.168.1.10 web1
      192.168.1.11 web2
      192.168.1.20 db1
    marker: "# {mark} ANSIBLE MANAGED"  # 블록 표시 주석
```

---

## 명령 실행

```yaml
# shell (쉘 문법 사용 가능: 파이프, 리다이렉트, 변수)
- shell: |
    df -h | grep /var
    echo "완료" >> /tmp/log.txt
  register: result

# command (쉘 문법 없이 순수 명령어, 보안상 권장)
- command: systemctl status nginx
  register: nginx_status
  changed_when: false    # 실행해도 changed 아님 (조회 목적)
  failed_when: nginx_status.rc not in [0, 3]

# 특정 조건일 때만 실행 (멱등성 확보)
- command: /opt/myapp/bin/init-db
  args:
    creates: /opt/myapp/.db_initialized   # 이 파일 있으면 실행 안 함
```

---

## 사용자/그룹 관리

```yaml
# 사용자 생성
- user:
    name: deploy
    shell: /bin/bash
    groups: wheel
    append: true         # 기존 그룹 유지하고 추가
    create_home: true
    password: "{{ 'mypassword' | password_hash('sha512') }}"

# 사용자 삭제
- user:
    name: olduser
    state: absent
    remove: true         # 홈 디렉토리도 삭제

# 그룹 생성
- group:
    name: developers
    gid: 2000
    state: present

# SSH 공개키 등록
- authorized_key:
    user: deploy
    key: "{{ lookup('file', '~/.ssh/id_rsa.pub') }}"
    state: present
```

---

## 파일 다운로드

```yaml
# URL에서 파일 다운로드
- get_url:
    url: https://example.com/app-2.1.0.tar.gz
    dest: /tmp/app-2.1.0.tar.gz
    checksum: sha256:abc123...   # 무결성 검증

# 압축 해제
- unarchive:
    src: /tmp/app-2.1.0.tar.gz
    dest: /opt/
    remote_src: true             # 원격 서버에 있는 파일
    creates: /opt/app-2.1.0      # 폴더 있으면 건너뜀
```

---

## HTTP 요청

```yaml
# Health check
- uri:
    url: http://localhost:8080/health
    method: GET
    status_code: 200
    timeout: 30
  register: health_check
  until: health_check.status == 200   # 성공할 때까지 재시도
  retries: 10
  delay: 5

# POST 요청
- uri:
    url: "{{ slack_webhook }}"
    method: POST
    body_format: json
    body:
      text: "배포 완료: {{ inventory_hostname }}"
```

---

## 재시도 (until/retries/delay)

```yaml
# 서비스가 올라올 때까지 기다리기
- name: 앱 서버 기동 대기
  uri:
    url: http://localhost:8080/actuator/health
    status_code: 200
  register: app_health
  until: app_health.status == 200
  retries: 12        # 최대 12번 재시도
  delay: 10          # 10초 간격
  # 총 대기시간: 최대 2분
```

---

## 디버그 및 확인

```yaml
# 변수 값 출력
- debug:
    msg: "서버: {{ inventory_hostname }}, IP: {{ ansible_default_ipv4.address }}"

# 변수 전체 출력
- debug:
    var: ansible_facts    # 변수명만 지정

# 서버 정보 수집 (Facts)
- setup:
    filter: ansible_distribution*   # 특정 Facts만

# 작업 일시 정지 (확인 후 진행)
- pause:
    prompt: "계속 진행하시겠습니까? (Enter)"
    seconds: 30    # 30초 후 자동 진행

# 조건 검증 (실패 시 플레이 중단)
- assert:
    that:
      - ansible_memtotal_mb >= 2048
      - ansible_distribution == "RedHat"
    fail_msg: "최소 사양 미충족"
    success_msg: "사양 확인 완료"
```

---

## 빠른 참조표

| 모듈 | 용도 |
|------|------|
| `dnf` / `apt` / `package` | 패키지 설치/제거 |
| `service` / `systemd` | 서비스 시작/중지/재시작 |
| `file` | 파일/디렉토리/링크 생성, 권한 |
| `copy` | 파일 복사 |
| `template` | Jinja2 템플릿으로 파일 생성 |
| `lineinfile` | 파일 특정 줄 추가/수정/삭제 |
| `blockinfile` | 파일에 블록 단위 추가 |
| `command` | 명령 실행 (쉘 없이) |
| `shell` | 쉘 명령 실행 (파이프 가능) |
| `user` | 사용자 계정 관리 |
| `group` | 그룹 관리 |
| `authorized_key` | SSH 공개키 등록 |
| `get_url` | URL에서 파일 다운로드 |
| `unarchive` | 압축 해제 |
| `uri` | HTTP 요청 |
| `debug` | 변수/메시지 출력 |
| `assert` | 조건 검증 |
| `pause` | 일시 정지 |
| `set_fact` | 변수 생성 |
| `register` | 결과 변수로 저장 |
| `include_tasks` | 태스크 파일 포함 |
| `import_tasks` | 태스크 파일 가져오기 |

---

## 모듈 도움말 확인

```bash
# 모듈 옵션 확인
ansible-doc dnf
ansible-doc copy
ansible-doc template

# 모듈 목록 검색
ansible-doc -l | grep user
```
