# 보안 체크리스트 — ansible-practice

## Vault 및 비밀 관리

- [ ] 모든 비밀번호/키는 `vault_` 접두사 변수로 관리
- [ ] `ansible-vault encrypt` 적용된 파일만 git 커밋
- [ ] `.gitignore`에 `*.vault_pass`, `vault_pass.txt` 추가
- [ ] `no_log: true` — 비밀 출력되는 태스크에 설정
- [ ] `mask_secret` 필터 — 로그 출력 시 비밀 마스킹

## SSH 강화 (security 롤 기준)

- [ ] `PasswordAuthentication no`
- [ ] `PermitRootLogin no`
- [ ] `MaxAuthTries 3`
- [ ] `ClientAliveInterval 300`
- [ ] `AllowUsers` 또는 `AllowGroups` 명시
- [ ] 불필요한 SSH 포트(22) 변경 고려

## 파일 권한

- [ ] 설정 파일: `mode: '0644'`
- [ ] 비밀 파일 (인증서, 키): `mode: '0600'`
- [ ] 실행 파일: `mode: '0755'`
- [ ] 디렉토리: `mode: '0755'` 또는 `'0750'`
- [ ] 웹 루트: 소유자 nginx/www-data, `mode: '0644'`

## 서비스별 보안

### MariaDB
- [ ] `bind-address = 127.0.0.1` (필요한 경우만 외부 허용)
- [ ] `skip_name_resolve = 1`
- [ ] 불필요한 익명 계정 제거
- [ ] `validate_password` 플러그인 활성화

### Redis
- [ ] `requirepass` 설정 (vault_redis_password)
- [ ] `bind 127.0.0.1` (외부 노출 금지)
- [ ] `protected-mode yes`
- [ ] TLS 활성화 (prod)

### Nginx
- [ ] `server_tokens off`
- [ ] TLS 1.2 이상만 허용
- [ ] HSTS 헤더 설정
- [ ] `X-Frame-Options: DENY`

## firewalld 설정

- [ ] 필요한 포트만 허용 (`firewalld` 롤 또는 security 롤)
- [ ] 서비스 내부 통신은 private IP로만 제한
- [ ] 관리 포트(SSH)는 Bastion 또는 VPN IP만 허용

## auditd (선택)

- [ ] 특권 명령어 실행 감사 (`auditd` 롤)
- [ ] 파일 변경 감사 규칙 (`-w /etc/passwd -p wa`)

## prod 배포 전 필수

```bash
# 드라이런으로 변경 사항 사전 확인
ansible-playbook -i inventories/prod/hosts.ini playbooks/site.yml \
  --check --diff --ask-vault-pass

# ansible-lint 검사
ansible-lint playbooks/site.yml
```
