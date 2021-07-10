FROM python:3.8-slim

WORKDIR /app

USER root

RUN apt-get -y update && apt-get install -y libpq-dev gcc \
  && pip install --upgrade pip

RUN pip3 install poetry==1.1.4

COPY poetry.lock pyproject.toml /app/

RUN poetry install --no-dev

COPY . /app/
