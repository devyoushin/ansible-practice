# 08. 템플릿 (Templates / Jinja2)

> "변수를 채워넣어 설정 파일을 자동으로 생성"

---

## 왜 템플릿이 필요한가?

```bash
# 서버마다 다른 설정 파일이 필요한 경우
web1: server_name = web1.example.com, port = 80
web2: server_name = web2.example.com, port = 80
db1:  bind_address = 192.168.1.20, port = 3306
```

파일을 서버마다 따로 만들면 유지보수가 힘들어집니다.
템플릿 하나로 모든 서버의 설정 파일을 자동 생성합니다.

---

## 기본 사용법

```
[템플릿 파일] + [변수값] → [완성된 설정 파일]
nginx.conf.j2   vars.yml    /etc/nginx/nginx.conf
```

```yaml
# 태스크에서 template 모듈 사용
tasks:
  - name: Nginx 설정 파일 배포
    template:
      src: nginx.conf.j2          # templates/ 폴더 기준 (롤 안에서)
      dest: /etc/nginx/nginx.conf
      owner: root
      group: root
      mode: "0644"
    notify: Nginx 재시작
```

---

## 템플릿 문법 기초

```jinja2
{# nginx.conf.j2 — 주석은 {# #} #}

# Nginx 설정 파일
# 생성일: {{ ansible_date_time.date }}
# 호스트: {{ inventory_hostname }}

worker_processes  {{ nginx_worker_processes }};    {# 변수 삽입 #}

events {
    worker_connections  {{ nginx_worker_connections | default(1024) }};
}

http {
    keepalive_timeout  {{ nginx_keepalive_timeout }};
    server_tokens      off;

    server {
        listen       {{ nginx_port }};
        server_name  {{ ansible_hostname }};   {# Facts 변수 사용 #}

        root  /var/www/html;
        index index.html;
    }
}
```

---

## 자주 쓰는 Jinja2 문법

### 변수 출력

```jinja2
{{ 변수명 }}
{{ config.key }}         {# 딕셔너리 #}
{{ items[0] }}           {# 리스트 첫 번째 #}
{{ "기본값" if 변수가없으면 }}
{{ 변수 | default("기본값") }}    {# 없으면 기본값 #}
```

### if 조건문

```jinja2
{% if env == "prod" %}
worker_processes  4;
{% elif env == "staging" %}
worker_processes  2;
{% else %}
worker_processes  1;
{% endif %}
```

### for 반복문

```jinja2
{# upstream 블록 자동 생성 #}
upstream backend {
{% for server in app_servers %}
    server {{ server.ip }}:{{ server.port }} weight={{ server.weight | default(1) }};
{% endfor %}
}
```

### 필터 활용

```jinja2
{{ app_name | upper }}           {# MYAPP #}
{{ memory_mb | int * 1024 }}     {# 숫자 연산 #}
{{ items | join(", ") }}         {# 리스트 → "a, b, c" #}
{{ path | basename }}            {# /etc/nginx → nginx #}
{{ text | replace("old", "new") }}
```

---

## 실전 예제: Nginx 가상호스트 설정

```yaml
# group_vars/webservers.yml
nginx_vhosts:
  - server_name: myapp.example.com
    port: 80
    root: /var/www/myapp
    index: index.html
  - server_name: api.example.com
    port: 80
    root: /var/www/api
    proxy_pass: http://localhost:8080
```

```jinja2
{# templates/vhost.conf.j2 #}

{% for vhost in nginx_vhosts %}
server {
    listen       {{ vhost.port }};
    server_name  {{ vhost.server_name }};

{% if vhost.proxy_pass is defined %}
    {# 리버스 프록시 설정 #}
    location / {
        proxy_pass         {{ vhost.proxy_pass }};
        proxy_set_header   Host $host;
        proxy_set_header   X-Real-IP $remote_addr;
    }
{% else %}
    {# 정적 파일 서빙 #}
    root   {{ vhost.root }};
    index  {{ vhost.index | default("index.html") }};

    location / {
        try_files $uri $uri/ =404;
    }
{% endif %}

    access_log  /var/log/nginx/{{ vhost.server_name }}_access.log;
    error_log   /var/log/nginx/{{ vhost.server_name }}_error.log;
}

{% endfor %}
```

**생성 결과:**
```nginx
server {
    listen       80;
    server_name  myapp.example.com;

    root   /var/www/myapp;
    index  index.html;

    location / {
        try_files $uri $uri/ =404;
    }

    access_log  /var/log/nginx/myapp.example.com_access.log;
    error_log   /var/log/nginx/myapp.example.com_error.log;
}

server {
    listen       80;
    server_name  api.example.com;

    location / {
        proxy_pass         http://localhost:8080;
        proxy_set_header   Host $host;
        proxy_set_header   X-Real-IP $remote_addr;
    }
    ...
}
```

---

## copy vs template 차이

| 모듈 | 용도 |
|------|------|
| `copy` | 파일을 그대로 복사 (변수 치환 없음) |
| `template` | 변수를 채워서 파일 생성 (`.j2` 확장자) |

```yaml
# 정적 파일 — copy 사용
- copy:
    src: files/index.html
    dest: /var/www/html/index.html

# 동적 설정 — template 사용
- template:
    src: templates/nginx.conf.j2
    dest: /etc/nginx/nginx.conf
```

---

## 템플릿 미리 확인하기

```bash
# --check --diff 로 실제 배포 없이 변경 내용 확인
ansible-playbook -i hosts.ini site.yml --check --diff

# 출력 예시:
--- before: /etc/nginx/nginx.conf
+++ after: /etc/nginx/nginx.conf
@@ -1,5 +1,5 @@
 worker_processes  auto;
-keepalive_timeout  65;
+keepalive_timeout  30;    ← 이렇게 변경된다고 미리 알려줌
```

---

## 다음 단계

자주 쓰는 모듈 치트시트 → [09_common_modules.md](09_common_modules.md)
