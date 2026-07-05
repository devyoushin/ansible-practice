# Ansible 서비스 구축 가이드

이 문서는 `nginx`, `tomcat`, `kafka`, `elasticsearch`처럼 성격이 다른 서비스를 Ansible로 어떻게 나누고 구축할지 정리한 문서입니다.

목표는 단순 설치가 아니라, 재현 가능한 구성 관리 구조를 만드는 것입니다.

1. 어떤 서비스인지 분류한다.
2. 인벤토리와 변수 범위를 정한다.
3. 롤을 `install / configure / service / validate`로 나눈다.
4. 템플릿, 핸들러, 헬스체크를 붙인다.
5. 운영 절차와 실패 대응 문서를 함께 만든다.

---

## 먼저 결론

서비스를 만들 때 가장 중요한 판단 기준은 세 가지입니다.

| 질문 | 의미 | 예시 |
|------|------|------|
| 단일 프로세스인가 | 설치와 설정, 서비스 시작이 단순한가 | `nginx`, `haproxy`, `redis` |
| JVM 기반인가 | 메모리, GC, `JAVA_HOME`, `setenv.sh` 관리가 필요한가 | `tomcat` |
| 클러스터형 상태 서비스인가 | 노드 간 합류, 초기화, 순서, 데이터 디렉토리 보호가 필요한가 | `kafka`, `elasticsearch` |

이 분류에 따라 롤의 복잡도와 운영 문서의 깊이가 달라집니다.

---

## 공통 설계 원칙

모든 서비스는 아래 구조를 우선으로 설계합니다.

| 영역 | 권장 위치 | 설명 |
|------|-----------|------|
| 실행 자산 | `ops/roles/<role>/` | 실제 설치, 설정, 서비스 시작 |
| 환경 변수 | `ops/inventories/<env>/group_vars/` | dev/staging/prod 별 변수 |
| 운영 설명 | `docs/` | 읽는 순서, 설계 의도, 운영 기준 |
| 점검 기준 | `docs/03-checklists/` | 배포 전 확인 항목 |
| 실패 대응 | `docs/04-runbooks/` | 장애, 롤백, 재배포 절차 |

롤 내부는 가능하면 다음 순서를 따릅니다.

```text
install -> configure -> service -> validate
```

태스크 파일 분리는 다음처럼 잡는 편이 안정적입니다.

```text
roles/<service>/
├── tasks/
│   ├── main.yml
│   ├── install.yml
│   ├── configure.yml
│   ├── service.yml
│   └── validate.yml
├── templates/
├── defaults/
├── handlers/
└── files/
```

---

## 서비스별 접근 방식

### 1. Nginx

`nginx`는 가장 단순한 범주입니다. 패키지 설치, 설정 파일 배포, 서비스 시작, 헬스체크가 핵심입니다.

권장 구성:
- `install.yml`: 패키지 설치, 저장소 추가
- `configure.yml`: `nginx.conf`, site/vhost 템플릿 배포
- `service.yml`: 서비스 enable/start
- `validate.yml`: `nginx -t`, `uri` 헬스체크

주의점:
- `template`에는 `validate:`를 붙여 설정 문법을 먼저 검사합니다.
- 설정 변경 후에는 `notify`로만 재시작합니다.
- 사이트 설정은 가능하면 `sites-available` / `sites-enabled` 패턴으로 분리합니다.

### 2. Tomcat

`tomcat`은 JVM 애플리케이션 서버입니다. Nginx보다 설정 포인트가 많습니다.

권장 구성:
- `install.yml`: JDK, Tomcat 바이너리, 전용 사용자, 디렉토리 생성
- `configure.yml`: `server.xml`, `setenv.sh`, `context.xml`, `systemd unit`
- `deploy.yml`: WAR 파일 배포 또는 링크 관리
- `validate.yml`: 포트 체크, `/health` 또는 actuator 확인

주의점:
- `JAVA_HOME`, `CATALINA_HOME`, `CATALINA_BASE`를 변수로 분리합니다.
- `setenv.sh`를 템플릿으로 관리해서 JVM 옵션을 코드로 남깁니다.
- WAR 배포가 있으면 업로드 후 교체 방식과 롤백 방식을 문서에 같이 둡니다.

