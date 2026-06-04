# Inventories

Ansible이 접속할 대상 호스트를 환경별로 정의합니다.

| 경로 | 목적 |
|------|------|
| `dev/hosts.ini` | 개발 환경 정적 인벤토리 |
| `staging/hosts.ini` | 스테이징 환경 정적 인벤토리 |
| `prod/hosts.ini` | 운영 환경 정적 인벤토리 |
| `aws/ec2.yml` | AWS EC2 동적 인벤토리 |

민감 값은 inventory 파일에 직접 쓰지 말고 Vault 또는 외부 Secret 관리 도구로 분리합니다.

