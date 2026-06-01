# 문서와 코드 규칙

이 디렉터리는 Ansible 문서와 실행 자산을 만들 때 지켜야 할 기준을 모아둡니다.

## 이 폴더의 역할

- 문서 작성 규칙
- Ansible 코드 컨벤션
- 보안 점검 기준
- 모니터링 문서 기준

여기는 “무엇을 할지”보다 “어떻게 써야 하는지”를 정리하는 곳입니다.

## 문서 목록

| 문서 | 용도 |
|------|------|
| `doc-writing.md` | README, 가이드, 설명 문서 작성 규칙 |
| `ansible-conventions.md` | 롤 구조, 태그, Vault, idempotency 기준 |
| `security-checklist.md` | 보안 검토 체크리스트 |
| `monitoring.md` | 모니터링 문서 기준 |

## 어떻게 쓰나

1. 새 롤이나 플레이북을 만들기 전에 `ansible-conventions.md`를 봅니다.
2. 문서를 작성할 때는 `doc-writing.md`를 봅니다.
3. 민감 정보나 권한이 걸리는 변경은 `security-checklist.md`를 봅니다.
4. 알림, 지표, 로그가 연결되는 문서는 `monitoring.md`를 봅니다.

## 관련 문서

- `../agents/README.md`
- `../templates/README.md`
- `../getting-started.md`
