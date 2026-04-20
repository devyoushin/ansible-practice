Ansible 롤 또는 플레이북을 검토합니다.

**사용법**: `/review-doc <파일 또는 디렉토리 경로>`

**예시**: `/review-doc roles/database` 또는 `/review-doc playbooks/rolling_update.yml`

다음 기준으로 검토하세요:

**롤 구조 (rules/ansible-conventions.md 기준)**
- [ ] tasks/main.yml — 태스크 분리 및 태그 적용
- [ ] defaults/main.yml — 모든 변수 기본값 정의
- [ ] handlers/main.yml — 서비스 재시작 핸들러
- [ ] templates/ — Jinja2 템플릿 존재 여부
- [ ] meta/main.yml — 의존 롤 정의
- [ ] molecule/ — 단위 테스트 존재 여부

**코드 품질**
- [ ] 태스크에 `name:` 한국어 설명 작성
- [ ] `become: true` 최소 범위 적용
- [ ] 하드코딩된 비밀번호 없음 (vault 변수 사용)
- [ ] idempotent 보장 (반복 실행 시 동일 결과)

**보안 (rules/security-checklist.md 기준)**
- [ ] SSH 설정 강화 여부 (security 롤)
- [ ] 파일 권한 명시 (mode: '0644')
- [ ] Vault 암호화 변수 사용

**플레이북**
- [ ] prod 대상은 `serial:` 설정으로 롤링 적용
- [ ] `--check` 드라이런으로 사전 검증 가능 구조

검토 결과를 항목별로 정리하고 개선이 필요한 부분에 수정 코드를 제시하세요.
