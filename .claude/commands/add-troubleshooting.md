Ansible 트러블슈팅 케이스를 추가합니다.

**사용법**: `/add-troubleshooting <증상 설명>`

**예시**: `/add-troubleshooting MariaDB 복제 지연`

다음 단계를 수행하세요:

1. 관련 롤의 README.md 또는 플레이북 문서를 읽어 기존 트러블슈팅 섹션을 확인하세요.
2. 아래 형식으로 케이스를 작성하세요:

```markdown
### <증상>

**원인**: <근본 원인>

**확인 방법**:
\`\`\`bash
ansible -i inventories/<env>/hosts.ini <호스트그룹> -m shell -a "<확인 명령어>"
\`\`\`

**해결**:
\`\`\`bash
ansible-playbook -i inventories/<env>/hosts.ini playbooks/<플레이북>.yml \\
  --tags <태그> --limit <호스트>
\`\`\`

**예방**: <재발 방지 방법 — 롤 변수 또는 핸들러 수정>
```

3. 해당 롤 README.md의 트러블슈팅 섹션에 추가하세요.
4. 여러 롤에 공통 적용되는 문제라면 `rules/ansible-conventions.md`에도 추가하세요.
