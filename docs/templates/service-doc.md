# {롤명} 롤

> **분야**: {웹서버 | 데이터베이스 | 보안 | 모니터링 | 미들웨어 | 운영}
> **지원 OS**: {RHEL 8/9 | Rocky 8/9 | Ubuntu 22.04}
> **작성일**: {YYYY-MM-DD}

---

## 역할

{이 롤이 무엇을 설치/설정하는지, 왜 필요한지 3문장 이내}

---

## 디렉토리 구조

```
roles/{롤명}/
├── tasks/
│   ├── main.yml          # 메인 태스크 (include_tasks로 분리)
│   ├── install.yml       # 패키지 설치
│   ├── configure.yml     # 설정 파일 배포
│   └── service.yml       # 서비스 시작/활성화
├── defaults/
│   └── main.yml          # 기본 변수값
├── handlers/
│   └── main.yml          # 서비스 재시작 핸들러
├── templates/
│   └── {설정파일}.j2     # Jinja2 템플릿
├── files/                # 정적 파일
├── meta/
│   └── main.yml          # 의존 롤 정의
└── molecule/default/     # 단위 테스트
```

---

## 주요 변수

| 변수명 | 기본값 | 설명 |
|--------|--------|------|
| `{변수명}` | `{기본값}` | {설명} |

Vault 변수 (`vault_` 접두사):
| 변수명 | 설명 |
|--------|------|
| `vault_{변수명}` | {설명} |

---

## 의존 롤

```yaml
# meta/main.yml
dependencies:
  - role: common
```

---

## 태그

| 태그 | 설명 |
|------|------|
| `install` | 패키지 설치만 실행 |
| `configure` | 설정 파일 배포만 실행 |
| `service` | 서비스 시작/활성화만 실행 |

---

## 실행 예시

```bash
# 드라이런 (변경 사항 확인)
ansible-playbook -i inventories/prod/hosts.ini playbooks/site.yml \
  --tags {롤명} --check

# 실제 실행
ansible-playbook -i inventories/prod/hosts.ini playbooks/site.yml \
  --tags {롤명} --ask-vault-pass

# 특정 호스트만
ansible-playbook -i inventories/prod/hosts.ini playbooks/site.yml \
  --tags {롤명} --limit webservers
```

---

## 트러블슈팅

### {증상 1}

**원인**: {근본 원인}

**해결**:
```bash
{해결 명령어}
```

---

## 구현 체크리스트

- [ ] 모든 태스크에 `name:` 한국어 설명
- [ ] Vault 변수로 비밀 관리
- [ ] idempotency 확인 (2회 실행 시 `changed: 0`)
- [ ] `mode:` 명시 (파일/디렉토리 권한)
- [ ] molecule 테스트 통과
- [ ] yamllint 통과
