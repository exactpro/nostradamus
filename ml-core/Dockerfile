FROM python:3.7.9-slim

WORKDIR /app

USER root

RUN apt-get update && apt-get install -y gcc \
  build-essential libpq-dev libffi-dev --no-install-recommends
RUN pip install --upgrade pip && pip install flake8 && pip install Cython

RUN pip3 install poetry==1.1.4

COPY poetry.lock pyproject.toml /app/

RUN poetry install --no-dev

COPY . /app/
