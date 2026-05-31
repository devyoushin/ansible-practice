# Ansible 롤 리뷰 체크리스트

- role defaults에 운영자가 조정할 수 있는 값이 분리되어 있는가?
- task는 멱등성을 유지하고 불필요한 changed를 만들지 않는가?
- handler는 필요한 경우에만 notify로 호출되는가?
- template 변경 시 validate 명령 또는 syntax check가 포함되어 있는가?
- 시크릿 값이 로그, template, debug 출력에 노출되지 않는가?
- OS family, 배포판, 버전 차이를 조건으로 처리했는가?
- Molecule 또는 최소한 syntax-check 실행 방법이 문서화되어 있는가?
