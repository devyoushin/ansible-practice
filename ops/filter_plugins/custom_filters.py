#!/usr/bin/env python3
# =============================================================
# Ansible 커스텀 필터 플러그인
# Jinja2 템플릿에서 {{ value | filter_name }} 형태로 사용
#
# 사용 예시:
#   {{ "512m" | parse_memory_mb }}           → 512
#   {{ servers | to_haproxy_backend }}        → HAProxy 설정 문자열
#   {{ "2024-01-15" | days_since }}          → 81 (경과 일수)
# =============================================================

from datetime import datetime, timezone


def parse_memory_mb(value):
    """
    메모리 문자열을 MB 정수로 변환
    예: "512m" → 512, "2g" → 2048, "1024" → 1024
    """
    value = str(value).lower().strip()
    if value.endswith('g'):
        return int(float(value[:-1]) * 1024)
    elif value.endswith('m'):
        return int(value[:-1])
    elif value.endswith('k'):
        return int(float(value[:-1]) / 1024)
    else:
        return int(value)


def to_haproxy_backend(servers, port=80, check_interval="5s"):
    """
    서버 목록을 HAProxy backend 설정 문자열로 변환
    사용: {{ groups['webservers'] | to_haproxy_backend(port=80) }}
    """
    lines = []
    for i, server in enumerate(servers):
        lines.append(
            f"    server {server} {server}:{port} "
            f"check inter {check_interval} rise 2 fall 3"
        )
    return "\n".join(lines)


def days_since(date_string, fmt="%Y-%m-%d"):
    """
    날짜 문자열로부터 경과 일수 계산
    사용: {{ "2024-01-01" | days_since }}
    """
    try:
        target = datetime.strptime(date_string, fmt)
        delta = datetime.now() - target
        return delta.days
    except (ValueError, TypeError):
        return -1


def mask_secret(value, show_chars=4):
    """
    시크릿 값을 마스킹 (로그 출력용)
    사용: {{ vault_db_password | mask_secret }}  → "dev-****"
    """
    value = str(value)
    if len(value) <= show_chars:
        return "*" * len(value)
    return value[:show_chars] + "*" * (len(value) - show_chars)


def to_yaml_list(items, indent=2):
    """
    Python 리스트를 YAML 리스트 문자열로 변환
    사용: {{ packages | to_yaml_list }}
    """
    prefix = " " * indent + "- "
    return "\n".join(f"{prefix}{item}" for item in items)


def filter_by_env(items, env, env_key="environment"):
    """
    환경별 필터링
    사용: {{ all_configs | filter_by_env('prod') }}
    """
    return [item for item in items if item.get(env_key) == env]


def sizeof_fmt(num, suffix="B"):
    """
    바이트를 사람이 읽기 쉬운 형태로 변환
    사용: {{ 1073741824 | sizeof_fmt }}  → "1.0 GiB"
    """
    for unit in ("", "Ki", "Mi", "Gi", "Ti"):
        if abs(num) < 1024.0:
            return f"{num:3.1f} {unit}{suffix}"
        num /= 1024.0
    return f"{num:.1f} Pi{suffix}"


# ----------------------------
# Ansible FilterModule 등록
# 이 클래스가 없으면 Ansible이 필터를 인식하지 못함
# ----------------------------
class FilterModule(object):
    def filters(self):
        return {
            'parse_memory_mb':    parse_memory_mb,
            'to_haproxy_backend': to_haproxy_backend,
            'days_since':         days_since,
            'mask_secret':        mask_secret,
            'to_yaml_list':       to_yaml_list,
            'filter_by_env':      filter_by_env,
            'sizeof_fmt':         sizeof_fmt,
        }
