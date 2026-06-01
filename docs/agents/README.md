# AI 작업 지침

이 디렉터리는 Ansible 문서와 롤을 다룰 때 사용하는 AI 작업 지침을 모아둡니다.

## 이 폴더의 역할

- 문서 작성 방식
- 롤 리뷰 기준
- 보안 감사 관점
- 역할 설계 기준

여기는 학습용 문서가 아니라, `CLAUDE.md`와 함께 작업 품질을 맞추는 보조 지침입니다.

## 문서 목록

| 문서 | 용도 |
|------|------|
| `doc-writer.md` | 롤/플레이북 문서 작성 기준 |
| `playbook-reviewer.md` | 플레이북 리뷰 관점 |
| `role-designer.md` | 롤 분해와 책임 경계 |
| `security-auditor.md` | 보안 점검 관점 |

## 어떻게 쓰나

1. 문서를 새로 쓸 때 `doc-writer.md`부터 봅니다.
2. 롤 구조가 애매하면 `role-designer.md`를 봅니다.
3. 변경 내용이 배포 흐름에 영향이 있으면 `playbook-reviewer.md`를 봅니다.
4. 비밀, 권한, 노출 범위가 걸리면 `security-auditor.md`를 봅니다.

## 관련 문서

- `../../CLAUDE.md`
- `../rules/README.md`
- `../templates/README.md`
