FROM tiangolo/uwsgi-nginx-flask:python3.8

ADD ./requirements.txt /

RUN pip install -r /requirements.txt

COPY . /app

WORKDIR /app

RUN . /app/env_vars.sh

RUN flask db init

