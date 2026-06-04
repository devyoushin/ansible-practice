# CI Examples

CI/CD 예시를 보관합니다. 실제 GitHub Actions로 사용하려면 `github-actions/workflows/*.yml` 파일을 저장소 루트의 `.github/workflows/` 아래로 복사합니다.

| 경로 | 목적 |
|------|------|
| `github-actions/workflows/ci.yml` | yamllint, ansible-lint, syntax-check, Molecule 예시 |
| `github-actions/workflows/deploy.yml` | dev/staging/prod 배포 파이프라인 예시 |

이 파일들은 실행 자산의 예시이며, 현재 위치에서는 GitHub Actions가 자동 실행하지 않습니다.

