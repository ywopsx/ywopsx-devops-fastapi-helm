# DevOps 과제: FastAPI & Kubernetes 배포

## 1. 프로젝트 개요
FastAPI 기반 웹 애플리케이션을 Kubernetes 환경에서 배포하고 테스트하기 위한 샘플 프로젝트입니다.
로컬 개발 환경에서는 Python 3.13 기반 가상환경에서 테스트 가능하며, Kubernetes 배포 시 Helm Chart와 Ingress를 활용합니다.

---

## 2. 환경 요구사항

- Python 3.13.7 (최신 안정 버전, 라이브러리 호환, 과제 환경 실사용 버전)
- Base Image: `python:3.13-slim` (컨테이너 경량화, 보안 취약점 최소화)
- Docker 28.3.3 (BuildKit 지원, Minikube 환경 호환)
- Helm 3.18.6 (Kubernetes v1.33/v1.34 호환)
- Kubernetes Minikube v1.36.0
  - Server v1.33.1, Client v1.34.0 (로컬 실습 환경, Helm Chart 배포 검증용)


---

## 3. 파이썬 실행 환경 준비 (로컬 테스트용)

```bash
# pipenv 설치 (MacOS)
brew install pipenv

# 프로젝트용 가상환경 생성 (Python 3.13)
pipenv --python 3.13

# FastAPI, Uvicorn 설치
pipenv install fastapi uvicorn

# 가상환경 활성화
pipenv shell

# 앱 실행 (localhost:3000)
pipenv run uvicorn main:app --host 0.0.0.0 --port 3000
```

> `localhost:3000`에서 FastAPI 앱을 테스트할 수 있습니다.

---

## 4. Docker 빌드 및 실행

```bash
# Docker 이미지 빌드
docker build -t devops_test:v1.0 .

# 컨테이너 실행
docker run -d -p 3000:3000 --name devops_test devops_test:v1.0

# 실행 중 컨테이너 확인
docker ps

# 종료 및 제거
docker stop devops_test
docker rm devops_test

# 이미지 제거 (필요 시)
docker rmi devops_test:v1.0

# 이미지 Docker Hub에 푸시 (선택)
docker tag devops_test:v1.0 ywroh519/devops_test:v1.0
docker push ywroh519/devops_test:v1.0
```

---

## 5. Minikube + Helm 배포

### 5.1 네임스페이스 생성

```bash
kubectl create namespace autoever-dev
kubectl create namespace autoever-stg
kubectl create namespace autoever-prd
```

### 5.2 Secret 생성 (DB 계정 관리용)

`secret.yaml` 파일은 헬름 차트 외부에 위치하며, 아래 명령어로 배포:

```bash
kubectl apply -f secret.yaml
```

예: dev 환경 Secret

```yaml
apiVersion: v1
kind: Secret
metadata:
  name: autoever-dev-db-secret
  namespace: autoever-dev
type: Opaque
stringData:
  username: dev_user
  password: dev_pass
```

> stg/prd 환경도 동일한 방식으로 관리합니다.

### 5.3 Helm Chart 배포

```bash
# dev 환경
helm upgrade autoever-dev ./autoever-chart -f ./autoever-chart/values-dev.yaml --set image.tag="v1.0" --namespace autoever-dev

# stg 환경
helm upgrade autoever-stg ./autoever-chart -f ./autoever-chart/values-stg.yaml --set image.tag="v1.0" --namespace autoever-stg

# prd 환경
helm upgrade autoever-prd ./autoever-chart -f ./autoever-chart/values-prd.yaml --set image.tag="v1.0" --namespace autoever-prd
```

---

## 6. Ingress 구조 및 ClusterIP 서비스

Minikube에서는 서비스 타입을 **ClusterIP**로 설정하고, 도메인 테스트를 위해 `minikube tunnel` 사용:

```bash
sudo minikube tunnel
```

- 브라우저 테스트용 hosts 예시: `127.0.0.1 devops-test.autoever.test`
- ClusterIP 서비스는 외부 IP를 가지지 않으므로, Tunnel을 통해 Ingress를 노출해야 함
- values-prd.yaml 예시:

```yaml
namespace: autoever-prd
replicaCount: 3
env: prd

ingress:
  hosts:
    - host: devops-test.autoever.test
      paths:
        - path: /
          pathType: Prefix
          backend:
            service:
              name: autoever-prd-autoever-chart
              port:
                number: 80
```

---

## 7. 레포지토리 구조

```
FASTAPI_TEST/
├── autoever-chart/
│   ├── templates/
│   │   ├── _helpers.tpl
│   │   ├── configmap.yaml
│   │   ├── deployment.yaml
│   │   ├── ingress.yaml
│   │   └── service.yaml
│   ├── .helmignore
│   ├── Chart.yaml
│   ├── values.yaml
│   ├── values-dev.yaml
│   ├── values-stg.yaml
│   └── values-prd.yaml
├── Dockerfile
├── main.py
├── README.md
├── requirements.txt
└── secret.yaml
```
- autoever-chart/ : Helm Chart 관련 파일 전체
- templates/ : Helm 템플릿 (Deployment, Service, Ingress 등)
- values-*.yaml : 환경별 값 (dev/stg/prd)
- Dockerfile : FastAPI 앱 컨테이너 빌드
- main.py : FastAPI 애플리케이션 코드
- requirements.txt : Python 의존성
- secret.yaml : Kubernetes Secret (DB 계정 등)
- README.md : 프로젝트 설명

---

## 8. GitHub에 업로드

```bash
# Git 초기화 (필요 시)
git init

# 모든 변경사항 추가
git add .

# 커밋
git commit -m "Initial commit with README, Dockerfile, Helm chart"

# GitHub 레포지토리 연결
git remote add origin <레포지토리_URL>

# 브랜치 설정 및 push
git branch -M main
git push -u origin main
