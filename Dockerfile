FROM python:3.9

LABEL owner='fgd19611@yandex.ru'

ENV PYTHONONUNBUFFERED=1

WORKDIR /app

COPY requirements.txt /app/

RUN pip install --no-cache-dir -r requirements.txt

COPY . /app 

CMD ["uvicorn", "backend.main:app", "--host", "0.0.0.0", "--port", "80"]