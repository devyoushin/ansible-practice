# 모니터링 지침 — ansible-practice

## 배포 후 확인 항목

### 서비스 상태 확인

```bash
# 모든 대상 호스트 서비스 상태
ansible -i inventories/prod/hosts.ini webservers -m shell \
  -a "systemctl status nginx"

# 최근 에러 로그 확인
ansible -i inventories/prod/hosts.ini all -m shell \
  -a "journalctl -u {{ service }} --since '10 minutes ago' | grep -i error"
```

### 헬스 체크

```bash
# 웹서버 응답 확인
ansible -i inventories/prod/hosts.ini webservers -m uri \
  -a "url=http://localhost/health return_content=yes"

# 포트 리스닝 확인
ansible -i inventories/prod/hosts.ini all -m shell \
  -a "ss -tlnp | grep LISTEN"
```

## Prometheus 수집 대상 (monitoring 롤)

| 컴포넌트 | Exporter | 포트 |
|---------|----------|------|
| OS | node_exporter | 9100 |
| MariaDB | mysqld_exporter | 9104 |
| Nginx | nginx_exporter | 9113 |
| Redis | redis_exporter | 9121 |
| HAProxy | haproxy_exporter | 9101 |

## 핵심 알람 규칙

| 알람 | 조건 | 심각도 |
|------|------|--------|
| 노드 다운 | `up == 0` 1분 | Critical |
| CPU 과부하 | `cpu > 80%` 5분 | Warning |
| 메모리 부족 | `mem_available < 10%` | Warning |
| 디스크 풀 | `disk_used > 85%` | Warning |
| 서비스 재시작 | `restart_count > 3` 1시간 | Warning |

## Ansible 실행 모니터링

```bash
# 배포 성공/실패 요약
ansible-playbook ... 2>&1 | tee /var/log/ansible/$(date +%Y%m%d).log

# 실패 호스트만 재실행
ansible-playbook ... --limit @/path/to/retry_hosts
```

## 롤별 헬스 체크 태스크

각 롤의 tasks/healthcheck.yml에 배포 후 검증 태스크를 포함:

```yaml
- name: "서비스 헬스 체크"
  uri:
    url: "http://localhost:{{ app_port }}/health"
    status_code: 200
  retries: 5
  delay: 10
  tags: [healthcheck]
```
