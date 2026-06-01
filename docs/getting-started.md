# Ansible 시작 가이드

이 저장소에서 처음 시작할 때는 문서를 순서대로 읽는 것보다, 먼저 작업 종류를 구분하는 것이 빠릅니다.

## 1. 작업 종류를 고른다

| 작업 | 먼저 볼 문서 |
|------|--------------|
| Ansible 개념을 처음 익힘 | `basics/README.md` |
| 서비스를 어떻게 만들지 고민함 | `service-build-guide.md` |
| 예제 플레이북을 바로 실행해 봄 | `examples/README.md` |
| 실제 배포를 수정함 | `../ops/README.md` |
| 실패 원인을 추적함 | `runbooks/playbook-failure.md` |
| 배포 전에 점검함 | `checklists/pre-deploy.md` |

## 2. 개념부터 잡는다

처음 보는 경우에는 아래 순서가 가장 덜 흔들립니다.

1. `basics/README.md`
2. `basics/01_what_is_ansible.md`
3. `basics/02_inventory.md`
4. `basics/03_playbook_basics.md`
5. `basics/04_variables.md`
6. `basics/07_roles.md`
7. `examples/README.md`

## 3. 실제 실행 전 준비

```bash
pip install ansible boto3
ansible-galaxy install -r ../ops/requirements.yml
```

```bash
ansible-playbook -i ../ops/inventories/dev/hosts.ini ../ops/playbooks/site.yml --syntax-check
ansible-playbook -i ../ops/inventories/dev/hosts.ini ../ops/playbooks/site.yml --check --diff
```

## 4. 배포 흐름

1. dev 환경에서 syntax-check와 dry-run을 먼저 확인합니다.
2. `--limit` 또는 `--tags`로 변경 범위를 좁혀 실행합니다.
3. 문제가 없으면 staging, 마지막에 prod 순으로 올립니다.
4. prod 반영 전에는 `checklists/pre-deploy.md`를 다시 확인합니다.

## 5. 막혔을 때

| 증상 | 먼저 볼 문서 |
|------|--------------|
| 특정 호스트만 실패 | `runbooks/playbook-failure.md` |
| Vault 관련 오류 | `runbooks/vault-rotation.md` |
| 문서 규칙이 궁금함 | `rules/doc-writing.md` |
| 역할 구조가 헷갈림 | `basics/07_roles.md` |

## 추천 시작점

처음이라면 아래 순서가 가장 안전합니다.

1. `docs/README.md`
2. `docs/getting-started.md`
3. `docs/service-build-guide.md`
4. `docs/basics/README.md`
5. `docs/examples/README.md`
6. `ops/README.md`
