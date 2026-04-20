새 Ansible 롤 또는 플레이북 문서를 생성합니다.

**사용법**: `/new-doc <롤명 또는 플레이북명>`

**예시**: `/new-doc roles/kafka` 또는 `/new-doc playbooks/failover`

다음 단계를 수행하세요:

1. `templates/service-doc.md`를 읽어 템플릿 구조를 확인하세요.
2. 대상 유형을 파악하세요:
   - **롤**: `roles/<이름>/` — tasks, handlers, defaults, templates 구조
   - **플레이북**: `playbooks/<이름>.yml` + 문서
3. 다음 내용을 포함한 `roles/<이름>/README.md` 또는 `playbooks/<이름>.md`를 생성하세요:
   - 역할/목적 설명
   - 지원 OS/환경
   - 주요 변수 (defaults/main.yml 기준)
   - 의존 롤 (meta/main.yml)
   - 실행 예시 (`ansible-playbook` 명령어)
   - 태그 목록
   - 트러블슈팅
4. `rules/ansible-conventions.md` 기준으로 롤 디렉토리 구조를 확인하세요.
