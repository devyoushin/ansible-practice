# Custom Nginx under /nginx

이 예제는 OS 패키지의 기본 `/etc/nginx`, `/usr/sbin/nginx` 구조를 쓰지 않고,
nginx를 소스 빌드해서 `/nginx` 아래에 설치하는 Ansible role 예시입니다.

생성되는 주요 경로:

```text
/nginx/sbin/nginx
/nginx/conf/nginx.conf
/nginx/conf/conf.d/default.conf
/nginx/html/index.html
/nginx/logs/access.log
/nginx/logs/error.log
/etc/systemd/system/nginx-custom.service
```

## 실행 방법

테스트 대상 서버를 `inventory/hosts.ini`에 적은 뒤 실행합니다.

```bash
ansible-playbook -i ops/02-examples/custom-nginx/inventory/hosts.ini ops/02-examples/custom-nginx/site.yml
```

로컬 VM이나 테스트 서버에 먼저 적용하려면:

```ini
[custom_nginx]
test-vm ansible_host=192.168.56.10 ansible_user=your_user
```

## 주요 변수

기본값은 `roles/custom_nginx/defaults/main.yml`에 있습니다.

```yaml
nginx_custom_prefix: /nginx
nginx_custom_version: "1.26.2"
nginx_custom_port: 80
nginx_custom_service_name: nginx-custom
```

설치 위치를 `/data/nginx`로 바꾸고 싶다면 playbook이나 inventory group_vars에서:

```yaml
nginx_custom_prefix: /data/nginx
```

처럼 오버라이드하면 됩니다.

## 수동 설치와의 대응 관계

이 role은 수동 작업으로 치면 아래 절차를 Ansible로 옮긴 것입니다.

```bash
./configure --prefix=/nginx --conf-path=/nginx/conf/nginx.conf
make
make install
systemctl enable --now nginx-custom
```

이미 설치된 버전은 `/nginx/.nginx-version` 파일로 확인합니다. `nginx_custom_version`을 바꾸면 다시 빌드/설치합니다.

## 폐쇄망에서 tar.gz로 전달하는 경우

인터넷이 안 되는 환경에서는 nginx 소스 파일을 컨트롤 노드에 미리 두고 실행합니다.

예시 파일 배치:

```text
ops/02-examples/custom-nginx/files/nginx-1.26.2.tar.gz
```

그 다음 `nginx_custom_source_archive`를 지정합니다.

```yaml
nginx_custom_version: "1.26.2"
nginx_custom_source_archive: ops/02-examples/custom-nginx/files/nginx-1.26.2.tar.gz
```

실행 예:

```bash
ansible-playbook \
  -i ops/02-examples/custom-nginx/inventory/hosts.ini \
  ops/02-examples/custom-nginx/site.yml \
  -e @ops/02-examples/custom-nginx/offline-vars.yml
```

이 방식에서는 대상 서버가 외부망에 접근하지 않습니다. Ansible 컨트롤 노드가 들고 있는 tarball을 대상 서버의 `/usr/local/src`로 복사한 뒤 빌드합니다.

## 폐쇄망에서 RPM/DEB 의존성까지 같이 전달하는 경우

소스 빌드에는 컴파일러와 라이브러리 개발 패키지가 필요합니다. RedHat 계열 기준으로 보통 아래 패키지들이 필요합니다.

```text
gcc
make
pcre-devel
zlib-devel
openssl-devel
ca-certificates
```

폐쇄망에서 OS repo를 쓸 수 없다면, 해당 RPM 파일과 의존 RPM을 모두 준비해서 컨트롤 노드에 둡니다.

예시:

```text
ops/02-examples/custom-nginx/files/rpms/gcc-*.rpm
ops/02-examples/custom-nginx/files/rpms/make-*.rpm
ops/02-examples/custom-nginx/files/rpms/pcre-devel-*.rpm
ops/02-examples/custom-nginx/files/rpms/zlib-devel-*.rpm
ops/02-examples/custom-nginx/files/rpms/openssl-devel-*.rpm
ops/02-examples/custom-nginx/files/rpms/*.rpm
```

변수는 이렇게 둡니다.

```yaml
nginx_custom_dependency_install_mode: local_files
nginx_custom_dependency_package_files:
  - ops/02-examples/custom-nginx/files/rpms/gcc-1.rpm
  - ops/02-examples/custom-nginx/files/rpms/make-1.rpm
  - ops/02-examples/custom-nginx/files/rpms/pcre-devel-1.rpm
  - ops/02-examples/custom-nginx/files/rpms/zlib-devel-1.rpm
  - ops/02-examples/custom-nginx/files/rpms/openssl-devel-1.rpm
```

주의할 점은 RPM 파일명을 예시처럼 와일드카드로 쓰면 안 된다는 점입니다. Ansible 변수에는 실제 파일명을 하나씩 적는 편이 가장 명확합니다.

이미 대상 서버에 빌드 의존성이 설치되어 있다면 설치 단계를 건너뛸 수 있습니다.

```yaml
nginx_custom_dependency_install_mode: skip
```

정리하면 폐쇄망에서는 보통 아래 둘 중 하나를 씁니다.

```text
방식 A: 의존성은 내부 repo로 설치 + nginx 소스 tar.gz만 Ansible로 복사
방식 B: 의존성 RPM/DEB도 Ansible로 복사 설치 + nginx 소스 tar.gz도 복사
```

내부 yum/dnf/apt repo가 있다면 `nginx_custom_dependency_install_mode: repo`를 그대로 두고, nginx 소스만 `nginx_custom_source_archive`로 넘기는 방식이 가장 깔끔합니다.
