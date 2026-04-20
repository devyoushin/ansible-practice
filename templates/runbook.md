# Runbook: {작업명}

> **분류**: {배포 | 유지보수 | 긴급 대응 | 마이그레이션 | OS 업그레이드}
> **대상 플레이북**: `playbooks/{파일명}.yml`
> **영향 환경**: {dev | staging | prod}
> **작성일**: {YYYY-MM-DD}
> **예상 소요 시간**: {N분}
> **영향 범위**: {무중단 | 서비스 영향 있음}

---

## 사전 체크리스트

- [ ] Vault 비밀번호 준비 (`.vault_pass` 또는 `--ask-vault-pass`)
- [ ] 인벤토리 호스트 목록 확인
- [ ] `--check` 드라이런으로 변경 사항 사전 확인
- [ ] prod: 배포 대상 서비스 모니터링 알람 대기
- [ ] 롤백 방법 확인
- [ ] 변경 승인 확인 (prod의 경우)

---

## 환경 확인

```bash
# Ansible 버전 확인
ansible --version

# 인벤토리 호스트 목록 확인
ansible-inventory -i inventories/{env}/hosts.ini --list

# 연결 테스트
ansible -i inventories/{env}/hosts.ini all -m ping
```

---

## Step 1: 드라이런 (필수)

```bash
ansible-playbook -i inventories/{env}/hosts.ini playbooks/{플레이북}.yml \
  --check \
  --diff \
  --ask-vault-pass
```

변경 예정 항목을 확인하고 의도치 않은 변경이 없는지 검토하세요.

---

## Step 2: {작업 내용}

```bash
ansible-playbook -i inventories/{env}/hosts.ini playbooks/{플레이북}.yml \
  --ask-vault-pass \
  {옵션}
```

또는 부분 실행:

```bash
ansible-playbook -i inventories/{env}/hosts.ini playbooks/{플레이북}.yml \
  --tags {태그} \
  --limit {호스트그룹} \
  --ask-vault-pass
```

---

## Step 3: 완료 확인

```bash
# 서비스 상태 확인
ansible -i inventories/{env}/hosts.ini {호스트그룹} -m shell \
  -a "systemctl status {서비스명}"

# 로그 확인
ansible -i inventories/{env}/hosts.ini {호스트그룹} -m shell \
  -a "journalctl -u {서비스명} --since '5 minutes ago'"
```

**성공 기준**:
- [ ] {조건 1}
- [ ] {조건 2}

---

## 롤백 절차

```bash
# 이전 버전으로 롤백
ansible-playbook -i inventories/{env}/hosts.ini playbooks/{플레이북}.yml \
  -e "{변수명}={이전 버전}" \
  --ask-vault-pass
```

---

## 모니터링 포인트

| 지표 | 확인 방법 | 정상 기준 |
|------|---------|---------|
| {지표} | Prometheus / CloudWatch | {기준} |
