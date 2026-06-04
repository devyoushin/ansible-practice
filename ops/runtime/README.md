# Runtime Outputs

Ansible 실행 중 생성되는 로그와 결과물을 보관하는 위치입니다. 실행 산출물은 Git에 커밋하지 않고, `.gitkeep`만 추적합니다.

| 경로 | 목적 |
|------|------|
| `logs/` | `ansible.cfg`의 `log_path` 출력 위치 |
| `outputs/` | dry-run 결과, 변경 전후 비교, 장애 대응 로그 |
| `tmp/` | Ansible local temporary directory |

`runtime/logs/*.log`와 `runtime/tmp/`는 `.gitignore`로 제외합니다.

