FROM python:3.9

LABEL owner='fgd196111@yandex.ru'

ENV PYTHONONUNBUFFERED=1

WORKDIR /app

COPY . /app 

RUN pip install --no-cache-dir -r requirements.txt

CMD ['uvicorn', 'backend/main:app', '--host', '--port 80']