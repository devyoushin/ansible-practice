# Ansible Examples

이 폴더는 실제 운영 서버에 바로 적용하기 전에 Ansible 구조를 작게 실습하기 위한 예제 모음입니다.

현재 예제:

```text
examples/custom-nginx
```

`custom-nginx`는 nginx를 OS 기본 경로인 `/etc/nginx`, `/usr/sbin/nginx`에 설치하지 않고, 직접 지정한 `/nginx` 아래에 소스 빌드로 설치하는 예제입니다.

## 왜 이 예제가 필요한가

패키지 매니저로 nginx를 설치하면 보통 배포판 표준 경로를 따릅니다.

```text
/etc/nginx
/usr/sbin/nginx
/var/log/nginx
```

하지만 직접 운영 표준을 잡아서 아래처럼 쓰고 싶을 수 있습니다.

```text
/nginx/sbin/nginx
/nginx/conf/nginx.conf
/nginx/html
/nginx/logs
```

이 경우 Ansible의 역할은 `nginx 패키지 설치`가 아니라, 기존에 수동으로 하던 작업을 코드화하는 것입니다.

```text
소스 tar.gz 준비
빌드 의존성 설치
./configure --prefix=/nginx
make
make install
nginx.conf 배포
systemd 서비스 등록
서비스 시작
헬스체크
```

## 먼저 볼 파일

순서대로 보면 이해하기 좋습니다.

```text
examples/custom-nginx/README.md
examples/custom-nginx/site.yml
examples/custom-nginx/offline-vars.yml
examples/custom-nginx/roles/custom_nginx/defaults/main.yml
examples/custom-nginx/roles/custom_nginx/tasks/main.yml
examples/custom-nginx/roles/custom_nginx/templates/nginx.conf.j2
examples/custom-nginx/roles/custom_nginx/templates/nginx-custom.service.j2
```

## 디렉토리 구조 이해

```text
examples/custom-nginx/
├── README.md
├── site.yml
├── offline-vars.yml
├── inventory/
│   └── hosts.ini
├── files/
│   ├── nginx-1.26.2.tar.gz
│   └── rpms/
└── roles/
    └── custom_nginx/
        ├── defaults/
        ├── handlers/
        ├── tasks/
        └── templates/
```

각 위치의 의미는 다음과 같습니다.

`site.yml`은 어떤 서버 그룹에 어떤 role을 적용할지 정하는 진입점입니다.

`inventory/hosts.ini`는 적용 대상 서버 목록입니다.

`offline-vars.yml`은 폐쇄망 실행에 필요한 변수 예시입니다.

`files/`는 컨트롤 노드가 대상 서버로 복사할 파일을 두는 곳입니다. nginx 소스 tarball이나 RPM/DEB 파일을 여기에 둡니다.

`roles/custom_nginx/defaults/main.yml`은 기본 변수입니다. 설치 경로, nginx 버전, 포트, 의존성 설치 방식을 여기서 바꿀 수 있습니다.

`roles/custom_nginx/tasks/main.yml`은 실제 작업 순서입니다. 수동 설치 명령을 Ansible task로 바꾼 핵심 파일입니다.

`roles/custom_nginx/templates/`는 대상 서버에 배포될 설정 파일 템플릿입니다.

## 폐쇄망 학습 흐름

외부망 접근이 안 되는 환경이라면 먼저 파일을 준비합니다.

```text
examples/custom-nginx/files/nginx-1.26.2.tar.gz
```

빌드 의존성을 내부 repo로 설치할 수 있으면 `offline-vars.yml`에서 이렇게 둡니다.

```yaml
nginx_custom_dependency_install_mode: repo
```

빌드 의존성이 이미 설치되어 있으면 이렇게 둡니다.

```yaml
nginx_custom_dependency_install_mode: skip
```

RPM/DEB 파일까지 Ansible로 전달하려면 이렇게 둡니다.

```yaml
nginx_custom_dependency_install_mode: local_files
nginx_custom_dependency_package_files:
  - examples/custom-nginx/files/rpms/gcc-1.rpm
  - examples/custom-nginx/files/rpms/make-1.rpm
  - examples/custom-nginx/files/rpms/pcre-devel-1.rpm
  - examples/custom-nginx/files/rpms/zlib-devel-1.rpm
  - examples/custom-nginx/files/rpms/openssl-devel-1.rpm
```

RPM은 실제 환경의 OS 버전과 아키텍처에 맞아야 합니다. Rocky 9용 RPM을 Rocky 8에 그대로 쓰는 식으로 섞으면 의존성 문제가 납니다.

## 실행 명령

대상 서버를 `examples/custom-nginx/inventory/hosts.ini`에 적습니다.

```ini
[custom_nginx]
test-vm ansible_host=192.168.56.10 ansible_user=your_user
```

폐쇄망 변수 파일을 같이 넘겨 실행합니다.

```bash
ansible-playbook \
  -i examples/custom-nginx/inventory/hosts.ini \
  examples/custom-nginx/site.yml \
  -e @examples/custom-nginx/offline-vars.yml
```

## 실행 후 확인

대상 서버에서 확인할 내용입니다.

```bash
systemctl status nginx-custom
/nginx/sbin/nginx -V
/nginx/sbin/nginx -t -c /nginx/conf/nginx.conf
curl http://127.0.0.1/
curl http://127.0.0.1/health
```

생성된 파일도 확인합니다.

```bash
ls -l /nginx
ls -l /nginx/conf
ls -l /nginx/logs
cat /etc/systemd/system/nginx-custom.service
```

## 자주 막히는 지점

`gcc: command not found`가 나오면 빌드 의존성이 설치되지 않은 것입니다. 내부 repo를 쓰거나 RPM 파일을 준비해야 합니다.

`./configure: error: the HTTP rewrite module requires the PCRE library`가 나오면 `pcre-devel` 계열 패키지가 빠진 것입니다.

`SSL modules require the OpenSSL library`가 나오면 `openssl-devel` 계열 패키지가 빠진 것입니다.

`Address already in use`가 나오면 이미 80 포트를 쓰는 프로세스가 있습니다. `nginx_custom_port`를 바꾸거나 기존 서비스를 중지해야 합니다.

`Permission denied`가 나오면 `/nginx` 생성 권한이나 systemd 등록 권한이 부족한 것입니다. playbook은 `become: true`로 실행되어야 합니다.

## 학습 포인트

이 예제에서 가장 중요한 부분은 모듈 이름이 아니라 역할 분리입니다.

`defaults/main.yml`에는 바뀔 수 있는 값을 둡니다.

`tasks/main.yml`에는 서버 상태를 만드는 절차를 둡니다.

`templates/*.j2`에는 서버마다 조금씩 달라질 설정 파일을 둡니다.

`handlers/main.yml`에는 설정 변경 후 재시작이나 reload 같은 후속 동작을 둡니다.

이 구조에 익숙해지면 nginx뿐 아니라 Redis, Tomcat, 사내 에이전트, 보안 솔루션 같은 수동 설치 절차도 같은 방식으로 role로 바꿀 수 있습니다.
