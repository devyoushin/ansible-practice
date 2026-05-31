# Ansible 코드 표준 관행

## 롤 디렉토리 구조

```
roles/<이름>/
├── tasks/
│   ├── main.yml       # include_tasks로 파일 분리 필수
│   ├── install.yml
│   ├── configure.yml
│   └── service.yml
├── defaults/
│   └── main.yml       # 모든 변수 기본값 (가장 낮은 우선순위)
├── vars/
│   └── main.yml       # 절대값 (오버라이드 불가 의도 시)
├── handlers/
│   └── main.yml       # notify로 재시작 제어
├── templates/
│   └── *.j2           # Jinja2 템플릿
├── files/             # 정적 파일
├── meta/
│   └── main.yml       # galaxy_info, dependencies
└── molecule/default/  # 단위 테스트
```

## 태스크 작성 규칙

```yaml
- name: "Nginx 패키지 설치"          # 한국어로 명확히
  package:
    name: nginx
    state: present
  tags: [install, nginx]             # 태그 필수

- name: "Nginx 설정 파일 배포"
  template:
    src: nginx.conf.j2
    dest: /etc/nginx/nginx.conf
    owner: root
    group: root
    mode: '0644'                     # mode 항상 명시
  notify: nginx 재시작               # 핸들러로 재시작 제어
  tags: [configure, nginx]
```

## 필수 규칙

### 멱등성 (Idempotency)
- `state: present` 사용 (not `state: latest` — prod)
- `creates:` 또는 `stat` 체크로 중복 실행 방지
- `shell`/`command` 사용 시 `changed_when: false` 또는 적절한 조건 설정

### 비밀 관리
- 하드코딩 금지 — `vault_` 접두사 Vault 변수만 사용
- group_vars에 `vault.yml` 분리 (ansible-vault encrypt)
- `.gitignore`에 `*.vault`, `vault_pass.txt` 추가

### prod 안전성
```yaml
- hosts: webservers
  serial: "25%"             # 25%씩 롤링 적용
  max_fail_percentage: 0    # 1대 실패 시 즉시 중단
```

### become 최소화
```yaml
- name: "설정 파일 배포 (root 불필요)"
  template:
    src: app.conf.j2
    dest: /etc/app/app.conf
  # become 없이 처리 가능한 경우 사용 안 함

- name: "시스템 서비스 재시작 (root 필요)"
  systemd:
    name: app
    state: restarted
  become: true              # 필요한 태스크에만 적용
```

## 플레이북 태그 표준

| 태그 | 설명 |
|------|------|
| `install` | 패키지 설치 |
| `configure` | 설정 파일 배포 |
| `service` | 서비스 시작/재시작 |
| `security` | 보안 강화 설정 |
| `update` | 버전 업데이트 |
| `cleanup` | 불필요 파일 정리 |

## Vault 변수 패턴

```yaml
# group_vars/all/vault.yml (암호화됨)
vault_db_root_password: "..."
vault_db_app_password: "..."

# group_vars/all/vars.yml (평문)
db_root_password: "{{ vault_db_root_password }}"
db_app_password: "{{ vault_db_app_password }}"
```
