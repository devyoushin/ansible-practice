# Ansible Vault Rotation 런북

## 목적

Vault 비밀번호 또는 Vault에 저장된 시크릿 값을 안전하게 교체합니다.

## Vault 비밀번호 교체

```bash
cd ops
ansible-vault rekey inventories/prod/group_vars/vault.yml
ansible-vault rekey inventories/staging/group_vars/vault.yml
ansible-vault rekey inventories/dev/group_vars/vault.yml
```

## 시크릿 값 교체

```bash
cd ops
ansible-vault edit inventories/prod/group_vars/vault.yml
ansible-playbook -i inventories/prod/hosts.ini playbooks/site.yml --check --diff --ask-vault-pass
```

## 검토 기준

- 이전 비밀번호 파일이 로컬과 CI/CD 시크릿 저장소에서 제거되었는가?
- 교체 후 dry-run이 정상 동작하는가?
- 서비스 재시작이 필요한 시크릿은 배포 창 안에서 반영하는가?
- 장애 대응 문서와 담당자 공유 채널에 변경 사실을 남겼는가?
