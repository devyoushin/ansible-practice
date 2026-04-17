# 04. 변수 (Variables)

> "값을 이름으로 저장해서 여러 곳에서 재사용"

---

## 변수 선언 방법 5가지

### 1. 플레이북 안에 직접

```yaml
- name: 앱 배포
  hosts: appservers
  vars:
    app_port: 8080
    app_name: myapp
    app_version: "2.1.0"

  tasks:
    - name: 포트 출력
      debug:
        msg: "앱 포트: {{ app_port }}"    # {{ }} 로 변수 참조
```

### 2. 외부 파일로 분리 (vars_files)

```yaml
# vars/app.yml
app_port: 8080
app_name: myapp
db_host: 192.168.1.20
```

```yaml
# playbook.yml
- name: 앱 배포
  hosts: appservers
  vars_files:
    - vars/app.yml    # 파일에서 변수 불러오기

  tasks:
    - debug:
        msg: "{{ app_name }} 포트: {{ app_port }}"
```

### 3. 인벤토리의 group_vars 폴더

```
inventories/
└── prod/
    ├── hosts.ini
    └── group_vars/
        ├── all.yml           # 모든 서버 공통 변수
        ├── webservers.yml    # webservers 그룹 변수
        └── dbservers.yml     # dbservers 그룹 변수
```

```yaml
# group_vars/all.yml
ntp_server: time.bora.net
timezone: Asia/Seoul
log_level: INFO

# group_vars/webservers.yml
nginx_worker_processes: auto
nginx_port: 80
```

### 4. 실행 시 명령줄에서 전달 (-e)

```bash
# 단일 변수
ansible-playbook site.yml -e "app_version=2.1.0"

# 여러 변수
ansible-playbook site.yml -e "app_version=2.1.0 env=prod"

# 파일로 전달
ansible-playbook site.yml -e @vars/prod.yml
```

### 5. 서버 정보에서 자동 수집 (Facts)

```yaml
tasks:
  - name: 서버 OS 버전 출력
    debug:
      msg: "OS: {{ ansible_distribution }} {{ ansible_distribution_version }}"
      # → "OS: RedHat 8.9"

  - name: 메모리 크기 출력
    debug:
      msg: "메모리: {{ ansible_memtotal_mb }}MB"

  - name: IP 주소 출력
    debug:
      msg: "IP: {{ ansible_default_ipv4.address }}"
```

```bash
# 어떤 Facts를 쓸 수 있는지 확인
ansible web1 -i hosts.ini -m setup | less
```

---

## 변수 우선순위 (높을수록 우선)

```
낮음 ↓                               높음 ↑
────────────────────────────────────────────
role defaults     →  group_vars/all  →
host_vars         →  플레이북 vars   →
vars_files        →  명령줄 -e 옵션
                                     ↑ 가장 강력
```

실무 팁: **명령줄 `-e`로 전달한 값은 무조건 우선 적용됩니다.**

---

## 변수 사용법 (Jinja2 문법)

```yaml
vars:
  app_name: myapp
  app_port: 8080
  servers:
    - web1
    - web2
  config:
    timeout: 30
    retry: 3

tasks:
  # 기본 참조
  - debug:
      msg: "{{ app_name }}"           # → "myapp"

  # 문자열 안에 삽입
  - debug:
      msg: "앱: {{ app_name }}:{{ app_port }}"  # → "앱: myapp:8080"

  # 리스트 접근
  - debug:
      msg: "첫 번째 서버: {{ servers[0] }}"     # → "web1"

  # 딕셔너리 접근
  - debug:
      msg: "타임아웃: {{ config.timeout }}"     # → "30"
      # 또는
      msg: "타임아웃: {{ config['timeout'] }}"  # 같은 결과

  # 기본값 지정 (변수 없을 때 fallback)
  - debug:
      msg: "버전: {{ app_version | default('latest') }}"
```

---

## register — 실행 결과를 변수로 저장

```yaml
tasks:
  - name: 현재 날짜 확인
    command: date +%Y-%m-%d
    register: today           # 결과를 today 변수에 저장

  - name: 날짜 출력
    debug:
      msg: "오늘: {{ today.stdout }}"   # stdout: 명령 출력 결과

  - name: Nginx 상태 확인
    command: systemctl is-active nginx
    register: nginx_status
    failed_when: false        # 실패해도 계속 진행

  - name: Nginx 상태 출력
    debug:
      msg: "Nginx 상태: {{ nginx_status.stdout }}"
      # → "Nginx 상태: active" 또는 "inactive"
```

### register 결과에서 자주 쓰는 키

| 키 | 설명 |
|----|------|
| `.stdout` | 명령 표준 출력 (문자열) |
| `.stdout_lines` | 표준 출력 (줄 단위 리스트) |
| `.stderr` | 표준 에러 출력 |
| `.rc` | 반환 코드 (0 = 성공) |
| `.changed` | 변경 발생 여부 (true/false) |
| `.failed` | 실패 여부 (true/false) |

---

## set_fact — 플레이북 안에서 변수 만들기

```yaml
tasks:
  - name: 메모리 계산
    set_fact:
      # JVM 힙 = 전체 메모리의 70%
      jvm_heap_mb: "{{ (ansible_memtotal_mb * 0.7) | int }}"

  - name: JVM 옵션 출력
    debug:
      msg: "-Xmx{{ jvm_heap_mb }}m"
      # → "-Xmx5734m" (메모리 8GB인 경우)
```

---

## 변수에서 자주 쓰는 필터

```yaml
vars:
  name: "  Hello World  "
  number: "42"
  items: [3, 1, 4, 1, 5, 9]

tasks:
  - debug:
      msg:
        - "{{ name | trim }}"           # "Hello World" (공백 제거)
        - "{{ name | upper }}"          # "  HELLO WORLD  "
        - "{{ name | lower }}"          # "  hello world  "
        - "{{ number | int }}"          # 42 (정수 변환)
        - "{{ number | int + 1 }}"      # 43
        - "{{ items | sort }}"          # [1, 1, 3, 4, 5, 9]
        - "{{ items | unique }}"        # [3, 1, 4, 5, 9]
        - "{{ items | max }}"           # 9
        - "{{ items | length }}"        # 6
        - "{{ 'abc' | upper }}"         # "ABC"
        - "{{ '/etc/nginx' | basename }}"  # "nginx"
        - "{{ '/etc/nginx' | dirname }}"   # "/etc"
```

---

## 실전 패턴: 환경별 변수 파일

```
group_vars/
├── all.yml             # 공통 설정
├── all/
│   ├── main.yml        # 일반 변수
│   └── vault.yml       # 암호화된 민감 변수 (Vault)
├── webservers.yml
└── dbservers.yml
```

```yaml
# group_vars/all.yml
app_name: myapp
timezone: Asia/Seoul

# group_vars/webservers.yml
nginx_port: 80
nginx_worker_processes: auto

# group_vars/dbservers.yml
mysql_port: 3306
mysql_max_connections: 200
```

---

## 다음 단계

조건문(when)과 반복문(loop)으로 더 유연하게 → [05_conditionals_loops.md](05_conditionals_loops.md)
