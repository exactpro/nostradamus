###########
# BUILDER #
###########

# pull official base image
FROM python:3.7-slim as builder

# set work directory
WORKDIR /usr/src/app/

# set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# install dependencies
RUN apt-get update
RUN apt-get -y upgrade
RUN dpkg --configure -a
RUN apt-get install gcc -y \
  build-essential libpq-dev libffi-dev --no-install-recommends
RUN apt-get clean
RUN pip install --upgrade pip && pip install flake8 && pip install Cython
COPY ./requirements.txt .
RUN pip wheel --no-cache-dir --no-deps --wheel-dir /usr/src/app/wheels -r requirements.txt

# copy source code
COPY . /usr/src/app/

#########
# FINAL #
#########

# pull official base image
FROM python:3.7-slim

# create directory for the app user
RUN mkdir -p /home/app

# create the appropriate directories
ENV HOME=/home/app
ENV APP_HOME=/home/app/nostradamus
RUN mkdir $APP_HOME
WORKDIR $APP_HOME

# install dependencies
COPY --from=builder /usr/src/app/wheels /wheels
COPY --from=builder /usr/src/app/requirements.txt .
RUN pip install --upgrade pip && pip install --no-cache /wheels/*

# copy the project
COPY . $APP_HOME

EXPOSE 8000
