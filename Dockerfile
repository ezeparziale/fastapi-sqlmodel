FROM python:3.11

WORKDIR /usr/src/app

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

RUN pip install --upgrade pip
COPY ./requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY app/ ./app

ENTRYPOINT [ "uvicorn", "app.main:app", "--workers", "4", "--host", "0.0.0.0", "--port", "8000"]