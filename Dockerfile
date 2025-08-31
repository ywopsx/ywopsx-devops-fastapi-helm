# 안정성과 DB 드라이버 호환성을 고려해 slim 사용
FROM python:3.13-slim

# 작업 디렉토리
WORKDIR /app

# 패키지 의존성 사전 복사 (캐시 최적화)
COPY requirements.txt .
RUN pip install --no-cache-dir --upgrade pip \
    && pip install --no-cache-dir -r requirements.txt

# 앱 코드 복사
COPY . .

# 비root 사용자 권장
RUN useradd -m appuser
USER appuser

# 컨테이너 포트
EXPOSE 3000

# FastAPI 실행
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "3000"]
