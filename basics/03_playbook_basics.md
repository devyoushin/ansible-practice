# 03. 플레이북 기초 (Playbook)

> "서버에게 줄 작업 지시서"

---

## 기본 구조

```yaml
---                          # YAML 파일 시작 표시 (관례)
- name: 플레이 이름           # 이 작업 묶음의 설명
  hosts: webservers          # 어느 서버에? (인벤토리 그룹명)
  become: true               # sudo 권한 사용?

  tasks:                     # 실행할 작업 목록
    - name: 첫 번째 작업      # 작업 설명 (로그에 표시됨)
      모듈이름:               # 사용할 모듈
        옵션1: 값1
        옵션2: 값2

    - name: 두 번째 작업
      모듈이름:
        옵션: 값
```

---

## 가장 간단한 예제

```yaml
---
- name: 웹서버 초기 설정
  hosts: webservers
  become: true

  tasks:
    - name: Nginx 설치
      dnf:
        name: nginx
        state: present        # present = 설치, absent = 제거

    - name: Nginx 서비스 시작
      service:
        name: nginx
        state: started        # started, stopped, restarted
        enabled: true         # 부팅 시 자동 시작
```

```bash
# 실행
ansible-playbook -i hosts.ini webserver.yml

# 실행 결과 예시
PLAY [웹서버 초기 설정] ****************************

TASK [Nginx 설치] **********************************
changed: [web1]      ← 설치됨 (변경 발생)
ok: [web2]           ← 이미 설치되어 있음 (변경 없음)

TASK [Nginx 서비스 시작] ****************************
changed: [web1]
changed: [web2]

PLAY RECAP *****************************************
web1 : ok=2  changed=2  unreachable=0  failed=0
web2 : ok=2  changed=1  unreachable=0  failed=0
```

---

## 실행 결과 색상 의미

| 색상 | 의미 |
|------|------|
| 초록 (ok) | 이미 원하는 상태 — 변경 없음 |
| 노랑 (changed) | 작업 실행되어 변경됨 |
| 빨강 (failed) | 실패 |
| 파랑 (skipping) | 조건 불충족으로 건너뜀 |

---

## 여러 플레이를 하나의 파일에

```yaml
---
# 첫 번째 플레이: 웹서버 설정
- name: 웹서버 설정
  hosts: webservers
  become: true
  tasks:
    - name: Nginx 설치
      dnf:
        name: nginx
        state: present

# 두 번째 플레이: DB 서버 설정
- name: DB 서버 설정
  hosts: dbservers
  become: true
  tasks:
    - name: MariaDB 설치
      dnf:
        name: mariadb-server
        state: present
```

---

## 자주 쓰는 플레이 옵션

```yaml
- name: 예제
  hosts: all
  become: true             # sudo 사용
  become_user: root        # sudo 대상 (기본: root)
  gather_facts: true       # 서버 정보 수집 (기본: true)
  serial: 2                # 한 번에 2대씩 순차 실행 (롤링 업데이트)
  any_errors_fatal: true   # 1대 실패 시 전체 중단
  tags: [setup, common]    # 태그 (선택 실행용)
  vars:                    # 플레이 내 변수
    app_port: 8080
```

---

## 태그 사용법

```yaml
tasks:
  - name: Nginx 설치
    dnf:
      name: nginx
      state: present
    tags: [install, nginx]    # 태그 지정

  - name: 설정 파일 배포
    copy:
      src: nginx.conf
      dest: /etc/nginx/nginx.conf
    tags: [config, nginx]

  - name: 서비스 재시작
    service:
      name: nginx
      state: restarted
    tags: [restart]
```

```bash
# nginx 태그 붙은 작업만 실행
ansible-playbook site.yml --tags nginx

# install 태그 건너뛰고 실행
ansible-playbook site.yml --skip-tags install

# 설정만 배포하고 재시작
ansible-playbook site.yml --tags "config,restart"
```

---

## 유용한 실행 옵션

```bash
# 실제 변경 없이 미리 확인 (dry run)
ansible-playbook site.yml --check

# 변경될 내용 상세 확인
ansible-playbook site.yml --check --diff

# 특정 서버에만 실행
ansible-playbook site.yml --limit web1

# 변수 직접 전달
ansible-playbook site.yml -e "app_version=2.1.0"

# 실행 전 매 작업 확인
ansible-playbook site.yml --step

# 특정 태스크부터 시작
ansible-playbook site.yml --start-at-task "Nginx 설치"

# 상세 로그
ansible-playbook site.yml -v      # 기본
ansible-playbook site.yml -vv     # 더 상세
ansible-playbook site.yml -vvv    # 최상세 (디버깅용)
```

---

## 자주 하는 실수

### 들여쓰기 오류 (YAML에서 가장 흔한 실수)

```yaml
# 잘못된 예 (들여쓰기 불일치)
tasks:
  - name: Nginx 설치
    dnf:
    name: nginx        # ← 들여쓰기가 모자람
      state: present   # ← 들여쓰기가 너무 많음

# 올바른 예
tasks:
  - name: Nginx 설치
    dnf:
      name: nginx      # ← dnf 아래 2칸 들여쓰기
      state: present
```

### hosts 오타

```yaml
# 잘못된 예
hosts: webserver       # 인벤토리에는 webservers 인데 s 빠짐

# 올바른 예
hosts: webservers
```

---

## 플레이북 문법 검사

```bash
# 실행 전 문법 오류 확인
ansible-playbook site.yml --syntax-check

# 정상이면: playbook: site.yml
# 오류이면: ERROR! ... (어디서 틀렸는지 알려줌)
```

---

## 다음 단계

변수를 사용해서 더 유연하게 만들기 → [04_variables.md](04_variables.md)
