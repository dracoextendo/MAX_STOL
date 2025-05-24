FROM python:3.13.3-slim

WORKDIR /app

# Устанавливаем openssl
RUN apt-get update && apt-get install -y openssl && rm -rf /var/lib/apt/lists/*

# Создаем папку certs и генерируем сертификаты
RUN mkdir certs && \
    cd certs/ && \
    openssl genrsa -out jwt-private.pem 2048 && \
    openssl rsa -in jwt-private.pem -outform PEM -pubout -out jwt-public.pem && \
    cd ..

COPY . .

RUN pip install -r requirements/requirements.txt

WORKDIR /app/src

CMD ["uvicorn", "main:app", "--host", "0.0.0.0"]