### 3. Kafka

`kafka`는 단순 서비스가 아니라 클러스터 구성입니다. 설치보다 토폴로지와 순서가 더 중요합니다.

권장 구성:
- `install.yml`: Java, Kafka 바이너리, 전용 계정, 데이터 디렉토리
- `configure.yml`: `server.properties`, `log.dirs`, `listeners`, `advertised.listeners`
- `service.yml`: systemd 등록과 시작
- `validate.yml`: 브로커 상태, 토픽 생성, 프로듀서/컨슈머 테스트

주의점:
- `broker.id`와 `node.id` 같은 식별자는 인벤토리 기반으로 고정합니다.
- `advertised.listeners`는 환경별 접근 경로와 맞아야 합니다.
- Zookeeper 기반인지 KRaft 기반인지 먼저 정하고, 그에 맞는 문서를 분리합니다.

### 4. Elasticsearch

`elasticsearch`는 상태 서비스이므로 데이터 디렉토리, 메모리, 클러스터 조인 절차가 핵심입니다.

권장 구성:
- `install.yml`: 패키지 또는 아카이브 설치
- `configure.yml`: `elasticsearch.yml`, `jvm.options`, `limits`, `sysctl`
- `service.yml`: 서비스 시작, enable
- `validate.yml`: 클러스터 health, node join, shard 상태

주의점:
- `vm.max_map_count`, `ulimit`, `memlock` 같은 OS 튜닝을 같이 관리합니다.
- 데이터 디렉토리는 자동 삭제하지 않도록 보수적으로 처리합니다.
- 초기 클러스터 구성과 노드 추가/제거 절차를 runbook으로 따로 둡니다.

---

## 서비스별 분해 기준

### 설치형 서비스

다음처럼 단순히 패키지를 설치하고 서비스만 올리는 경우입니다.

- `nginx`
- `haproxy`
- `redis`

이 경우 중심은 `install.yml`, `configure.yml`, `service.yml`입니다.

### 애플리케이션 서버

런타임과 배포물이 분리되는 경우입니다.

- `tomcat`

이 경우는 설정 템플릿과 아티팩트 배포가 별도입니다.

### 클러스터형 상태 서비스

노드 역할과 부팅 순서가 있는 경우입니다.

- `kafka`
- `elasticsearch`

이 경우는 단일 롤보다 다음이 중요합니다.
- 노드 순서
- bootstrap 절차
- 클러스터 검증
- 롤링 재시작
- 데이터 보존 기준

---

## 권장 문서 순서

서비스를 새로 정리할 때는 다음 문서 순서로 맞추는 게 가장 덜 흔들립니다.

1. `docs/01-basics/getting-started.md`
2. `docs/02-examples/service-build-guide.md`
3. `docs/01-basics/07_roles.md`
4. `docs/01-basics/08_templates.md`
5. `docs/03-checklists/pre-deploy.md`
6. `docs/04-runbooks/playbook-failure.md`
7. `ops/README.md`

---

## 실제 구현 체크리스트

- [ ] 서비스 유형을 단일/앱서버/클러스터형으로 먼저 분류했다
- [ ] `defaults/main.yml`에 기본값을 모았다
- [ ] `group_vars`와 `vault.yml`을 분리했다
- [ ] 템플릿에 `validate:` 또는 사전 점검을 넣었다
- [ ] 서비스 재시작은 handler로만 유도했다
- [ ] `uri`, `command`, `shell` 검증은 최소화하고 조건을 명시했다
- [ ] 운영용 헬스체크와 실패 대응 절차를 `docs/04-runbooks/`에 연결했다
- [ ] `--tags`, `--limit`, `--check`, `--diff` 실행 예시를 문서에 남겼다

---

## 참고 경로

- `docs/91-templates/service-doc.md`
- `docs/90-standards/ansible-conventions.md`
- `docs/02-examples/README.md`
- `ops/roles/webserver/`
- `ops/roles/tomcat/`
- `ops/roles/redis/`
- `ops/roles/haproxy/`
