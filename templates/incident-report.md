# 장애 분석 보고서: {장애명}

> **발생 일시**: {YYYY-MM-DD HH:MM}
> **해결 일시**: {YYYY-MM-DD HH:MM}
> **관련 롤/플레이북**: {롤명 또는 플레이북명}
> **장애 등급**: {P1 | P2 | P3}
> **영향 환경**: {dev | staging | prod}
> **영향 범위**: {서비스/호스트 목록}

---

## 1. 요약

{장애 원인과 해결 방법을 3문장 이내로 요약. Ansible 관점에서 무엇이 잘못되었고 어떻게 고쳤는지}

---

## 2. 타임라인

| 시각 | 이벤트 |
|------|--------|
| HH:MM | 장애 감지 |
| HH:MM | 원인 분석 시작 |
| HH:MM | Ansible 진단 실행 |
| HH:MM | 해결 완료 |

---

## 3. 근본 원인

**관련 롤**: `roles/{롤명}/tasks/{파일}.yml`

**진단에 사용한 명령어**:
```bash
# Ad-hoc 진단
ansible -i inventories/prod/hosts.ini {호스트그룹} -m shell \
  -a "{진단 명령어}"

# 장애 대응 플레이북 실행
ansible-playbook -i inventories/prod/hosts.ini playbooks/incident_response.yml \
  --tags {태그}
```

{기술적 근본 원인 설명}

---

## 4. 해결 방법

```bash
{실제 해결 ansible-playbook 명령어}
```

```yaml
# 롤/태스크 수정 내용 (해당 시)
{변경된 YAML}
```

---

## 5. 재발 방지

| 대책 | 관련 파일 | 완료 기한 |
|------|----------|---------|
| {대책} | `roles/{롤명}/` 또는 `rules/` | {날짜} |

---

## 6. 학습 포인트

이 장애에서 확인한 Ansible 운영 원칙:
- {원칙 1}: `rules/ansible-conventions.md` 참조
