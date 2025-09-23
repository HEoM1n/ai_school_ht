FROM python:3.11-slim

WORKDIR /app

# Oracle Instant Client 설치 (cx_Oracle 의존성)
RUN apt-get update && apt-get install -y \
    wget \
    unzip \
    libaio1 \
    && rm -rf /var/lib/apt/lists/*

# Oracle Instant Client 다운로드 및 설치
RUN mkdir -p /opt/oracle && \
    cd /opt/oracle && \
    wget https://download.oracle.com/otn_software/linux/instantclient/1923000/instantclient-basic-linux.x64-19.23.0.0.0dbru.zip && \
    unzip instantclient-basic-linux.x64-19.23.0.0.0dbru.zip && \
    rm instantclient-basic-linux.x64-19.23.0.0.0dbru.zip && \
    echo /opt/oracle/instantclient_19_23 > /etc/ld.so.conf.d/oracle-instantclient.conf && \
    ldconfig

# 환경변수 설정
ENV LD_LIBRARY_PATH=/opt/oracle/instantclient_19_23:$LD_LIBRARY_PATH

# Python 의존성 설치
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# 애플리케이션 코드 복사
COPY . .

# uploads 디렉토리 생성
RUN mkdir -p uploads

EXPOSE 8000

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]